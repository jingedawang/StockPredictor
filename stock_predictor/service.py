import datetime
from itertools import chain
import json
import math
import pandas as pd
import pypinyin
import qlib.data
import tqdm
from typing import Iterable

import constants
from crawler import Crawler
from database import Database
import predict
from stock import Stock


class Service:
    """
    Backend service class.

    This class provides all the necessary methods for the web app.
    """

    def __init__(self) -> None:
        """
        Initialize service.
        """
        qlib.init(provider_uri=constants.QLIB_DATA_PATH)
        self.database = Database()

    def load_stock_list(self) -> None:
        """
        Load stock list from official stock exchange website and update the database.
        """
        # Crawl the stock list files from the official websites of stock exchanges.
        with Crawler() as cralwer:
            cralwer.crawl_shanghai_stock_list(constants.SH_STOCK_LIST_PATH)
            shanghai_stock_list = pd.read_excel(constants.SH_STOCK_LIST_PATH, dtype=str)[['A股代码', '证券简称', '上市日期']]
            cralwer.crawl_shenzhen_stock_list(constants.SZ_STOCK_LIST_PATH)
            shenzhen_stock_list = pd.read_excel(constants.SZ_STOCK_LIST_PATH, dtype=str)[['A股代码', 'A股简称', 'A股上市日期']]

        # Combine two stock lists.
        shanghai_stock_list.columns = ['id', 'name', 'listing_date']
        shanghai_stock_list['stock_exchange'] = 'SH'
        shenzhen_stock_list.columns = ['id', 'name', 'listing_date']
        shenzhen_stock_list['stock_exchange'] = 'SZ'
        stock_list = pd.concat([shanghai_stock_list, shenzhen_stock_list])

        # Load stock list into database.
        print('Load stock list into database...')
        stock_list_with_progressbar = tqdm.tqdm(stock_list.iterrows(), total=stock_list.shape[0])
        for _, row in stock_list_with_progressbar:
            # Remove spaces in name.
            name = row['name'].replace(' ', '')

            # We need to translate the Chinese name of the stock to Pinyin and select the first Character of each word.
            # This will help users look up their stock rapidly.
            # TODO: Need to confirm if there are problems of heteronym.
            pinyin_lists = pypinyin.pinyin(name, style=pypinyin.FIRST_LETTER)
            pinyin = ''.join(list(chain(*pinyin_lists))).upper()

            # Format listing date.
            listing_date = row['listing_date']
            if row['stock_exchange'] == 'SH':
                listing_date = datetime.datetime.strptime(row['listing_date'], '%Y%m%d').strftime('%Y-%m-%d')

            # Update or insert stock.
            stock = Stock(
                id=row['id'],
                pinyin=pinyin,
                name=name,
                qlib_id=row['stock_exchange'] + row['id'],
                delisted=False,
                listing_date=listing_date
            )
            self.database.upsert(stock)

        # Mark a stock as delisted if it doesn't appear in the new stock list.
        id_set = set(stock_list['id'])
        for stock in tqdm.tqdm(self.database.all()):
            if stock.id not in id_set:
                stock.delisted = True
                self.database.upsert(stock)

    def batch(self, iterable, n=1) -> Iterable:
        """
        Batches an iterable to a generator of collections with the size of the inner collection specified.
        For example, given a list of size 250, batch(list, 100) will generate a list of [list[0:100], list[100:200], list[200:250]].

        Args:
            iterable: The collection to be batched.
            n: The batch size. Default 1.
        """
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]

    def predict_all(self, date=None) -> None:
        """
        Predict for all stocks in given date. If no date is given, predict for all the dates.

        Args:
            date: The date to predict.
        """
        if date is None:
            date = constants.START_PREDICTING_DATE

        all_stocks_in_database = self.database.all()
        with tqdm.tqdm(total=len(all_stocks_in_database)) as progress_bar:
            for stocks in self.batch(all_stocks_in_database, 200):
                # Predict a batch of stocks in one forward pass.
                predictions = predict.predict([stock.qlib_id for stock in stocks], start_date=date, end_date=datetime.date.today().strftime('%Y-%m-%d'))
                if not predictions.empty:
                    for stock in stocks:
                        # Check if the result for current stock exists.
                        if not predictions.index.isin([stock.qlib_id], level='instrument').any():
                            continue
                        # Select the prediction for current stock.
                        prediction = predictions.loc[(slice(None), stock.qlib_id),].droplevel('instrument')
                        prediction.index = prediction.index.map(lambda timestamp: timestamp.strftime('%Y-%m-%d'))
                        # Update the stock with the prediction.
                        if stock.predict is None:
                            stock.predict = prediction.to_dict()
                        else:
                            stock.predict.update(prediction.to_dict())
                        self.database.upsert(stock)
                progress_bar.update(len(stocks))

    def fix_mising_prediction(self) -> None:
        """
        Fix the missing predictions.

        Due to some special circumstances, the daily prediction may fail or break.
        We could fix those missing predictions by finding them and re-predict them in this method.
        """
        missed_durations = []
        for stock in self.database.all():
            # If no prediction in current stock, it may be not supported by our data source. We just skip it.
            if stock.predict is None:
                continue

            # Select the date durations that missing a series of consecutive predictions and save them as a tuple.
            supported_trading_days = qlib.data.D.calendar(start_time=constants.START_PREDICTING_DATE, end_time=datetime.date.today().strftime('%Y-%m-%d'))
            start_date = None
            end_date = None
            for trading_day in supported_trading_days:
                date = trading_day.strftime('%Y-%m-%d')
                if date not in stock.predict:
                    # Record the start date and the end date of one duration.
                    if start_date is None:
                        start_date = date
                    end_date = date
                else:
                    # Complete the duration and reset the start date and the end date.
                    if start_date is not None and end_date is not None:
                        missed_durations.append((stock, start_date, end_date))
                        start_date = None
                        end_date = None
            # Don't miss the final duration.
            if start_date is not None and end_date is not None:
                missed_durations.append((stock, start_date, end_date))

        # Predict for each stock's each missing duration and update them into database.
        for missed_duration in tqdm.tqdm(missed_durations):
            stock = missed_duration[0]
            predictions = predict.predict([stock.qlib_id], start_date=missed_duration[1], end_date=missed_duration[2])
            if not predictions.empty:
                # Check if the result exists.
                if not predictions.index.isin([stock.qlib_id], level='instrument').any():
                    continue
                # Select the prediction for this stock.
                prediction = predictions.loc[(slice(None), stock.qlib_id),].droplevel('instrument')
                prediction.index = prediction.index.map(lambda timestamp: timestamp.strftime('%Y-%m-%d'))
                # Update the stock with the prediction.
                if stock.predict is None:
                    stock.predict = prediction.to_dict()
                else:
                    stock.predict.update(prediction.to_dict())
                self.database.upsert(stock)

    def get_stock_list(self) -> str:
        """
        Get the stock list from database.

        Returns:
            The JSON string of the stock list.
        """
        stocks = []
        for stock in self.database.all():
            # Don't return delisted stock.
            if stock.delisted:
                continue

            # Only return following 3 fields for the request.
            keep = ['id', 'pinyin', 'name']
            filtered_stock_json = {key: value for key, value in stock.to_dict().items() if key in keep}
            stocks.append(filtered_stock_json)
        return json.dumps(stocks, ensure_ascii=False)

    def get_history_and_predict_result(self, id: str, date: str) -> str:
        """
        Get the history prices and the predicted price of the stock.

        Args:
            id: The id of the stock, which is a 6-digit number.
            date: The date when the request is sent. This will be used to infer the predicting date.

        Returns:
            A JSON string containing the history prices and the predicted price of the stock.
        """
        # Retrieve the stock with given id from the database.
        stock = self.database.search(id)
        if stock is None:
            raise LookupError(f'No such id in database: {id}')

        # Get history prices.
        recent_40_trading_days = qlib.data.D.calendar(start_time=(pd.Timestamp(date) - pd.Timedelta(days=80)).strftime("%Y-%m-%d"), end_time=date)[-40:]
        history_data = qlib.data.D.features([stock.qlib_id], ['$close/$factor'], recent_40_trading_days[0].strftime('%Y-%m-%d'), date)
        history = [{key[1].strftime('%Y-%m-%d'): round(value, 2)} for key, value in history_data.to_dict()['$close/$factor'].items() if not math.isnan(value)]

        # Get predicted price.
        predicted_trading_date = None
        predicted_price = None
        if stock.predict is not None:
            latest_trading_date = None
            offset = 0
            while latest_trading_date not in stock.predict:
                # Find the latest supported trading date.
                # Ideally, latest supported trading date should be today (if today's stock market has closed) or yesterday (if today's stock market has not closed).
                # But if there is any unexpected circumstance that yesterday's data is missing, we need to use former data instead.
                offset -= 1
                latest_trading_date = list(history[offset].keys())[0]
            latest_price = history[offset][latest_trading_date]
            predicted_trading_date = (pd.Timestamp(latest_trading_date) + pd.Timedelta(days=14)).strftime("%Y-%m-%d")
            predicted_price = round((1.0 + stock.predict[latest_trading_date]) * latest_price, 2)
        else:
            raise LookupError(f'Stock {id} is not supported yet.')

        # Return the necessary values of the stock and convert it to json string.
        stock.history = history
        stock.predict = {predicted_trading_date: predicted_price}
        return stock.to_json(ensure_ascii=False)
import datetime
import json
import os
from pathlib import Path
import pandas as pd
import pypinyin
import qlib.data
from tinydb import TinyDB, Query
import tqdm
import predict
from functools import partial
from stock import Stock
from concurrent.futures import ThreadPoolExecutor, as_completed


## Define the database file name here.
STOCK_DATABASE = Path('~/.stock/stock.json').expanduser()

def load_stock_list():
    """
    Load stock list from a csv file and insert the data into database.
    """
    os.makedirs(os.path.dirname(STOCK_DATABASE), exist_ok=True)
    database = TinyDB(STOCK_DATABASE)

    print('Load stock list into database...')
    stock_list = pd.read_csv(os.path.dirname(__file__) + '/../data/stock_list.csv')
    stock_list_with_progressbar = tqdm.tqdm(stock_list.iterrows(), total=stock_list.index.size)
    for _, row in stock_list_with_progressbar:
        id = row['ts_code'][:-3]
        name = row['name']
        enname = row['enname']
        qlib_id = row['ts_code'][-2:] + row['ts_code'][:6]

        # We need to translate the Chinese name of the stock to Pinyin and select the first Character of each word.
        # This will help users look up their stock rapidly.
        # TODO: Need to confirm if there are problems of heteronym.
        # TODO: English characters are dropped by the pypinyin library.
        pinyin_list = pypinyin.pinyin(name, style=pypinyin.NORMAL)
        pinyin_first_characters = []
        for word in pinyin_list:
            pinyin_first_characters.append(word[0][0].upper())
        pinyin = "".join(pinyin_first_characters)
        stock = Stock(id, pinyin, name, qlib_id, enname=enname)
        stock_json = stock.to_dict()
        query = Query()
        database.upsert(stock_json, query.id == stock.id)

def predict_all(date=None, force_update=False):
    """
    Predict for all stocks in given date. If no date is given, predict for all the dates.

    Args:
        date: The date to predict.
        force_update: Never skip any stocks if set to `True`.
    """
    qlib.init(provider_uri='~/.qlib/qlib_data/cn_data')
    database = TinyDB(STOCK_DATABASE)   
    predict_all_loop_fixed = partial(predict_all_loop, date, force_update)
    with tqdm.tqdm(database.all()) as database_with_progressbar:
        with ThreadPoolExecutor(max_workers= 100) as poolExecutor:  
            futures = []  
            rows = [] 
            for row in database_with_progressbar:
                futures.append(poolExecutor.submit(predict_all_loop_fixed, row))
            for future in as_completed(futures):
                rows.append(future.result())                
        for row in rows:
            database.upsert(row, Query().id == row['id'])
            database_with_progressbar.update(1)
            
def predict_all_loop(date, force_update, row):    
        prediction = pd.DataFrame()
        if date is None:
            # If no date specified, predict all the dates start from 2022-01-01.
            if row['predict'] is not None and not force_update:                

                # If the predictions already exist in the database, don't waste time on repeating it, unless force_update is set.
                return
            prediction = predict.predict(row['qlib_id'], start_date='2022-01-01', end_date=datetime.date.today().strftime('%Y-%m-%d'))
        else:
            # If a date is specified, predict for it.
            prediction = predict.predict(row['qlib_id'], start_date=date, end_date=date)
        if not prediction.empty:
            prediction = prediction.loc[(slice(None), row['qlib_id']),].droplevel('instrument')
            prediction.index = prediction.index.map(lambda timestamp: timestamp.strftime('%Y-%m-%d'))
            # Append the predictions to the already existing ones.
            if row['predict'] is None:
                row['predict'] = prediction.to_dict()
            else:
                row['predict'].update(prediction.to_dict())
        return row
            
    
def get_stock_list() -> str:
    """
    Get the stock list from database.

    Returns:
        The JSON string of the stock list.
    """
    database = TinyDB(STOCK_DATABASE)
    stocks = []
    for row in database.all():
        # Only return following 4 fields for the request.
        keep = ['id', 'pinyin', 'name', 'enname']
        filtered_stock_json = {key: row[key] for key in keep}
        stocks.append(filtered_stock_json)
    return json.dumps(stocks, ensure_ascii=False)

def get_history_and_predict_result(id: str, date: str) -> str:
    """
    Get the history prices and predicted price of the stock.

    Args:
        id: The id of the stock, which is a 6-digit number.
        date: The date when the request is sent. This will be used to infer the predicting date.

    Returns:
        A JSON string containing the history prices and the predicted price of the stock.
    """
    qlib.init(provider_uri='~/.qlib/qlib_data/cn_data')

    # Get the qlib_id from the database.
    database = TinyDB(STOCK_DATABASE)
    matched_rows = database.search(Query().id == id)
    if len(matched_rows) == 0:
        raise LookupError(f'No such id in database: {id}')
    qlib_id = matched_rows[0]['qlib_id']

    # Get history prices.
    recent_40_trading_days = qlib.data.D.calendar(start_time='2008-01-01', end_time=date)[-40:]
    history_data = qlib.data.D.features([qlib_id], ['$close/$factor'], recent_40_trading_days[0].strftime('%Y-%m-%d'), date)
    history = [{key[1].strftime('%Y-%m-%d'): round(value, 2)} for key, value in history_data.to_dict()['$close/$factor'].items()]

    # Get predicted price.
    latest_trading_date = qlib.data.D.calendar(start_time=(pd.Timestamp(date) - pd.Timedelta(days=20)).strftime("%Y-%m-%d"), end_time=date)[-1].strftime("%Y-%m-%d")
    predicted_trading_date = (pd.Timestamp(latest_trading_date) + pd.Timedelta(days=14)).strftime("%Y-%m-%d")
    predicted_price = None
    if matched_rows[0]['predict'] is not None and latest_trading_date in matched_rows[0]['predict']:
        predicted_price = round((1.0 + matched_rows[0]['predict'][latest_trading_date]) * history[-1][latest_trading_date], 2)

    # Create Stock object and convert it to json string
    stock = Stock(
        id,
        matched_rows[0]['pinyin'],
        matched_rows[0]['name'],
        qlib_id,
        enname=matched_rows[0]['enname'],
        history=history,
        predict={predicted_trading_date: predicted_price}
    )
    return stock.to_json(ensure_ascii=False)
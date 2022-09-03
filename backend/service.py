import json
import os
import pandas
import pypinyin
import qlib.data
from tinydb import TinyDB, Query

from stock import Stock


## Define the database file name here.
STOCK_DATABASE = os.path.expanduser("~") + '/.stock/stock.json'


def load_stock_list():
    """
    Load stock list from a csv file and insert the data into database.
    """
    os.makedirs(os.path.dirname(STOCK_DATABASE), exist_ok=True)
    database = TinyDB(STOCK_DATABASE)

    stock_list = pandas.read_csv(os.path.dirname(__file__) + '/stock_list.csv')
    for index, row in stock_list.iterrows():
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
        print(f'Updated stock {index}:', stock_json)
    
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
    qlib.init(provider_uri=os.path.expanduser("~") + '/.qlib/qlib_data/cn_data')

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
    stock = Stock(id, matched_rows[0]['pinyin'], matched_rows[0]['name'], qlib_id, enname=matched_rows[0]['enname'], history=history)

    # Get predicted price.
    # TODO: Get predicted price.

    return stock.to_json(ensure_ascii=False)
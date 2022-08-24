import json
import os
import pandas
import pypinyin
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

        # We need to translate the Chinese name of the stock to Pinyin and select the first Character of each word.
        # This will help users look up their stock rapidly.
        # TODO: Need to confirm if there are problems of heteronym.
        # TODO: English characters are dropped by the pypinyin library.
        pinyin_list = pypinyin.pinyin(name, style=pypinyin.NORMAL)
        pinyin_first_characters = []
        for word in pinyin_list:
            pinyin_first_characters.append(word[0][0].upper())
        pinyin = "".join(pinyin_first_characters)
        stock = Stock(id, pinyin, name, enname=enname)
        stock_json = stock.to_dict()
        query = Query()
        database.upsert(stock_json, query.id == stock.id)
        print(f'Updated stock {index}:', stock_json)
    
def get_stock_list() -> str:
    """
    Get the stock list from database.
    """
    database = TinyDB(STOCK_DATABASE)
    stocks = []
    for row in database.all():
        # Only return following 3 fields for the request.
        keep = ['id', 'pinyin', 'name']
        filtered_stock_json = {key: row[key] for key in keep}
        stocks.append(filtered_stock_json)
    return json.dumps(stocks, ensure_ascii=False)
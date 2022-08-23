from flask import Flask
import logging

import service


app = Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route('/')
def home():
    """
    Home page of this service.
    """
    return 'This is the homepage of stock prediction service.<p>Usages:<br>&emsp;<b>Get stock list:</b>&emsp;/stock/list'


@app.route('/stock/list')
def get_stock_list():
    """
    Get the stock list in the market.

    The format of the returned JSON should look like:
    [
        {
            "id": "600479",
            "pinyin": "QJYY",
            "name": "千金药业"
        },
        {
            "id": "600480",
            "pinyin": "LYGF",
            "name": "凌云股份"
        },
        {
            "id": "600481",
            "pinyin": "SLJN",
            "name": "双良节能"
        }
    ]

    Returns:
        A JSON string including all the stocks in the market.
    """
    return service.get_stock_list()

if __name__ == '__main__':
   app.run()
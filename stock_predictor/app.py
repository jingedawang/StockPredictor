import datetime
from flask import Flask
from flask_cors import CORS
import logging

import service


app = Flask(__name__)
CORS(app, resources=r'/*')
app.logger.setLevel(logging.INFO)


@app.route('/')
def home():
    """
    Home page of this service.
    """
    return 'This is the homepage of stock prediction service.<p>' \
        'Usages:<br>' \
        '&emsp;<b>Get stock list:</b>&emsp;/stock/list<br>' \
        '&emsp;<b>Predict:</b>&emsp;/stock/&lt;id&gt;<br>' \
        '&emsp;<b>Predict in date:</b>&emsp;/stock/&lt;id&gt;/&lt;yyyy-mm-dd&gt;'


@app.route('/stock/list')
def get_stock_list():
    """
    Get the stock list in the market.

    The format of the returned JSON should look like:
    [
        {
            "id": "000001",
            "pinyin": "PAYH",
            "name": "平安银行",
            "enname": "Ping An Bank Co., Ltd."
        },
        {
            "id": "000002",
            "pinyin": "WKA",
            "name": "万科A",
            "enname": "China Vanke Co.,Ltd."
        },
        {
            "id": "000004",
            "pinyin": "GNKJ",
            "name": "国农科技",
            "enname": "Shenzhen Cau Technology Co.,Ltd."
        }
    ]

    Returns:
        A JSON string including all the stocks in the market.
    """
    return service.get_stock_list()

@app.route('/stock/<id>')
def predict(id: str):
    """
    Predict the stock price after 2 weeks.

    The format of the returned JSON should look like:
    {
        "id": "600000",
        "pinyin": "PFYH",
        "name": "浦发银行",
        "qlib_id": "SH600000",
        "enname": "Shanghai Pudong Development Bank Co.,Ltd.",
        "history": [
            {
                "2022-09-06": 7.26
            },
            {
                "2022-09-07": 7.22
            },
            {
                "2022-09-08": 7.24
            },
            {
                "2022-09-09": 7.31
            }
        ],
        "predict": {
            "2022-09-23": 7.36
        }
    }

    Args:
        id: The id of the stock, which is a 6-digit number.

    Returns:
        The history prices and the predicted price for the stock.
    """
    # Check the input id.
    if not id.isdigit() or len(id) != 6:
        return f'Error parameter: {id} is not a valid stock id.'

    # Call service to fetch the history and prediction of today.
    today = datetime.date.today().strftime('%Y-%m-%d')
    try:
        result = service.get_history_and_predict_result(id, today)
    except LookupError:
        return f'Error parameter: Stock {id} is invalid or not supported yet.'
    return result

@app.route('/stock/<id>/<date>')
def predict_in_date(id: str, date: str):
    """
    Predict the stock price after 2 weeks from the specified date.

    The format of the returned JSON should look like:
    {
        "id": "600000",
        "pinyin": "PFYH",
        "name": "浦发银行",
        "qlib_id": "SH600000",
        "enname": "Shanghai Pudong Development Bank Co.,Ltd.",
        "history": [
            {
                "2022-04-26": 7.87
            },
            {
                "2022-04-27": 7.83
            },
            {
                "2022-04-28": 7.99
            },
            {
                "2022-04-29": 8.03
            }
        ],
        "predict": {
            "2022-05-13": 8.34
        }
    }

    Args:
        id: The id of the stock, which is a 6-digit number.
        date: The date when the predict request is sent. Should be in format 'YYYY-mm-dd'.

    Returns:
        The history prices and the predicted price for the stock at the specified date.
    """
    # Check the input id and date strings.
    if not id.isdigit() or len(id) != 6:
        return f'Error parameter: {id} is not a valid stock id.'
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return f'Error parameter: {date} is not a valid date.'

    # Call service to fetch the history and prediction for the given date.
    try:
        result = service.get_history_and_predict_result(id, date)
    except LookupError:
        return f'Error parameter: Stock {id} is invalid or not supported yet.'
    return result


if __name__ == '__main__':
   app.run(host='0.0.0.0')
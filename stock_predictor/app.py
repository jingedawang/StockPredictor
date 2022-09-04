import datetime
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
                "2022-08-30": 7.19
            },
            {
                "2022-08-31": 7.27
            },
            {
                "2022-09-01": 7.23
            },
            {
                "2022-09-02": 7.21
            }
        ],
        "predict": 7.33
    }

    Args:
        id: The id of the stock, which is a 6-digit number.

    Returns:
        The history prices and the predicted price for the stock.
    """
    today = datetime.date.today().strftime('%Y-%m-%d')
    return service.get_history_and_predict_result(id, today)

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
                "2020-05-07": 10.39
            },
            {
                "2020-05-08": 10.44
            },
            {
                "2020-05-11": 10.43
            },
            {
                "2020-05-12": 10.34
            }
        ],
        "predict": 10.21
    }

    Args:
        id: The id of the stock, which is a 6-digit number.
        date: The date when the predict request is sent. Should be in format 'YYYY-mm-dd'.

    Returns:
        The history prices and the predicted price for the stock at the specified date.
    """
    return service.get_history_and_predict_result(id, date)


if __name__ == '__main__':
   app.run(host='0.0.0.0')
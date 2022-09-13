import datetime

import service


if __name__ == '__main__':
    """
    Do today's prediction for all the stocks.
    """
    service.predict_all(date=datetime.date.today().strftime('%Y-%m-%d'))
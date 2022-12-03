import datetime

from service import Service


if __name__ == '__main__':
    """
    Do today's prediction for all the stocks.
    """
    service = Service()
    service.predict_all(date=datetime.date.today().strftime('%Y-%m-%d'))
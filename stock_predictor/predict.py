import pandas as pd
import qlib
import qlib.data
from qlib.data.dataset import DatasetH
from qlib.workflow import R

from data_handler import Alpha158TwoWeeks


def predict(id='all', start_date=None, end_date=None) -> pd.DataFrame:
    """
    Predict the after-two-weeks price of the given stock in the specific date range.

    Args:
        id: The qlib id of the stock. Default 'all' means predicting all the stocks.
        start_date: The beginning of the requested date range (inclusive).
        end_date: The end of the requested date range (inclusive).
    """
    # Reset the date to the latest trading date
    latest_trading_date = qlib.data.D.calendar(start_time=(pd.Timestamp(start_date) - pd.Timedelta(days=20)).strftime("%Y-%m-%d"), end_time=start_date)[-1]
    if latest_trading_date < pd.Timestamp(start_date):
        start_date = latest_trading_date.strftime("%Y-%m-%d")
    if end_date is None:
        end_date = start_date

    # Prepare the data used for inference.
    if id != 'all':
        id = [id]
    data_handler = Alpha158TwoWeeks(instruments=id)
    dataset = DatasetH(
        handler=data_handler,
        segments={
            "test": [start_date, end_date]
        }
    )

    # Start predicting with pre-trained model.
    with R.start(experiment_name="stock_predictor", recorder_name='predict'):
        model = R.get_recorder(recorder_name='two_weeks_model').load_object("model.pkl")
        pred = model.predict(dataset)
        return pred
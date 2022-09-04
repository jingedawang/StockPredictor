import pandas as pd
from qlib.data import D
from qlib.data.dataset import DatasetH
from qlib.workflow import R

from data_handler import Alpha158TwoWeeks


def predict(id: str, date: str) -> float:
    """
    Predict the after-two-weeks price of the given stock at the specific date.

    Args:
        id: The qlib id of the stock.
        date: The date when the prediction is made.
    """
    # Reset the date to the latest trading date
    latest_trading_date = D.calendar(start_time=(pd.Timestamp(date) - pd.Timedelta(days=20)).strftime("%Y-%m-%d"), end_time=date)[-1]
    if latest_trading_date < pd.Timestamp(date):
        date = latest_trading_date.strftime("%Y-%m-%d")

    # Prepare the data used for inference.
    data_handler = Alpha158TwoWeeks(instruments=[id])
    dataset = DatasetH(
        handler=data_handler,
        segments={
            "test": [date, date]
        }
    )

    # Start predicting with pre-trained model.
    with R.start(experiment_name="workflow"):
        model = R.get_recorder(recorder_id="cc9943bccdb2471eae81cde5a2be32ee").load_object("params.pkl")
        pred = model.predict(dataset)
        return round(pred[date, id], 2)
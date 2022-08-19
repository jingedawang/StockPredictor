import qlib
from qlib.constant import REG_CN
from qlib.data.dataset import DatasetH
from qlib.utils import init_instance_by_config, flatten_dict
from qlib.workflow import R
from qlib.tests.data import GetData
from qlib.tests.config import CSI300_GBDT_TASK

from stock_predictor.data_handler import Alpha158TwoWeeks


if __name__ == "__main__":

    # use default data
    provider_uri = "~/.qlib/qlib_data/cn_data"  # target_dir
    GetData().qlib_data(target_dir=provider_uri, region=REG_CN, exists_skip=True)
    qlib.init(provider_uri=provider_uri, region=REG_CN)

    # Load data with our customized data handler.
    # The Alpha158TwoWeeks is different with Alpha158 only in the labels.
    # TODO: Data is important for model training, we need to try other adjustments to the data handler to acheive better results.
    data_handler = Alpha158TwoWeeks(instruments='csi300')
    dataset = DatasetH(
        handler=data_handler,
        segments={
            "train": ["2008-01-01", "2014-12-31"],
            "valid": ["2015-01-01", "2016-12-31"],
            "test": ["2017-01-01", "2020-08-01"]
        }
    )

    # Use GBDT model.
    # TODO: Model architecture is also important. We need to try different models to acheive better results.
    model = init_instance_by_config(CSI300_GBDT_TASK["model"])

    # NOTE: This line is optional.
    # Show the prepared training data to make sure we are using the correct data for trainning.
    example_df = dataset.prepare("train")
    print(example_df.head())

    # start experiment.
    with R.start(experiment_name="workflow"):
        R.log_params(**flatten_dict(CSI300_GBDT_TASK))
        model.fit(dataset)
        R.save_objects(**{"params.pkl": model})

        pred = model.predict(dataset)
        print('pred', pred)

    # TODO: We need do backtest to evaluate our model.
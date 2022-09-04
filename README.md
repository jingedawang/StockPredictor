# StockPredictor
Predict the stock price with AI models.

This is the main repository of the [Stock Prediction](https://github.com/users/jingedawang/projects/2) project, which starts as an [internal project](https://hackbox.microsoft.com/project/597) in Microsoft Hackthon 2022.

## Background

Everyone loves stock. Everyone hates stock.

It's so hard to figure out which direction the price will go in next few weeks. If you are a technical analyst, you may be interested in leveraging AI to dig the potential pattern of a given stock.

MSRA has open-sourced a powerful tool for quantitative investment, which is called [Qlib](https://github.com/microsoft/qlib). We could try to use this framework to construct a useful service for our daily trading.

A simple scenario may like,

**Me**: Please tell me how much the stock xxx will rise at the end of the next 2 weeks?
<br>**Service**: It will decrease 8% from now till that time.
<br>**Me**: Oh shit, I will sell them!

## Quick Start

### Installation & Deployment
It's highly encouraged to use a virtual environment with Anaconda. We assume you are using a conda environment with Python 3.8.

Firstly, install Qlib and download trading data.
```bash
pip install numpy
pip install --upgrade cython
git clone https://github.com/microsoft/qlib.git && cd qlib
pip install .
python scripts/data_collector/yahoo/collector.py download_data --source_dir ~/.qlib/stock_data/source/cn_data --start 1999-01-01 --end 2022-12-31 --delay 1 --interval 1d --region CN
python scripts/data_collector/yahoo/collector.py normalize_data --source_dir ~/.qlib/stock_data/source/cn_data --normalize_dir ~/.qlib/stock_data/source/cn_1d_nor --region CN --interval 1d
python scripts/dump_bin.py dump_all --csv_path ~/.qlib/stock_data/source/cn_1d_nor --qlib_dir ~/.qlib/qlib_data/cn_data --freq day --exclude_fields date,symbol
```

Secondly, download this repository and load data.
```bash
git clone https://github.com/jingedawang/StockPredictor.git
pip install -r stock_predictor/requirements.txt
python stock_predictor/setup.py
```

Then, we need to train a prediction model, and do a full prediction for all the stocks in the market.
```bash
python stock_predictor/train_two_week_predictor.py
python stock_predictor/predict_all.py
```

Before starting the service, we need to setup a schedule to automatically update the data everyday after the market closing time.
```bash
crontab config/update_data.crontab
```

Finally we could start our prediction service.
```bash
python stock_predictor/app.py
```


### Web API

Once the prediction service started, you could send requests to the following methods.
Note that 20.205.61.210 is our public server address, we have deployed an app here already.
You could test the web API on your own machine and compare it with the public one.

#### API 1: Get stock list
```
Url: /stock/list
Parameter: None
Response: A JSON string.
Example for request http://20.205.61.210:5000/stock/list:
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
```
#### API 2: Predict
```
Url: /stock/<id>
Parameter: <id>: The id of the stock.
Response: A JSON string containing both history prices and predicted price.
Example for request http://20.205.61.210:5000/stock/600000:
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
```
#### API 3: Predict in specific date
```
Url: /stock/<id>/<date>
Parameter:
    <id>: The id of the stock.
    <date>: The date when performs the prediction.
Response: A JSON string containing both history prices and predicted price for the prediction.
Example for request http://20.205.61.210:5000/stock/600000/2020-05-12:
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
```

## Contribute

### What can I contribute?

It's always welcomed to join us as a developer. Please check [Stock Prediction](https://github.com/users/jingedawang/projects/2) project and see what you could do.

Currently, we are in Iteration Hachthon (8/15/2022 to 9/26/2022).
Our first goal is to develop an initial version of StockPredictor, which could tell us how much the price will be in the next two weeks.

If you don't like our development plan but have good ideas about this project, please create an issue.
We are happy to merge good implementations.

### Resources

If you are interested in stock prediction model, there are several resources. The first two should be read carefully.
The third one is the video records of AI school course which teaching the theories of stock models and how to use them.

+ Machine learning framework for stock: [microsoft/qlib](https://github.com/microsoft/qlib)
+ Documentation of Qlib: [Qlib Documentation](https://qlib.readthedocs.io/en/latest/index.html)
+ Course in AI School: [AI + Stock](https://microsoftapc-my.sharepoint.com/:f:/g/personal/jingewang_microsoft_com/EoHHzyc1dRJMvt-b1QgOBS8BENFA4ZXvMUpgnWukliyh1Q?e=4CwYaS)

### Overview

This directory includes the algorithm related code written in Python. Please follow the instructions below to setup your development environment and start writing code.

### Setup

Please install the Qlib library according to the official document here: https://qlib.readthedocs.io/en/latest/start/installation.html.

It's recommended to use Anaconda with Python 3.8 on Ubuntu 20.04.

Then, you should be able to run the script under this directory like
```
python train_two_week_predictor.py
```

This script will train a GBDT model with dataset sampled from 2008 to 2014. Then predict the after-two-weeks price for dataset sampled from 2016 to 2017.
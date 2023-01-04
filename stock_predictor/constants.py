from pathlib import Path


# Path of TinyDB database.
STOCK_DATABASE = Path('~/.stock/stock.json').expanduser()

# MongoDB connection string
MONGODB_CONNECTION_STRING = 'mongodb://localhost:27017'
# MongoDB database name
MONGODB_DATABASE_NAME = 'stock'
# MongoDB collection name
MONGODB_COLLECTION_NAME = 'stocks'

# Path of Shanghai stock list file.
SH_STOCK_LIST_PATH = Path('~/.stock/sh_stock_list.xls').expanduser()
# Path of Shenzhen stock list file.
SZ_STOCK_LIST_PATH = Path('~/.stock/sz_stock_list.xls').expanduser()
# URL of Shanghai stock list webpage.
SHANGHAI_STOCK_EXCHANGE_URL = 'http://www.sse.com.cn/assortment/stock/list/share/'
# URL of Shenzhen stock list webpage.
SHENZHEN_STOCK_EXCHANGE_URL = 'http://www.szse.cn/market/product/stock/list/index.html'

# The date we start to support predicting.
START_PREDICTING_DATE = '2022-01-01'

# Path of Qlib data.
QLIB_DATA_PATH = '~/.qlib/qlib_data/cn_data'
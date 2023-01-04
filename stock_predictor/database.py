import os
import pymongo
from typing import List, Optional
from tinydb import TinyDB, Query

import constants
from stock import Stock


class Database:
    """
    The universal database interface for stock predictor.

    This class simplifies the database operation to object level.
    """

    def __init__(self) -> None:
        """
        Initialize database.
        """
        pass

    def all(self) -> List[Stock]:
        """
        Get all the stocks in the database.
        """
        pass

    def search(self, id: str) -> Optional[Stock]:
        """
        Search a stock with given id.
        """
        pass

    def upsert(self, stock: Stock) -> None:
        """
        Update or insert the stock into database.

        The id field of stock will be used for lookup in the database.
        """
        pass

    def refresh(self) -> None:
        """
        Refresh the data in database.
        """
        pass

    def close(self) -> None:
        """
        Close the database and release resources.
        """
        pass


class TinyDatabase(Database):
    """
    TinyDB implementation of database.
    """

    def __init__(self) -> None:
        """
        Initialize TinyDB database object.
        """
        os.makedirs(os.path.dirname(constants.STOCK_DATABASE), exist_ok=True)
        self.database = TinyDB(constants.STOCK_DATABASE)
        self.query = Query()

    def all(self) -> List[Stock]:
        """
        Get all the stocks in the database.
        """
        return [Stock.from_dict(row) for row in self.database.all()]

    def search(self, id: str) -> Optional[Stock]:
        """
        Search a stock with given id.
        """
        matched_rows = self.database.search(Query().id == id)
        if len(matched_rows) == 1:
            return Stock.from_dict(matched_rows[0])
        elif len(matched_rows) > 1:
            raise ValueError(f'Multiple rows with the same id {id}')
        else:
            return None

    def upsert(self, stock: Stock) -> None:
        """
        Update or insert the stock into database.

        The id field of stock will be used for lookup in the database.
        """
        stock_dict = {key: value for key, value in stock.to_dict().items() if value is not None}
        self.database.upsert(stock_dict, self.query.id == stock.id)

    def refresh(self) -> None:
        """
        Refresh the data by clearing the cache.

        The cache is not updated if the data is modified by another process.
        So we need to call this method manually.
        """
        self.database.clear_cache()

    def close(self) -> None:
        """
        Close the database and release resources.
        """
        self.database.close()


class MongoDatabase(Database):
    """
    MongoDB implementation of database.
    """

    def __init__(self) -> None:
        """
        Create MongoDB client and connect to MongoDB server. Get the database and collections for stock data.
        """
        self.client = pymongo.MongoClient(constants.MONGODB_CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        self.database = self.client.get_database(constants.MONGODB_DATABASE_NAME)
        self.collection = self.database.get_collection(constants.MONGODB_COLLECTION_NAME)

    def all(self) -> List[Stock]:
        """
        Get all the stocks in the database.
        """
        rows = self.collection.find()
        return [Stock.from_dict(row) for row in rows]

    def search(self, id: str) -> Optional[Stock]:
        """
        Search a stock with given id.
        """
        matched_row = self.collection.find_one({'id': id})
        if matched_row is not None:
            return Stock.from_dict(matched_row)
        else:
            return None

    def upsert(self, stock: Stock) -> None:
        """
        Update or insert the stock into database.

        The id field of stock will be used for lookup in the database.
        """
        stock_dict = {key: value for key, value in stock.to_dict().items() if value is not None}
        self.collection.update_one(
            {'id': stock.id},
            {'$set': stock_dict},
            upsert=True
        )

    def refresh(self) -> None:
        """
        Do nothing. MongoDB don't need to refresh.
        """
        pass

    def close(self) -> None:
        """
        Close the database and release resources.
        """
        self.client.close()
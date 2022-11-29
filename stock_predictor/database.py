import os
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
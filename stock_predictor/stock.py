from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Dict, List, Optional


@dataclass_json()
@dataclass
class Stock:
    """Stock entity class.
    
    Args:
        id (str): The unique id of the stock in market.
        pinyin (str): The first characters of the pinyin of the stock name.
        name (float): The Chinese name of the stock.
        qlib_id (str): The id of the stock used in Qlib data.
        enname (str): The English name of the stock.
        history (List[Dict]): The history prices of the stock. Each item is a key value pair of date and price.
        predict (Dict): The predicted price for the stock.
        delisted (bool): `True` if the stock has already been delisted, `False` otherwise.
        listing_date (str): The listing date of the stock.
        delisted_date (str): The delisted date of the stock.
    """
    id: str
    pinyin: str
    name: str
    qlib_id: str
    enname: Optional[str] = None
    history: Optional[List[Dict[str, float]]] = None
    predict: Optional[Dict[str, float]] = None
    delisted: bool = False
    listing_date: Optional[str] = None
    delisted_date: Optional[str] = None
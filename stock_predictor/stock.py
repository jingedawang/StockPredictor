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
        history (List[Dict]): The history prices of the stock. Each item is a key value pair of date and price.
        predict (Dict): The predicted price for the stock.
    """
    id: str
    pinyin: str
    name: str
    qlib_id: str
    enname: Optional[str] = None
    history: Optional[List[Dict[str, float]]] = None
    predict: Optional[Dict[str, float]] = None
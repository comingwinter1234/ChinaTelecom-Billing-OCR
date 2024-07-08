from typing import Union, Tuple
from datetime import date
from pydantic import BaseModel


class SearchServiceInfo(BaseModel):
    service_name: Union[str, None] = None
    service_money: Union[Tuple[float, float], None] = None
    seller_company: Union[str, None] = None
    service_time: Union[Tuple[date, date], None] = None

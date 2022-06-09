from typing import List, Optional, Union

from pydantic import BaseModel # 객체 타입설정


class User(BaseModel):
    email: str = None
    name: str= None
    nickname: str= None
    img_url: str= None
    token: str= None

class Review(BaseModel):
    market_id: str= None
    rate: int= None
    comment : str= None
    solution : str= None

class Market(BaseModel):
    market_name: str= None
    market_latitude : float= None
    market_longitude : float= None
    phone : str= None
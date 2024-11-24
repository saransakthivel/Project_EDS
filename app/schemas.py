from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InsEdsDataModel(BaseModel):
    d_name: str
    d_value: float
    date_time : datetime
    
    class Config:
        orm_mode = True
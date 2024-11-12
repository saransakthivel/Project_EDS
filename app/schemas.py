from pydantic import BaseModel
from typing import Optional

class InsEdsDataModel(BaseModel):
    d_name: str
    d_value: float

class InsEdsData(InsEdsDataModel):
    id: int

    class Config:
        from_attributes = True
        
    
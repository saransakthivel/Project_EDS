from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Time
from .database import Base

class ValuesData(Base):
    __tablename__ = "EDSdata"

    id = Column(Integer, primary_key=True, index=True)
    d_name = Column(String(100), index=True)
    d_value = Column(Float)
    date_time = Column(DateTime)
    date = Column(Date)
    time = Column(Time)

from sqlalchemy import Column, String, Float, Date, DateTime, Time
from .database import Base
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

class EDSdata(Base):
    __tablename__ = "EDSdata"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, index=True)
    d_name = Column(String(100), index=True)
    d_value = Column(Float)
    date_time = Column(DateTime)
    date = Column(Date)
    time = Column(Time)

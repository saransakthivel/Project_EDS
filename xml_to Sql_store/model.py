# models.py
from sqlalchemy import Column, Integer, Float, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EDSdata(Base):
    __tablename__ = 'EDSdata'  # Table name

    d_name = Column(String, primary_key=True)
    d_value = Column(Float)
    date = Column(Date)
    time = Column(Time)

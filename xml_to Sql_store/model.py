# models.py
from sqlalchemy import Column, Integer, Float, String, Date, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid

Base = declarative_base()

class EDSdata(Base):
    __tablename__ = 'CasData'  # Table name

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    d_name = Column(String)
    d_value = Column(Float)
    date_time = Column(DateTime)
    date = Column(Date)
    time = Column(Time)

class TechEdsData(Base):
    __tablename__ = 'TechData'

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    d_name = Column(String)
    d_value = Column(Float)
    date_time = Column(DateTime)
    date = Column(Date)
    time = Column(Time)

class CTHEdsData(Base):
    __tablename__ = 'CTHData'

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    d_name = Column(String)
    d_value = Column(Float)
    date_time = Column(DateTime)
    date = Column(Date)
    time = Column(Time)

class ITEdsData(Base):
    __tablename__ = 'ITData'

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    d_name = Column(String)
    d_value = Column(Float)
    date_time = Column(DateTime)
    date = Column(Date)
    time = Column(Time)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

CONNECTION_STRING="mssql+pyodbc://sa:RPSsql12345@localhost:1433/CASeds?driver=ODBC+Driver+17+for+SQL+Server"

engine=create_engine(CONNECTION_STRING)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()
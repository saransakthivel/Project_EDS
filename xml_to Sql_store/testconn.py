from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mssql+pyodbc://sa:RPSsql12345@localhost:1433/PSGedsData?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database Connection Successfull Result:",result.scalar())
except Exception as e:
    print("Error while Connecting to database:",e)
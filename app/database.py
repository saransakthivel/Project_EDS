from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, text

CONNECTION_STRING="mssql+pyodbc://sa:RPSsql12345@45.127.108.208:1433/PSGedsData?driver=ODBC+Driver+17+for+SQL+Server"

engine=create_engine(CONNECTION_STRING)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

# try:
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT 1"))
#         print("Database Connected Successfully, Result: ", result.scalar())
# except Exception as e:
#     print("Error while connecting to database: ",e)
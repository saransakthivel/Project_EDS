from app.database import Base, engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

try:
    Base.metadata.create_all(bind=engine)
    print("Table Created Successfully")
except Exception as e:
    print(f'Error Creating table {e}')

# def create_table():
#     create_table_query = text("""
#     CREATE TABLE EDSdata (
#         id INT PRIMARY KEY IDENTITY(1,1),
#         d_name VARCHAR(255),
#         value FLOAT
#     )
#     """)
#     try:
#         with engine.connect() as connection:
#             # Execute the query using the connection
#             connection.execute(create_table_query)
#             connection.commit()
#             print("Table created successfully!")
#     except Exception as e:
#         print(f"Error creating table: {e}")

#     print(engine.url)

# create_table()

# try:
#     with engine.connect() as connection:
#         print("Connection successful!")
# except OperationalError as e:
#     print(f"Connection failed: {e}")

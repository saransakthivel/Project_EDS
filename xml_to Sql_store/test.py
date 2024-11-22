import pytz
import requests
from sqlalchemy import create_engine, Column, Integer, Float, String, Date, Time
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import xml.etree.ElementTree as ET

# Database configuration
DATABASE_URL = "mssql+pyodbc://sa:RPSsql12345@localhost:1433/CASeds?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the EDSdata table
class EDSdata(Base):
    __tablename__ = "EDSdata"
    id = Column(Integer, primary_key=True, index=True)
    d_name = Column(String, nullable=False)
    d_value = Column(Float, nullable=False)
    date_time = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

Base.metadata.create_all(bind=engine)

# URLs file
URLS_FILE = "urls.txt"

# Function to test the complete workflow
def test_workflow():
    # Step 1: Extract URLs
    try:
        with open(URLS_FILE, "r") as file:
            urls = [line.strip() for line in file if line.strip()]
            print("Extracted URLs:", urls)
    except Exception as e:
        print(f"Error reading URLs from {URLS_FILE}: {e}")
        return

    # Step 2: Fetch and parse XML for each URL
    for url in urls:
        try:
            print(f"\nFetching data from URL: {url}")
            response = requests.get(url)
            if response.status_code == 200:
                print("Success: Fetched data from URL.")
                print("XML Content Preview:", response.text[:500])  # Print first 500 chars of XML
                root = ET.fromstring(response.content)
                print("XML Parsed Successfully.")

                # Step 3: Extract data from XML
                variable_elements = root.findall(".//variable")
                if variable_elements:
                    print(f"Found {len(variable_elements)} <variable> elements.")
                    for variable_element in variable_elements:
                        d_name_element = variable_element.find("id")
                        d_value_element = variable_element.find("value")

                        if d_name_element is not None and d_value_element is not None:
                            d_name = d_name_element.text
                            d_value = float(d_value_element.text)

                            now_ist = datetime.now(pytz.timezone("Asia/Kolkata"))
                            date_time_str = now_ist.strftime("%Y-%m-%d %H:%M:%S")
                            date_str = now_ist.date()
                            time_str = now_ist.time()

                            print(f"Extracted Data - ID: {d_name}, Value: {d_value}, DateTime: {date_time_str}")

                            # Step 4: Store data in the database
                            db = SessionLocal()
                            try:
                                eds_data = EDSdata(
                                    d_name=d_name,
                                    d_value=d_value,
                                    date_time=date_time_str,
                                    date=date_str,
                                    time=time_str,
                                )
                                db.add(eds_data)
                                db.commit()
                                print("Data stored successfully in the database.")
                            except Exception as db_error:
                                print(f"Error inserting data into database: {db_error}")
                            finally:
                                db.close()
                        else:
                            print("Error: 'id' or 'value' not found in <variable>")
                else:
                    print("Error: No <variable> elements found in XML.")
            else:
                print(f"Failed to fetch URL. Status code: {response.status_code}")
        except Exception as fetch_error:
            print(f"Error fetching or processing URL: {fetch_error}")

# Run the workflow test
if __name__ == "__main__":
    test_workflow()

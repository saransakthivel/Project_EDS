import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import xml.etree.ElementTree as ET
from sqlalchemy.orm import Session
from model import EDSdata
import pytz
import time

DATABASE_URL = "mssql+pyodbc://sa:RPSsql12345@localhost:1433/CASeds?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

xml_url = "http://192.168.29.247/services/user/values.xml?var=Second%20Floor.API"
fetch_interval = 0.5  # seconds

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fetchAndStore_XmlData():

    db = SessionLocal()
    try:
        response = requests.get(xml_url)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            variable_element = root.find(".//variable")

            if variable_element is not None:
                d_name_element = variable_element.find("id")
                d_value_element = variable_element.find("value")

                if d_name_element is not None and d_value_element is not None:
                    d_name = d_name_element.text
                    d_value = float(d_value_element.text)

                    now_ist = datetime.now(pytz.timezone("Asia/Kolkata"))
                    date_str = now_ist.date()
                    time_str = now_ist.time()

                    eds_data = EDSdata(d_name=d_name, d_value=d_value, date=date_str, time=time_str)

                    print(f"Fetched Data - ID: {d_name}, Value: {d_value}, Date: {date_str}, Time: {time_str}")

                    db.add(eds_data)
                    db.commit()

                    print("Data stored successfully")
                else:
                    print("Error: 'id' or 'value' not found in <variable>")
            else:
                print("Error: No <variable> element found in XML")
        else:
            print(f"Failed to fetch XML data. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(fetchAndStore_XmlData, trigger="interval", seconds=fetch_interval)

def start_service():
    scheduler.start()
    print("XML data fetching service started.")
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down the service")
        scheduler.shutdown()

if __name__ == "__main__":
    try:
        start_service()
    except Exception as e:
        print("An error occurred while starting the service:", e)

import pytz
import time
import requests
import win32serviceutil
import win32service
import win32event
import servicemanager
import win32timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import xml.etree.ElementTree as ET
from model import EDSdata

DATABASE_URL = "mssql+pyodbc://sa:RPSsql12345@localhost:1433/CASeds?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
url_file = "urls.txt"
fetch_interval = 10  # seconds

class EdsToSqlService(win32serviceutil.ServiceFramework):
    _svc_name_ = "EDSDataFetchService"
    _svc_display_name_ = "EDS Data Fetch Service"
    _svc_description_ = "Fetches EDS Data and Stores in SQL Database"
    
    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.scheduler = BackgroundScheduler()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        try:
            self.scheduler.shutdown()
        except Exception as e:
            servicemanager.LogErrorMsg(f"Scheduler shutdown error: {e}")

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.scheduler.add_job(self.fetchAndStore_XmlData, 'interval', seconds=fetch_interval, max_instances=1)
        self.scheduler.start()
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

    def fetchAndStore_XmlData(self):
        db = SessionLocal()
        try:
            with open("urls.txt", "r") as file:
                urls = [line.strip() for line in file if line.strip()]
                print("Extracted URLs:", urls)
            
            for url in urls:
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        root = ET.fromstring(response.content)
                        variable_elements = root.findall(".//variable")
                
                        if variable_elements:
                            for variable_element in variable_elements:
                                d_name_element = variable_element.find("id")
                                d_value_element = variable_element.find("value")

                                if d_name_element is not None and d_value_element is not None:
                                    d_name = d_name_element.text
                                    d_value = float(d_value_element.text)

                                    now_ist = datetime.now(pytz.timezone("Asia/Kolkata"))
                                    dateTime_str = now_ist.strftime("%Y-%m-%d %H:%M:%S")
                                    date_str = now_ist.date()
                                    time_str = now_ist.time().strftime("%H:%M:%S")

                                    eds_data = EDSdata(d_name=d_name, d_value=d_value, date_time=dateTime_str, date=date_str, time=time_str)
                                    print(f"Fetched Data - ID: {d_name}, Value: {d_value}, DateTime: {dateTime_str}")

                                    db.add(eds_data)
                                    db.commit()
                                    print("Data stored successfully")
                                else:
                                    print("Error: 'id' or 'value' not found in <variable>")
                        else:
                            print("Error: No <variable> elements found in XML")
                    else:
                        print(f"Failed to fetch XML data from {url}. Status code: {response.status_code}")
                except Exception as e:
                    print(f"Error fetching data from {url}: {e}")
        except Exception as e:
            print(f"Error reading URLs or processing data: {e}")
        finally:
            db.close()

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(EdsToSqlService)

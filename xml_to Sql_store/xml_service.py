import os
import pytz
import logging
from logging.handlers import RotatingFileHandler
import time
import requests
import win32serviceutil
import win32service
import win32event
import servicemanager
from sqlalchemy import create_engine
from datetime import timedelta
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import xml.etree.ElementTree as ET
from model import EDSdata, TechEdsData, CTHEdsData, ITEdsData

DATABASE_URL = "mssql+pyodbc://sa:RPSsql12345@localhost:1433/PSGedsData?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

script_dir=os.path.abspath(os.path.dirname(__file__))
url_file = os.path.join(script_dir, "urls.txt")
tech_url_file = os.path.join(script_dir, "tech_urls.txt")
it_url_file = os.path.join(script_dir, "it_urls.txt")
fetch_interval = 10  # seconds

# logging.basicConfig(
#     filename="C:\\xml_to Sql_store\\service_debug.log",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     encoding="utf-8",
#     force=True
# )

logging.basicConfig(level=logging.INFO)

log_directory = "C:\\Users\\admin\\OneDrive - E 4 Energy Solutions\\Saturn Pyro Files\\Documents\\Project EDS\\xml_to Sql_store\\logs"

# log_directory = "C:\\xml_to Sql_store\\logs"
log_file = os.path.join(log_directory, "service_debug.log")

os.makedirs(log_directory, exist_ok=True)

log_handler = RotatingFileHandler(
    log_file, maxBytes=1 * 1024 * 2024, backupCount=5, encoding="utf-8"
)
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_handler.setFormatter(log_formatter)

logging.getLogger().addHandler(log_handler)

logging.info("program started.")

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
            logging.error(f"Scheduler shutdown error: {e}")

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        try:
            self.scheduler.add_job(self.fetchAndStore_XmlData, 'interval', seconds=fetch_interval, max_instances=1)
            logging.info("Job scheduled: fetchAndStore_XmlData every %s seconds", fetch_interval)
            
            self.scheduler.add_job(self.fetchAndStore_TechXmlData, 'interval', seconds=fetch_interval, max_instances=1)
            logging.info("Job scheduled: fetchAndStore_TechXmlData every %s seconds", fetch_interval)
            
            self.scheduler.add_job(self.fetchAndStore_CTHXmlData, 'interval', seconds=fetch_interval, max_instances=1)
            logging.info("Job scheduled: fetchAndStore_CTHXmlData every %s seconds", fetch_interval)

            self.scheduler.add_job(self.fetchAndStore_ITXmlData, 'interval', seconds=fetch_interval, max_instances=1)
            logging.info("Job scheduled: fetchAndStore_CTHXmlData every %s seconds", fetch_interval)

            self.scheduler.add_job(delete_old_data, 'interval', minutes=5, max_instances=1)
            logging.info("job scheduled: delete_old_data every 5 minutes")

            self.scheduler.start()
            logging.info("Scheduler started successfully.")
        except Exception as e:
            logging.error(f"Error starting scheduler: {e}")
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

    def fetchAndStore_XmlData(self):
        db = SessionLocal()
        try:
            with open(url_file, "r") as file:
                urls = [line.strip() for line in file if line.strip()]
                logging.info(f"Extracted URLs: {urls}")

            now_ist = datetime.now(pytz.timezone("Asia/Kolkata")) 
            dateTime_str = now_ist.strftime("%Y-%m-%d %H:%M:%S")
            date_str = now_ist.date()
            time_str = now_ist.time().strftime("%H:%M:%S")

            logging.info(f"Timestamp for this fetch cycle: {dateTime_str}")

            for url in urls:
                try:
                    logging.info(f"Fetching data from {url}")
                    response = requests.get(url)
                    if response.status_code == 200:
                        root = ET.fromstring(response.content)
                        variable_elements = root.findall(".//variable")
                        for variable_element in variable_elements:
                            d_name = variable_element.find("id").text
                            d_value = float(variable_element.find("value").text)

                            data_record = EDSdata(
                                d_name=d_name, 
                                d_value=d_value, 
                                date_time=dateTime_str, 
                                date=date_str, 
                                time=time_str
                            )
                            #logging.info(f"Fetched Data - ID: {d_name}, Value: {d_value}, DateTime: {dateTime_str}")

                            try:
                                db.add(data_record)
                                db.commit()
                                logging.info("CAS Data stored successfully. Total recodrds: {len(data_rec)}")
                            except Exception as db_error:
                                db.rollback()
                                logging.error(f"Error storing data in database: {db_error}")
                    else:
                        logging.error(f"Failed to fetch XML data from {url}. Status code: {response.status_code}")
                except Exception as e:
                    logging.error(f"Error fetching data from {url}: {e}")
        except Exception as e:
            logging.error(f"Error reading URLs or processing data: {e}")
        finally:
            db.close()

    def fetchAndStore_TechXmlData(self):
        db = SessionLocal()
        try:
            with open(tech_url_file, 'r') as file:
                urls = [line.strip() for line in file if line.strip()]
                logging.info(f"Extracted Tech URLs: {urls}")

            now_ist = datetime.now(pytz.timezone("Asia/Kolkata"))
            dateTime_str = now_ist.strftime("%Y-%m-%d %H:%M:%S")
            date_str = now_ist.date()
            time_str = now_ist.time().strftime("%H:%M:%S")
        
            logging.info(f"Timestamp for Tech fetch cycle: {dateTime_str}")

            for url in urls:
                try:
                    logging.info(f"Fetching data from {url}")
                    response = requests.get(url)
                    if response.status_code == 200:
                        root = ET.fromstring(response.content)
                        variable_elements = root.findall(".//variable")
                        data_records = []
                        for variable_element in variable_elements:
                            d_name = variable_element.find("id").text
                            d_value = float(variable_element.find("value").text)

                            data_record=TechEdsData(
                                d_name=d_name, 
                                d_value=d_value, 
                                date_time=dateTime_str, 
                                date=date_str, 
                                time=time_str
                            )
                            #logging.info(f"Fetched Tech Data - ID: {d_name}, Value: {d_value}, DateTime: {dateTime_str}")

                            try:
                                db.add(data_record)
                                db.commit()
                                logging.info("Tech Data stored successfully. Total records: {len(data_records)}")
                            except Exception as db_error:
                                db.rollback()
                                logging.error(f"Error storing data in database: {db_error}")
                    else:
                        logging.error(f"Failed to fetch Tech XML data from {url}. Status code: {response.status_code}")
                except Exception as e:
                    logging.error(f"Error fetching Tech data from {url}: {e}")
        except Exception as e:
            logging.error(f"Error reading Tech URLs or processing Tech data: {e}")
        finally:
            db.close()

    def fetchAndStore_CTHXmlData(self):
        db = SessionLocal()
        try:
            with open(tech_url_file, 'r') as file:
                urls = [line.strip() for line in file if line.strip()]
                logging.info(f"Extracted Tech URLs: {urls}")

            now_ist = datetime.now(pytz.timezone("Asia/Kolkata"))
            dateTime_str = now_ist.strftime("%Y-%m-%d %H:%M:%S")
            date_str = now_ist.date()
            time_str = now_ist.time().strftime("%H:%M:%S")
        
            logging.info(f"Timestamp for Tech fetch cycle: {dateTime_str}")

            for url in urls:
                try:
                    logging.info(f"Fetching data from {url}")
                    response = requests.get(url)
                    if response.status_code == 200:
                        root = ET.fromstring(response.content)
                        variable_elements = root.findall(".//variable")
                        data_records = []
                        for variable_element in variable_elements:
                            d_name = variable_element.find("id").text
                            d_value = float(variable_element.find("value").text)

                            data_record=CTHEdsData(
                                d_name=d_name, 
                                d_value=d_value, 
                                date_time=dateTime_str, 
                                date=date_str, 
                                time=time_str
                            )
                            #logging.info(f"Fetched Tech Hostel Data - ID: {d_name}, Value: {d_value}, DateTime: {dateTime_str}")

                            try:
                                db.add(data_record)
                                db.commit()
                                logging.info("Tech Hostel Data stored successfully. Total records: {len(data_records)}")
                            except Exception as db_error:
                                db.rollback()
                                logging.error(f"Error storing data in database: {db_error}")
                    else:
                        logging.error(f"Failed to fetch Tech Hostel XML data from {url}. Status code: {response.status_code}")
                except Exception as e:
                    logging.error(f"Error fetching Tech Hostel data from {url}: {e}")
        except Exception as e:
            logging.error(f"Error reading Tech URLs or processing Tech data: {e}")
        finally:
            db.close()

    def fetchAndStore_ITXmlData(self):
        db = SessionLocal()
        try:
            with open(it_url_file, 'r') as file:
                urls = [line.strip() for line in file if line.strip()]
                logging.info(f"Extracted Tech URLs: {urls}")

            now_ist = datetime.now(pytz.timezone("Asia/Kolkata"))
            dateTime_str = now_ist.strftime("%Y-%m-%d %H:%M:%S")
            date_str = now_ist.date()
            time_str = now_ist.time().strftime("%H:%M:%S")
        
            logging.info(f"Timestamp for Tech fetch cycle: {dateTime_str}")

            for url in urls:
                try:
                    logging.info(f"Fetching data from {url}")
                    response = requests.get(url)
                    if response.status_code == 200:
                        root = ET.fromstring(response.content)
                        variable_elements = root.findall(".//variable")
                        data_records = []
                        for variable_element in variable_elements:
                            d_name = variable_element.find("id").text
                            d_value = float(variable_element.find("value").text)

                            data_record=ITEdsData(
                                d_name=d_name, 
                                d_value=d_value, 
                                date_time=dateTime_str, 
                                date=date_str, 
                                time=time_str
                            )
                            #logging.info(f"Fetched Tech Hostel Data - ID: {d_name}, Value: {d_value}, DateTime: {dateTime_str}")

                            try:
                                db.add(data_record)
                                db.commit()
                                logging.info("Tech Hostel Data stored successfully. Total records: {len(data_records)}")
                            except Exception as db_error:
                                db.rollback()
                                logging.error(f"Error storing data in database: {db_error}")
                    else:
                        logging.error(f"Failed to fetch Tech Hostel XML data from {url}. Status code: {response.status_code}")
                except Exception as e:
                    logging.error(f"Error fetching Tech Hostel data from {url}: {e}")
        except Exception as e:
            logging.error(f"Error reading Tech URLs or processing Tech data: {e}")
        finally:
            db.close()

def delete_old_data():
    db=SessionLocal()
    try:
        now_ist = datetime.now(pytz.timezone("Asia/Kolkata"))
        Timestamp_pastminute_ago = now_ist - timedelta(minutes=1)

        formatted_timestamp = Timestamp_pastminute_ago.strftime("%Y-%m-%d %H:%M:%S")

        db.query(EDSdata).filter(EDSdata.date_time < formatted_timestamp).delete(synchronize_session=False)
        db.query(TechEdsData).filter(TechEdsData.date_time < formatted_timestamp).delete(synchronize_session=False)
        db.query(CTHEdsData).filter(CTHEdsData.date_time < formatted_timestamp).delete(synchronize_session=False)
        db.query(ITEdsData).filter(ITEdsData.date_time < formatted_timestamp).delete(synchronize_session=False)

        db.commit()
        logging.info(f"Old data older than {formatted_timestamp} fas been deleted successfully.")
    except Exception as e:
        db.rollback()
        logging.error(f"Error while deleting old data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(EdsToSqlService)

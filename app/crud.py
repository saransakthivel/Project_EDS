from sqlalchemy.orm import session
from .import models, schemas
import requests
import xml.etree.ElementTree as ET
from sqlalchemy import desc


# def ins_d_data(db: session, eds_data: schemas.InsEdsDataModel):
#     db_casEDS = models.ValuesData(**eds_data.model_dump())
#     db.add(db_casEDS)
#     db.commit()
#     db.refresh(db_casEDS)
#     return db_casEDS

def get_latest_data(db : session, d_name: str):
    return db.query(models.EDSdata).filter(models.EDSdata.d_name == d_name).order_by(desc(models.EDSdata.date_time)).first()


# def get_d_data(db: session, skip: int=0, limit: int=10):
#     return db.query(models.ValuesData).order_by(models.ValuesData.id).offset(skip).limit(limit).all()




# def fetch_xml_data_toSql(db: session):
#     #xml_url = "http://103.196.31.6/services/user/values.xml?var=F-01%20EB%20Incomer.AE"
#     #xml_url = "http://192.168.29.247/services/user/values.xml?var=Ground%20Floor.AE"
#     xml_url = "http://192.168.29.247/services/user/values.xml?var=Ground%20Floor.API"

#     response =  requests.get(xml_url)

#     if response.status_code == 200:

#         root = ET.fromstring(response.content)

#         variable_element = root.find(".//variable")

#         if variable_element is not None:
#             d_name_element = variable_element.find("id")
#             d_value_element = variable_element.find("value")

#             if d_name_element is not None and d_value_element is not None:
#                 d_name = d_name_element.text
#                 d_value = float(d_value_element.text)

#                 eds_data = schemas.InsEdsDataModel(d_name=d_name,d_value=d_value)
#                 return ins_d_data(db=db, eds_data=eds_data)
#             else:
#                return {"error" : "Required tags 'id' or 'value' not found in <variable>"}
#         else:
#             return {"error" : "No <variable> element found in XML"}
#     else:
#          return {"error" : "failed to fetch xml data", "status_code" : response.status_code}


from sqlalchemy.orm import session
from .import models, schemas, crud
import requests
import xml.etree.ElementTree as ET

def ins_d_data(db: session, eds_data: schemas.InsEdsDataModel):
    db_casEDS = models.ValuesData(**eds_data.model_dump())
    db.add(db_casEDS)
    db.commit()
    db.refresh(db_casEDS)
    return db_casEDS

def get_d_data(db: session, skip: int=0, limit: int=10):
    return db.query(models.ValuesData).order_by(models.ValuesData.id).offset(skip).limit(limit).all()

def fetch_xml_data_toSql(db: session):
    xml_url = "http://103.196.31.6/services/user/values.xml?var=F-01%20EB%20Incomer.AE"

    response =  requests.get(xml_url)

    if response.status_code == 200:

        root = ET.fromstring(response.content)

        d_name_element = root.find("id")
        d_value_element = root.find("value")

        if d_name_element is None or d_value_element is None:
            return {"error": "Required Elements Not Found"}
        else:
            d_name = d_name_element.text
            d_value = float(d_value_element.text)

            eds_data = schemas.InsEdsDataModel(d_name=d_name,d_value=d_value)

        return ins_d_data(db, eds_data)
    else:
        return {"error" : "failed to fetch xml data", "status_code" : response.status_code}


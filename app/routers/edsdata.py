from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import schemas, crud
from typing import List
from ..models import EDSdata

router = APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/insEds/",response_model=schemas.InsEdsData)
# def insert_edsData(edsData: schemas.InsEdsDataModel, db:Session = Depends(get_db)):
#     return crud.ins_d_data(db=db, eds_data=edsData)

@router.get("/data/", response_model=schemas.InsEdsDataModel)
def get_edsData(d_name: str, db: Session = Depends(get_db)):
    data = (
        db.query(EDSdata)
        .filter(EDSdata.d_name == d_name)
        .order_by(EDSdata.date_time.desc())
        .first()
    )
    if not data:
        raise HTTPException(status_code=404, detail="No data found for the device")
    return {
        "id" : str(data.id),
        "d_name" : data.d_name,
        "d_value" : data.d_value,
        "date_time" : data.date_time
    }
# @router.get("/fxml/")
# def fetch_and_storeXml(db: Session = Depends(get_db)):
#     result = crud.fetch_xml_data_toSql(db=db)
#     if hasattr(result, 'error') and result.error:
#         raise HTTPException(status_code=500, detail=result.error)
#     return result

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import schemas, crud

router = APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/insEds/",response_model=schemas.InsEdsData)
def insert_edsData(edsData: schemas.InsEdsDataModel, db:Session = Depends(get_db)):
    return crud.ins_d_data(db=db, eds_data=edsData)

@router.get("/insEds/")
def read_edsData(skip: int=0, limit: int=10, db:Session = Depends(get_db)):
    return crud.get_d_data(db=db, skip=skip, limit=limit)

@router.get("/fxml/")
def fetch_and_storeXml(db: Session = Depends(get_db)):
    result =  crud.fetch_xml_data_toSql(db=db)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
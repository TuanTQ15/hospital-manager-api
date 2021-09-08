from fastapi import APIRouter, Depends
from core.schema import schemas as sm
from core.model.database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..repository import medicalrecord

router = APIRouter(prefix="/api/medicalrecords", tags=['Medical Record'])


@router.get('/{CMND}', response_model=List[sm.MedicalRecordModel])
def get_all_medical_history(CMND,db: Session = Depends(get_db)):
    return medicalrecord.get_all_medical_record(db,CMND)

@router.get('/payment/{CMND}',response_model=List[sm.MedicalRecordShow])
def get_all_medical_history(CMND,db: Session = Depends(get_db)):
    return medicalrecord.get_medical_record(db,CMND)
from fastapi import APIRouter, Depends, status
from core.schema.schemas import PatientShow, Patient,PatientLogin
from core.model.models import PatientModel
from core.model.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from ..repository import payment

now = datetime.now()
router = APIRouter(prefix="/api/patients", tags=['Patient'])


@router.get('/payment/{CMND}')
def get_hospital_fee(CMND,db: Session = Depends(get_db)):
    return payment.get_hospital_fee(CMND,db)

@router.post('/payment/{MABA}')
def create_receiptment(maBA,db: Session = Depends(get_db)):
    return payment.create_receiptment(maBA,db)

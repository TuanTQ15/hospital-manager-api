from fastapi import APIRouter, Depends, status
from core.schema.schemas import ReceiptModel
from core.model.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from ..repository import payment

now = datetime.now()
router = APIRouter(prefix="/api/patients", tags=['Patient'])


@router.get('/payment/{CMND}')
def get_hospital_fee(CMND,db: Session = Depends(get_db)):
    return payment.get_hospital_fee(CMND,db)

@router.post('/payment')
def create_receiptment(request:ReceiptModel,db: Session = Depends(get_db)):
    return payment.create_receiptment(request,db)

from fastapi import APIRouter, Depends, status
from core.schema.schemas import PatientShow, Patient,PatientLogin
from core.model.models import PatientModel
from core.model.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from ..repository import patient

now = datetime.now()
router = APIRouter(prefix="/api/patients", tags=['Patient'])


# Bệnh Nhân
@router.post('/', response_model=PatientShow, status_code=status.HTTP_201_CREATED)
def create_patient(request: Patient, db=Depends(get_db)):
    return patient.create_patient(request, db)


@router.get('/', response_model=List[PatientShow])
def get_all_patients(db: Session = Depends(get_db)):
    return patient.get_all_patients(db)


@router.get('/{CMND}', status_code=200, response_model=PatientShow)
def get_patient_by_id(CMND, db: Session = Depends(get_db)):
    return patient.get_patient_by_id(CMND, db)

@router.get('login/{CMND}', status_code=200)
def get_user_login(CMND, db: Session = Depends(get_db)):
    return patient.get_user_login( db,CMND)

@router.put('/{CMND}')
def update_patient(CMND, request: Patient, db: Session = Depends(get_db)):
    return patient.update_patient(CMND, request, db)

# (CMND, HOTEN, GIOITINH, NGAYSINH, DIACHI, DOITUONG, BHYT,SODIENTHOAI, EMAIL, HINHANH )


@router.delete('/{CMND}', status_code=status.HTTP_204_NO_CONTENT)
def destroy_patient(CMND, db: Session = Depends(get_db)):
    return patient.destroy_patient(CMND, db)

@router.post('/register')
def create_account(request:PatientLogin, db:Session =Depends(get_db)):
    return patient.create_account(db,request)
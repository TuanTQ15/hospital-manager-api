from core.schema.schemas import  Patient,PatientLogin,ChangePassword
from fastapi import  status, HTTPException
from sqlalchemy.orm import Session
from core.model.models import PatientModel,PatientLoginModel
from core.utility import hashing,uploadImage,dateconverter
from datetime import datetime
from ..utility.hashing import Hash
now = datetime.now()


def get_all_patients(db: Session):
    patients = db.query(PatientModel).all()
    for patient in patients:
        patient.NGAYSINH = dateconverter.convertDateTimeToLong(str(patient.NGAYSINH))
    return patients

def create_patient(request: Patient, db: Session):

    new_patient = PatientModel(HOTEN=request.HOTEN, GIOITINH=request.GIOITINH,
                               DIACHI=request.DIACHI, CMND=request.CMND, NGAYSINH=request.NGAYSINH,
                               HINHANH=request.HINHANH, DOITUONG=request.DOITUONG, EMAIL=request.EMAIL,
                               SODIENTHOAI=request.SODIENTHOAI
                               )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


def get_patient_by_id(CMND, db: Session):
    patient = db.query(PatientModel).filter(PatientModel.CMND == CMND).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy bệnh nhân {CMND}")
    patient.NGAYSINH = dateconverter.convertDateTimeToLong(str(patient.NGAYSINH))
    return patient


def update_patient(CMND, request: Patient, db: Session):
    patient = db.query(PatientModel).filter(PatientModel.CMND == CMND)
    patientLogin= db.query(PatientLoginModel).filter(PatientLoginModel.CMND==CMND)
    if not patient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Không tìm thấy bệnh  nhân {CMND}')
    if not patientLogin.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Không tìm thấy bệnh  nhân {CMND}')

    patientObject = patient.first()
    login=patientLogin.first()
    patientObject.CMND = request.CMND
    patientObject.HOTEN = request.HOTEN
    patientObject.GIOITINH = request.GIOITINH
    patientObject.NGAYSINH = dateconverter.convertLongToDateTime(request.NGAYSINH)
    patientObject.DIACHI = request.DIACHI
    patientObject.DOITUONG = request.DOITUONG
    login.HINHANH= uploadImage.uploadFile(request.HINHANH)
    patientObject.SODIENTHOAI = request.SODIENTHOAI
    patientObject.EMAIL = request.EMAIL
    patientObject.updated_at = now
    db.commit()
    db.refresh(patientObject)
    db.refresh(login)
    patientObject.NGAYSINH=dateconverter.convertDateTimeToLong(str(patientObject.NGAYSINH))
    return patientObject


def destroy_patient(CMND, db: Session):
    employee = db.query(PatientModel).filter(PatientModel.CMND == CMND)
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Không tìm thấy bệnh nhân {CMND}')
    employee.delete(synchronize_session=False)
    db.commit()
    return
def create_account(db:Session,request: PatientLogin):
    hashedPassword = hashing.Hash.bcrypt(request.PASSWORD)
    print(len(hashedPassword))
    new_patient_login = PatientLoginModel(CMND=request.CMND,PASSWORD=hashedPassword)
    db.add(new_patient_login)
    db.commit()
    db.refresh(new_patient_login)
    return new_patient_login

def get_user_login(db:Session,CMND):
    userlogin = db.query(PatientLoginModel).filter(PatientLoginModel.CMND == CMND).first()
    if not userlogin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy bệnh nhân {CMND}")
    return userlogin

def change_password(request:ChangePassword,db:Session):
    userlogin = db.query(PatientLoginModel).filter(PatientLoginModel.CMND == request.USERNAME).first()
    hashedPassword = hashing.Hash.bcrypt(request.PASSWORD)
    userlogin.PASSWORD=hashedPassword
    db.commit()
    db.refresh(userlogin)
    return
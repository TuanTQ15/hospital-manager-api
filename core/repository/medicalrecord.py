from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from core.model.models import MedicalRecordModel,PatientModel
from ..utility import dateconverter


def get_all_medical_record(db: Session,CMND):
    if CMND=="":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Vui lòng nhập mã chứng minh nhân dân")
    medicalrecords = db.query(MedicalRecordModel).filter(MedicalRecordModel.CMND == CMND).all()
    if not medicalrecords:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy")
    for medicalrecord in medicalrecords:
        medicalrecord.NGAYLAP = dateconverter.convertDateTimeToLong(str(medicalrecord.NGAYLAP))
        for medialhistory in medicalrecord.medicalhistorys:
            medialhistory.NGAYKHAM = dateconverter.convertDateTimeToLong(str(medialhistory.NGAYKHAM))
    return medicalrecords

def get_medical_record(db: Session,CMND):
    if CMND=="":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Vui lòng nhập mã chứng minh nhân dân")
    medicalrecords = db.query(MedicalRecordModel).filter(MedicalRecordModel.CMND == CMND).all()
    if not medicalrecords:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy")
    for medicalrecord in medicalrecords:
        medicalrecord.NGAYLAP = dateconverter.convertDateTimeToLong(str(medicalrecord.NGAYLAP))

    return medicalrecords

def get_all(db:Session):
    patients = db.query(PatientModel).all()
    if not patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy")
    for patient in patients:
        patient.NGAYSINH = dateconverter.convertDateTimeToLong(str(patient.NGAYSINH))
        for medicalrecord in patient.medicalrecords:
            try:
                medicalrecord.NGAYLAP = dateconverter.convertDateTimeToLong(str(medicalrecord.NGAYLAP))
            except:
                medicalrecord.NGAYLAP = 0
            for medialhistory in medicalrecord.medicalhistorys:
                try:
                    medialhistory.NGAYKHAM = dateconverter.convertDateTimeToLong(str(medialhistory.NGAYKHAM))
                except:
                    medialhistory.NGAYKHAM = 0
    return patients

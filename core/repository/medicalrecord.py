from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from core.model.models import MedicalRecordModel
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


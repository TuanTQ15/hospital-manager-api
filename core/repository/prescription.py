from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from core.model.models import PrescriptionModel
from core.model.models import DetailPrescriptionModel

from datetime import datetime
now = datetime.now()



def get_all_prescriptions(db: Session):
    prescriptions = db.query(PrescriptionModel).all()
    return prescriptions

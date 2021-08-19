from fastapi import APIRouter, Depends, status, HTTPException
from core.schema import schemas as sm
from core.model.database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..repository import prescription

router = APIRouter(prefix="/api/prescriptions", tags=['Prescription'])


@router.get('/', response_model=List[sm.Prescription])
def get_all_prescriptions(db: Session = Depends(get_db)):
    return prescription.get_all_prescriptions(db)


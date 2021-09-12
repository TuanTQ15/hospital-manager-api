from fastapi import APIRouter, Depends, status, HTTPException
from core.schema import schemas as sm
from core.model.database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..repository import services

router = APIRouter(prefix="/api/services", tags=['Service'])


@router.get('/', response_model=List[sm.Service])
def get_all_services(db: Session = Depends(get_db)):
    return services.get_all_service(db)


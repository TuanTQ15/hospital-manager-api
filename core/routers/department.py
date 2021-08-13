from typing import List
from fastapi import APIRouter, Depends, status
from core.schema import schemas as sm
from core.model.database import get_db
from sqlalchemy.orm import Session
from ..utility import oauth2
from ..repository import department
router = APIRouter(prefix="/api/departments", tags=['Department'])


@router.get('/', response_model=List[sm.DepartmentShow])
def get_all_departments(db: Session = Depends(get_db),au=Depends(oauth2.get_current_user)):
    return department.get_all_departments(db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=sm.DepartmentShow)
def insert_department(request: sm.Department, db: Session = Depends(get_db),au=Depends(oauth2.get_current_user)):
    return department.insert_department(request,db)

@router.get('/{maKhoa}', response_model=sm.DepartmentShow)
def get_department_by_id(maKhoa, db: Session = Depends(get_db),au=Depends(oauth2.get_current_user)):
    return department.get_department_by_id(maKhoa,db)


@router.put('/{maKhoa}',response_model=sm.DepartmentShow)
def update_department(maKhoa, request: sm.Department, db: Session = Depends(get_db),au=Depends(oauth2.get_current_user)):
    return department.update_department(maKhoa,request,db)


@router.delete('/{maKhoa}',status_code=status.HTTP_204_NO_CONTENT)
def destroy_department(maKhoa, db: Session = Depends(get_db),au=Depends(oauth2.get_current_user)):
    department.destroy_department(maKhoa,db)
    return

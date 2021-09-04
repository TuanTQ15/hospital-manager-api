from fastapi import APIRouter, Depends, status, HTTPException
from core.schema import schemas as sm
from core.model.database import get_db
from sqlalchemy.orm import Session


from typing import List
from ..repository import employee

router = APIRouter(prefix="/api/employees", tags=['Employee'])


# Nhân Viên
@router.post('/', response_model=sm.EmployeeShow, status_code=status.HTTP_201_CREATED)
def create_employee(request: sm.Employee, db: Session = Depends(get_db)):
    return employee.create_employee(request,db)


@router.get('/', response_model=List[sm.EmployeeShow])
def get_all_employees(db: Session = Depends(get_db)):
    return employee.get_all_employees(db)


@router.get('/{maNV}', status_code=200)
def get_employee_by_id(maNV, db: Session = Depends(get_db)):
    return employee.get_employee_by_id(maNV,db)


@router.put('/{maNV}', response_model=sm.EmployeeShow)
def update_employee(maNV, request: sm.Employee, db: Session = Depends(get_db)):
    return employee.update_employee(maNV,request,db)


@router.delete('/{maNV}', status_code=status.HTTP_204_NO_CONTENT)
def destroy_employee(maNV, db: Session = Depends(get_db)):
    employee.destroy_employee(maNV,db)
    return

@router.post('/register')
def create_account(request:sm.EmployeeLogin, db:Session =Depends(get_db)):
    return employee.create_account(db,request)

@router.put('/password/change')
def change_password(request:sm.ChangePassword,db:Session =Depends(get_db)):
    return employee.change_password(request,db)
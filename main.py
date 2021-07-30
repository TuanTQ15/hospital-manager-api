from fastapi import FastAPI, Depends, status, HTTPException
from core.schema import schemas as sm
from core.model import models
from core.model import database
from sqlalchemy.orm import Session
from datetime import datetime
from core import hashing
from typing import List
now = datetime.now()

app = FastAPI()

models.Base.metadata.create_all(database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return "Web service for "


@app.post("/departments", status_code=status.HTTP_201_CREATED,response_model=sm.DepartmentShow,tags=['Department'])
def insert_department(request: sm.Department, db: Session = Depends(get_db)):
    new_department = models.DepartmentModel(TENKHOA=request.TENKHOA, SODT=request.SODT, EMAIL=request.EMAIL)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


@app.get('/departments',tags=['Department'])
def get_all_departments(db: Session = Depends(get_db)):
    departments = db.query(models.DepartmentModel).all()
    return departments


@app.get('/departments/{maKhoa}', status_code=200,tags=['Department'])
def get_department_by_id(maKhoa, db: Session = Depends(get_db)):
    department = db.query(models.DepartmentModel).filter(models.DepartmentModel.MAKHOA == maKhoa).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy khoa")
    return department


@app.delete('/departments/{maKhoa}',tags=['Department'])
def destroy_department(maKhoa, db: Session = Depends(get_db)):
    department = db.query(models.DepartmentModel).filter(models.DepartmentModel.MAKHOA ==
                                                         maKhoa)
    if not department.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Không tìm thấy khoa')
    department.delete(synchronize_session=False)
    db.commit()
    return


@app.put('/departments/{maKhoa}',tags=['Department'])
def update_department(maKhoa, request: sm.Department, db: Session = Depends(get_db)):
    department = db.query(models.DepartmentModel).filter(models.DepartmentModel.MAKHOA == maKhoa)
    if not department.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Không tìm thấy khoa')
    x = department.first()
    x.TENKHOA = request.TENKHOA
    x.EMAIL = request.EMAIL
    x.SODT = request.SODT
    x.updated_at = now
    db.commit()
    return

#Nhân Viên
@app.post('/employees',response_model=sm.EmployeeShow,tags=['Employee'])
def create_employee(request: sm.Employee, db=Depends(get_db)):
    hashedPassword=hashing.Hash.bcrypt(request.PASSWORD)
    if request.GIOITINH!=0 and request.GIOITINH!=1:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail='Giới tính 0: Nam, 1: Nữ')
    new_employee = models.EmployeeModel(MAKHOA=request.MAKHOA,MALOAI=request.MALOAI, HOTEN=request.HOTEN, GIOITINH=request.GIOITINH,
                                        DIACHI=request.DIACHI,
                                        CMND=request.CMND, NGAYSINH=request.NGAYSINH, HINHANH=request.HINHANH,
                                        SODT=request.SODT, EMAIL=request.SODT,USERNAME=request.USERNAME,PASSWORD= hashedPassword)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@app.get('/employees',response_model=List[sm.EmployeeShow],tags=['Employee'])
def get_all_departments(db: Session = Depends(get_db)):
    employees = db.query(models.EmployeeModel).all()
    return employees

@app.get('/employees/{maNV}', status_code=200,response_model=sm.EmployeeShow,tags=['Employee'])
def get_department_by_id(maNV, db: Session = Depends(get_db)):
    employee = db.query(models.EmployeeModel).filter(models.EmployeeModel.MANV == maNV).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy nhân viên {maNV}")
    return employee

@app.put('/employees/{maNV}',response_model=sm.EmployeeShow,tags=['Employee'])
def update_department(maNV, request: sm.Employee, db: Session = Depends(get_db)):
    employee = db.query(models.EmployeeModel).filter(models.EmployeeModel.MANV == maNV)
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Không tìm thấy nhân viên {maNV}')
    employeeObject = employee.first()
    employeeObject.MAKHOA=request.MAKHOA
    employeeObject.MALOAI = request.MALOAI
    employeeObject.HOTEN = request.HOTEN
    employeeObject.GIOITINH = request.GIOITINH
    employeeObject.DIACHI =request.DIACHI
    employeeObject.CMND =request.CMND
    employeeObject.NGAYSINH = request.NGAYSINH
    employeeObject.HINHANH =request.HINHANH
    employeeObject.SODT =request.SODT
    employeeObject.EMAIL = request.EMAIL
    employeeObject.updated_at = now
    db.commit()
    return

@app.delete('/employees/{maKhoa}',tags=['Employee'])
def destroy_department(maKhoa, db: Session = Depends(get_db)):
    department = db.query(models.DepartmentModel).filter(models.DepartmentModel.MAKHOA ==
                                                         maKhoa)
    if not department.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Không tìm thấy khoa')
    department.delete(synchronize_session=False)
    db.commit()
    return
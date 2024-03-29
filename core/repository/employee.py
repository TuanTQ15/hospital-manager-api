from core.schema import schemas as sm
from sqlalchemy.orm import Session
from core.utility import hashing,dateconverter,uploadImage
from core.model.models import EmployeeModel,EmployeeLoginModel
from fastapi import status, HTTPException
from datetime import datetime

now = datetime.now()
def validat_employee(request,):
    if len(request.MANV)>15 or len(request.MANV)<=0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=f"Mã nhân viên quá dài hoặc quá ngắn: '{request.MANV}'")

    if len(request.HOTEN)>50 or len(request.HOTEN)<=0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=f"Họ tên quá dài hoặc quá ngắn: '{request.HOTEN}'")

    if len(request.GIOITINH) > 6 or len(request.GIOITINH) <= 0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail=f"Giới tính quá dài (Nam - Nữ) ")
    if len(request.GIOITINH) <= 0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail=f"Giới tính không được để trống (Nam - Nữ)")


    if len(request.DIACHI)>15 :
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=f"Địa chỉ quá dài")

    if  len(request.DIACHI) <= 0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=f"Địa chỉ không được để trống")

    if len(request.CHUCVU)>50:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=f"Chức vụ quá dài ")

    if len(request.CHUCVU)<=0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=f"Chức vụ không được để trống")

    if len(request.SODIENTHOAI) > 15:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,detail=f"Số điện thoại quá dài")

    if len(request.CMND) > 15 or len(request.CMND) < 9 :
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail=f"Chứng minh nhân dân phải có 9 số")

    if len(request.EMAIL) > 100 :
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail=f"Email quá dài")
    if request.MALOAINV > 3:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail=f"Mã loại nhân viên không được quá 15 ký tự")
    if request.MALOAINV < 0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail=f"Mã loại nhân viên không được để trống")
    if len(request.MAKHOA) > 15 :
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail=f"Mã khoa quá dài '{request.GIOITINH}'")
    if len(request.MAKHOA) <= 0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail=f"Mã khoa không được để trống")

def validat_employee_updated(request,):


    if len(request.HOTEN)>50 or len(request.HOTEN)<=0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=f"Họ tên quá dài hoặc quá ngắn: '{request.HOTEN}'")

    if len(request.GIOITINH) > 6 or len(request.GIOITINH) <= 0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail=f"Giới tính quá dài (Nam - Nữ) ")
    if len(request.GIOITINH) <= 0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail=f"Giới tính không được để trống (Nam - Nữ)")


    if len(request.DIACHI)>15 :
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=f"Địa chỉ quá dài")

    if  len(request.DIACHI) <= 0:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail=f"Địa chỉ không được để trống")


    if len(request.SODIENTHOAI) > 15:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,detail=f"Số điện thoại quá dài")


    if len(request.EMAIL) > 100 :
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,detail=f"Mã khoa không được để trống")

def get_all_employees(db: Session):
    employees = db.query(EmployeeModel).all()
    for employee in employees:
        employee.NGAYSINH = dateconverter.convertDateTimeToLong(str(employee.NGAYSINH))
    return employees

#-	NHANVIEN ( MANV, HOTEN, GIOITINH, NGAYSINH, DIACHI, CHUCVU, SODIENTHOAI, CMND, EMAIL, HINHANH, MALOAINV , MAKHOA)
def create_employee(request: sm.Employee, db: Session):
    validat_employee(request=request)
    hashedPassword = hashing.Hash.bcrypt(request.PASSWORD)

    new_employee = EmployeeModel(MANV=request.MANV, MAKHOA=request.MAKHOA, MALOAINV=request.MALOAINV,
                                 HOTEN=request.HOTEN,
                                 GIOITINH=request.GIOITINH,
                                 DIACHI=request.DIACHI, CHUCVU=request.CHUCVU,
                                 CMND=request.CMND, NGAYSINH= datetime.fromtimestamp(request.NGAYSINH/1000), HINHANH=request.HINHANH,
                                 SODIENTHOAI=request.SODIENTHOAI, EMAIL=request.EMAIL,
                                 PASSWORD=hashedPassword)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


def get_employee_by_id(maNV, db: Session):
    employee = db.query(EmployeeModel).filter(EmployeeModel.MANV == maNV).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy nhân viên {maNV}")
    employee.NGAYSINH = dateconverter.convertDateTimeToLong(str(employee.NGAYSINH))
    return employee


def update_employee(maNV, request: sm.EmployeeUpdate, db: Session):
    employee = db.query(EmployeeModel).filter(EmployeeModel.MANV == maNV)
    employee_login= db.query(EmployeeLoginModel).filter(EmployeeLoginModel.MANV==maNV).first()
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Không tìm thấy nhân viên {maNV}')
    if not employee_login:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Không tìm thấy nhân viên {maNV}')
    validat_employee_updated(request=request)
    employeeObject = employee.first()
    employeeObject.HOTEN = request.HOTEN
    employeeObject.GIOITINH = request.GIOITINH
    employeeObject.DIACHI = request.DIACHI
    employeeObject.NGAYSINH = dateconverter.convertLongToDateTime(request.NGAYSINH)
    employee_login.HINHANH = uploadImage.uploadFile(request.HINHANH)
    employeeObject.SODIENTHOAI = request.SODIENTHOAI
    employeeObject.EMAIL = request.EMAIL
    employeeObject.updated_at = now
    db.commit()
    db.refresh(employeeObject)
    employeeObject.NGAYSINH = dateconverter.convertDateTimeToLong(str(employeeObject.NGAYSINH))
    return employeeObject


def destroy_employee(maNV, db: Session):
    employee = db.query(EmployeeModel).filter(EmployeeModel.MANV == maNV)
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Không tìm thấy nhân viên {maNV}')
    employee.delete(synchronize_session=False)
    db.commit()
    return
def create_account(db:Session,request: sm.EmployeeLogin):
    hashedPassword = hashing.Hash.bcrypt(request.PASSWORD)
    print(len(hashedPassword))
    new_patient_login = EmployeeLoginModel(MANV=request.MANV,USERNAME=request.USERNAME,PASSWORD=hashedPassword,HINHANH="https://res.cloudinary.com/ptithcm/image/upload/v1629283355/default_user.png")
    db.add(new_patient_login)
    db.commit()
    db.refresh(new_patient_login)
    return new_patient_login

def change_password(request:sm.ChangePassword,db:Session):
    userlogin = db.query(EmployeeLoginModel).filter(EmployeeLoginModel.USERNAME == request.USERNAME).first()
    if not userlogin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy bệnh nhân {request.USERNAME}")
    if not hashing.Hash.verify(userlogin.PASSWORD, request.PASSWORD):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password")
    hashedPassword = hashing.Hash.bcrypt(request.NEWPASSWORD)
    userlogin.PASSWORD=hashedPassword
    db.commit()
    db.refresh(userlogin)
    return "true"

def get_user_login(db:Session,maNV):
    employeeLogin = db.query(EmployeeLoginModel).filter(EmployeeLoginModel.MANV == maNV).first()
    if not employeeLogin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy bệnh nhân {maNV}")
    return employeeLogin
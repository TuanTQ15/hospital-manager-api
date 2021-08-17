import datetime
from typing import Optional

from pydantic import BaseModel


# Khoa
class Department(BaseModel):
    MAKHOA: str
    TENKHOA: str
    SODT: str
    EMAIL: str


class DepartmentShow(BaseModel):
    MAKHOA: str
    TENKHOA: str
    SODT: str
    EMAIL: str

    class Config:
        orm_mode = True


# Nhân Viên
class Employee(BaseModel):
    MANV: str
    MAKHOA: str
    HOTEN: str
    GIOITINH: str="Nữ"
    DIACHI: str
    CMND: str
    NGAYSINH:datetime.date
    HINHANH: str
    CHUCVU: str
    SODIENTHOAI: str
    EMAIL: str
    MALOAINV: str
    PASSWORD: str


class EmployeeShow(BaseModel):
    MANV: str
    MAKHOA: str
    HOTEN: str
    GIOITINH: str
    DIACHI: str
    CMND: str
    NGAYSINH: datetime.date
    HINHANH: str
    CHUCVU: str
    SODIENTHOAI: str
    EMAIL: str
    MALOAINV: str
    department: DepartmentShow
    class Config:
        orm_mode = True


# Bệnh Nhân
class Patient(BaseModel):
    CMND: str
    HOTEN: str
    GIOITINH: str="Nữ"
    NGAYSINH: datetime.date
    DIACHI: str
    DOITUONG: str
    BHYT: str
    SODIENTHOAI: str
    EMAIL: str
    HINHANH: str
    PASSWORD: str


# -	BENHNHAN (CMND, HOTEN, GIOITINH, NGAYSINH, DIACHI, DOITUONG, BHYT,SODIENTHOAI, EMAIL, HINHANH )
class PatientShow(BaseModel):
    CMND: str
    HOTEN: str
    GIOITINH: str
    NGAYSINH: datetime.date
    DIACHI: str
    DOITUONG: str
    BHYT: str
    SODIENTHOAI: str
    EMAIL: str
    HINHANH: str
    class Config:
        orm_mode = True

class Login(BaseModel):
    userName: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

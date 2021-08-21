import datetime
from typing import Optional, List

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
    NGAYSINH:int
    HINHANH: str
    CHUCVU: str
    SODIENTHOAI: str
    EMAIL: str
    MALOAINV: int
    PASSWORD:str


class EmployeeShow(BaseModel):
    MANV: str
    MAKHOA: str
    HOTEN: str
    GIOITINH: str
    DIACHI: str
    CMND: str
    NGAYSINH: int
    HINHANH: str
    CHUCVU: str
    SODIENTHOAI: str
    EMAIL: str
    MALOAINV: str
    class Config:
        orm_mode = True


# Bệnh Nhân
class Patient(BaseModel):
    CMND: str
    HOTEN: str
    GIOITINH: str="Nữ"
    NGAYSINH: int
    DIACHI: str
    DOITUONG: str
    BHYT: str
    SODIENTHOAI: str
    EMAIL: str
    HINHANH: str
    PASSWORD: str
    class Config:
        orm_mode = True
# -	BENHNHAN (CMND, HOTEN, GIOITINH, NGAYSINH, DIACHI, DOITUONG, BHYT,SODIENTHOAI, EMAIL, HINHANH )
class PatientShow(BaseModel):
    CMND: str
    HOTEN: str
    GIOITINH: str
    NGAYSINH: int
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




class Medicine(BaseModel):
    MATHUOC :str
    TENTHUOC :str
    CONGDUNG :str
    MOTA :str
    HINHANH :str
    class Config:
        orm_mode = True
#-	CHITIETTOATHUOC (MATOA, MATHUOC, SOLUONG, CACHDUNG,DONGIA)
class DetailPrescription(BaseModel):
    MATOA: str
    MATHUOC:str
    SOLUONG:int
    CACHDUNG:str
    DONGIA:int
    medicines: Medicine

    class Config:
        orm_mode = True


#-	TOATHUOC (MATOA,NGAYLAP, YLENH, CTKHAM_ID)
class Prescription(BaseModel):
    MATOA:str
    YLENH:str
    CTKHAM_ID:int
    detailPrescriptions: List[DetailPrescription]

    class Config:
        orm_mode = True
class DetailExamination(BaseModel):
    CTKHAM_ID:int
    MABA:str
    MABS :str
    MAYTA :str
    NGAYKHAM:int
    TINHTRANG:str
    CHANDOAN:str
    prescription: Prescription

    class Config:
        orm_mode = True

class MedicalRecordModel(BaseModel):
    __tablename__ = 'BENHAN'
    MABA :str
    MANV :str
    CMND :str
    NGAYLAP :int
    TIENSU: str
    CANNANG :int
    CHIEUCAO:int
    medicalhistorys: List[DetailExamination] =[]

    class Config:
        orm_mode = True
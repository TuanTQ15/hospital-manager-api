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
    GIOITINH: str="Female"
    DIACHI: str
    NGAYSINH:int
    HINHANH: str
    CHUCVU: str
    SODIENTHOAI: str
    EMAIL: str
    MALOAI: int
class EmployeeUpdate(BaseModel):
    MANV: str
    HOTEN: str
    GIOITINH: str="Nữ"
    DIACHI: str
    HINHANH:str
    NGAYSINH:int
    CHUCVU: str
    SODIENTHOAI: str
    EMAIL: str

class EmployeeShow(BaseModel):
    MANV: str
    MAKHOA: str
    HOTEN: str
    GIOITINH: str
    DIACHI: str
    NGAYSINH: int
    HINHANH: str
    CHUCVU: str
    SODIENTHOAI: str
    EMAIL: str
    MALOAI: str
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
    SODIENTHOAI: str
    EMAIL: str
    HINHANH: str
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
    SODIENTHOAI: str
    EMAIL: str
    HINHANH: str
    class Config:
        orm_mode = True

class EmployeeLogin(BaseModel):
    MANV: str
    USERNAME:str
    PASSWORD:str
    class Config:
        orm_mode = True
class PatientLogin(BaseModel):
    CMND: str
    PASSWORD:str
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
    HINHANH :str=None
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
    YLENH:str=None
    CTKHAM_ID:int
    detailPrescriptions: List[DetailPrescription]=None

    class Config:
        orm_mode = True
class DetailExamination(BaseModel):
    CTKHAM_ID:int
    MABA:str
    MABS :str
    MAYTA :str =None
    NGAYKHAM:int
    TINHTRANG:str
    CHANDOAN:str
    prescription: Prescription =None

    class Config:
        orm_mode = True

class DetailArrangeRomBedModel(BaseModel):
    CTPHONGGIUONG_ID:int
    MABA:str
    NGAYTHUE:datetime.datetime
    NGAYTRA:datetime.datetime
    DONGIA:int
    class Config:
        orm_mode = True

class DetailServiceModel(BaseModel):
    NGAY:datetime.datetime
    MABA:str
    MADV:str
    KETQUA:str=None
    DONGIA:int
    HINHANH:str=None
    MANV:str
    MABS:str
    class Config:
        orm_mode = True


class AdvancesModel(BaseModel):
    MAPTU:str
    NGAYLAP:datetime.datetime
    SOTIEN:int
    LYDO:str=None
    GHICHU:str=None
    MABA:str
    MANV:str
    class Config:
        orm_mode = True


class MedicalRecordModel(BaseModel):
    MABA :str
    MANV :str
    CMND :str
    NGAYLAP :int
    TIENSU: str=None
    CANNANG :int
    CHIEUCAO:int
    medicalhistorys: List[DetailExamination] =None
    class Config:
        orm_mode = True
class MedicalRecordShow(BaseModel):
    MABA :str
    MANV :str
    CMND :str
    NGAYLAP :int
    TIENSU: str
    CANNANG :int
    CHIEUCAO:int

    class Config:
        orm_mode = True


class ReceiptModel(BaseModel):
    TONGTIEN :int
    GHICHU :str=None
    MABA:str
    TIENTHUOC:int
    TIENGIUONG:int
    TONGTAMUNG:int
    TIENDICHVU:int
    THUCTRA:int

class ChangePassword(BaseModel):
    USERNAME:str
    PASSWORD:str
    NEWPASSWORD:str

class StatisticTreatment(BaseModel):
    DATEFROM:int
    DATETO:int

class PatientMedicalRecord(BaseModel):
    CMND: str
    HOTEN: str
    GIOITINH: str="Nữ"
    NGAYSINH: int
    DIACHI: str
    DOITUONG: str
    SODIENTHOAI: str
    EMAIL: str
    HINHANH: str=None
    
    class Config:
        orm_mode = True
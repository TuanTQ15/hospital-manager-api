import datetime

from pydantic import BaseModel
class Department(BaseModel):
    TENKHOA :str
    SODT :str
    EMAIL :str
class DepartmentShow(BaseModel):
    TENKHOA :str
    SODT :str
    EMAIL :str

    class Config:
        orm_mode = True
class Employee(BaseModel):
    MAKHOA: int
    MALOAI: int
    HOTEN:str
    GIOITINH:int
    DIACHI:str
    CMND:str
    NGAYSINH:datetime.date
    HINHANH:str
    SODT: str
    EMAIL: str
    USERNAME: str
    PASSWORD: str

class EmployeeShow(BaseModel):
    MAKHOA: int
    MALOAI: int
    HOTEN:str
    GIOITINH:int
    DIACHI:str
    CMND:str
    NGAYSINH:datetime.date
    HINHANH:str
    SODT: str
    EMAIL: str

    class Config:
        orm_mode = True
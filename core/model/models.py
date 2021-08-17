from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey
from sqlalchemy.dialects.postgresql import DATE
from sqlalchemy.orm import relationship

from core.model.database import Base
from datetime import datetime

now = datetime.now()


class DepartmentModel(Base):
    __tablename__ = 'KHOA'
    MAKHOA = Column(String, primary_key=True, nullable=False)
    TENKHOA = Column(String)
    SODT = Column(String)
    EMAIL = Column(String)
    created_at = Column(DATETIME, default=now)
    updated_at = Column(DATETIME)
    employees = relationship("EmployeeModel", back_populates="department")


class EmployeeModel(Base):
    __tablename__ = 'NHANVIEN'
    MANV = Column(String, primary_key=True, nullable=False)
    MAKHOA = Column(String, ForeignKey("KHOA.MAKHOA"), nullable=False)
    HOTEN = Column(String)
    GIOITINH = Column(String)
    DIACHI = Column(String)
    CMND = Column(String)
    NGAYSINH = Column(String)
    HINHANH = Column(String)
    CHUCVU = Column(String)
    SODIENTHOAI = Column(String)
    EMAIL = Column(String)
    MALOAINV = Column(Integer)
    PASSWORD = Column(String)
    created_at = Column(DATETIME, default=now)
    updated_at = Column(DATETIME)
    department = relationship("DepartmentModel", back_populates="employees")


class PatientModel(Base):
    __tablename__ = 'BENHNHAN'
    CMND = Column(String, primary_key=True, nullable=False)
    HOTEN = Column(String)
    DIACHI = Column(String)
    GIOITINH = Column(String)
    NGAYSINH = Column(String)
    HINHANH = Column(String)
    SODIENTHOAI = Column(String)
    EMAIL = Column(String)
    DOITUONG = Column(String)
    BHYT = Column(String)
    PASSWORD = Column(String)
    created_at = Column(DATETIME, default=now)
    updated_at = Column(DATETIME)

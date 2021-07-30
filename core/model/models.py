from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey,BOOLEAN
from sqlalchemy.dialects.postgresql import BIT, DATE
from sqlalchemy.orm import relationship

from core.model.database import Base
from datetime import datetime

now = datetime.now()


class DepartmentModel(Base):
    __tablename__ = 'KHOA'
    MAKHOA = Column(Integer, primary_key=True)
    TENKHOA = Column(String)
    SODT = Column(String)
    EMAIL = Column(String)
    created_at=Column(DATETIME,default=now)
    updated_at=Column(DATETIME)
    deleted_at=Column(DATETIME)

    employees=relationship("EmployeeModel", back_populates="departments")

class EmployeeModel(Base):
    __tablename__ = 'NHANVIEN'
    MANV = Column(Integer, primary_key=True)
    MAKHOA = Column(Integer,ForeignKey("KHOA.MAKHOA"),nullable=False)
    HOTEN= Column(String)
    GIOITINH= Column(Integer)
    DIACHI= Column(String)
    CMND= Column(String)
    NGAYSINH= Column(DATE)
    HINHANH= Column(String)
    SODT= Column(String)
    EMAIL= Column(String)
    MALOAI=Column(Integer)
    USERNAME=Column(String)
    PASSWORD=Column(String)
    created_at = Column(DATETIME,default=now)
    updated_at = Column(DATETIME)
    deleted_at = Column(DATETIME)
    departments = relationship("DepartmentModel", back_populates="employees")


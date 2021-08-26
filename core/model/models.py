from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey,BigInteger
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
    NGAYSINH = Column(BigInteger)
    HINHANH = Column(String)
    CHUCVU = Column(String)
    SODIENTHOAI = Column(String)
    EMAIL = Column(String)
    MALOAI = Column(Integer)
    department = relationship("DepartmentModel", back_populates="employees")


class PatientModel(Base):
    __tablename__ = 'BENHNHAN'
    CMND = Column(String, primary_key=True, nullable=False)
    HOTEN = Column(String)
    DIACHI = Column(String)
    GIOITINH = Column(String)
    NGAYSINH = Column(DATETIME)
    HINHANH = Column(String)
    SODIENTHOAI = Column(String)
    EMAIL = Column(String)
    DOITUONG = Column(String)
    BHYT = Column(String)
    account = relationship("PatientLoginModel", uselist=False)


class PatientLoginModel(Base):
    __tablename__ = 'USERBENHNHAN'
    ID= Column(Integer,primary_key=True,nullable=False)
    PASSWORD =Column(String,nullable=False)
    CMND=Column(String, ForeignKey(PatientModel.CMND),nullable=False)
    HINHANH= Column(String, nullable=True)


class EmployeeLoginModel(Base):
    __tablename__ = 'USERNHANVIEN'
    ID = Column(Integer, primary_key=True, nullable=False)
    PASSWORD = Column(String, nullable=False)
    MANV = Column(String, nullable=False)
    USERNAME = Column(String, nullable=False)
    HINHANH = Column(String, nullable=True)

#CHITIETKHAM(CTKHAM_ID ,  MABA,MABS,MAYTA,NGAYKHAM,TINHTRANG,CHANDOAN )
class MedicalHistory(Base):
    __tablename__ = 'CHITIETKHAM'
    CTKHAM_ID=Column(Integer, primary_key=True, nullable=False)
    MABA=Column(String,ForeignKey("BENHAN.MABA"),  nullable=False)
    MABS = Column(String,nullable=False)
    MAYTA =Column(String,nullable=False)
    NGAYKHAM=Column(DATETIME,nullable=False)
    TINHTRANG=Column(String)
    CHANDOAN = Column(String)
    prescription = relationship("PrescriptionModel", uselist=False)
    medicalrecords = relationship("MedicalRecordModel", back_populates="medicalhistorys")

#-	TOATHUOC (MATOA,NGAYLAP, Y LENH, CTKHAM_ID)
class PrescriptionModel(Base):
    __tablename__ = 'TOATHUOC'
    MATOA = Column(String, primary_key=True, nullable=False)
    YLENH = Column(String)
    CTKHAM_ID=Column(Integer,ForeignKey("CHITIETKHAM.CTKHAM_ID"),nullable=False)
    detailPrescriptions = relationship("DetailPrescriptionModel", back_populates="prescription")


class MedicineModel(Base):
    __tablename__ = 'THUOC'
    MATHUOC=Column(String, primary_key=True,nullable=False)
    TENTHUOC=Column(String)
    CONGDUNG=Column(String)
    MOTA=Column(String)
    HINHANH=Column(String)
    detailPrescriptions = relationship("DetailPrescriptionModel", back_populates="medicines")

#-	CHITIETTOATHUOC (MATOA, MATHUOC, SOLUONG, CACHDUNG,DONGIA)
class DetailPrescriptionModel(Base):
    __tablename__ = 'CHITIETTOATHUOC'
    MATOA = Column(String,ForeignKey(PrescriptionModel.MATOA), primary_key=True, nullable=False)
    MATHUOC = Column(String, ForeignKey(MedicineModel.MATHUOC), primary_key=True, nullable=False)
    SOLUONG=Column(Integer)
    CACHDUNG=Column(String)
    DONGIA=Column(Integer)
    prescription = relationship("PrescriptionModel",back_populates="detailPrescriptions")
    medicines = relationship("MedicineModel", back_populates="detailPrescriptions")
#-	BENHAN ( MABA, NGAYLAP,CHIEUCAO,CANNANG,TIENSU, MANV , CMND )
class MedicalRecordModel(Base):
    __tablename__ = 'BENHAN'
    MABA = Column(String, primary_key=True, nullable=False)
    MANV =Column(String, ForeignKey(EmployeeModel.MANV),nullable=False)
    CMND = Column(String,ForeignKey(PatientModel.CMND),nullable=False)
    NGAYLAP = Column(DATETIME, nullable=False)
    TIENSU=Column(String)
    CANNANG = Column(Integer)
    CHIEUCAO=Column(Integer)
    medicalhistorys = relationship("MedicalHistory", back_populates="medicalrecords")
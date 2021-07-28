from sqlalchemy import Column, Integer, String,DATETIME
from data.database import Base
from datetime import datetime
now = datetime.now()

class DepartmentModel(Base):
    __tablename__ = 'KHOA'
    MAKHOA = Column(Integer, primary_key=True)
    TENKHOA = Column(String)
    SODT = Column(String)
    EMAIL = Column(String)
    created_at=Column(DATETIME,default=now)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (self.maKhoa, self.tenKhoa, self.soDT, self.email)

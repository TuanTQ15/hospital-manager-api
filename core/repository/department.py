from core.schema import schemas as sm
from core.model import models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from ..utility import dateconverter

now = datetime.now()


def get_all_departments(db: Session):
    departments = db.query(models.DepartmentModel).all()
    return departments


def insert_department(request: sm.Department, db: Session):
    new_department = models.DepartmentModel(MAKHOA=request.MAKHOA, TENKHOA=request.TENKHOA, SODT=request.SODT,
                                            EMAIL=request.EMAIL)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


def get_department_by_id(maKhoa, db: Session):
    department = db.query(models.DepartmentModel).filter(models.DepartmentModel.MAKHOA == maKhoa).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy mã khoa {maKhoa}")
    return department


def update_department(maKhoa, request: sm.Department, db: Session):
    department = db.query(models.DepartmentModel).filter(models.DepartmentModel.MAKHOA == maKhoa)
    if not department.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy mã khoa {maKhoa}")
    response = department.first()
    response.TENKHOA = request.TENKHOA
    response.EMAIL = request.EMAIL
    response.SODT = request.SODT
    response.updated_at = now
    db.commit()
    db.refresh(response)
    return response


def destroy_department(maKhoa, db: Session):
    department = db.query(models.DepartmentModel).filter(models.DepartmentModel.MAKHOA == maKhoa)
    if not department.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy mã khoa {maKhoa}")
    department.delete(synchronize_session=False)
    db.commit()
    return

def statistic_treatment_by_department(db,DATEFROM,DATETO):
    if DATEFROM < 0  or DATETO <0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    date_from=dateconverter.convertLongToDate(DATEFROM,'%Y-%m-%d')
    date_to = dateconverter.convertLongToDate(DATETO,'%Y-%m-%d')
    date_to+= ' 23:59:59.999'
    query='select "TENKHOA",count(ba."MABA") as "SOLUONG" from "KHOA" as kh left join ' \
          '"NHANVIEN" as nv on kh."MAKHOA" = nv."MAKHOA" left join "BENHAN" as ba on nv."MANV" = ba."MANV" where' \
          ' ba."NGAYLAP" between \''+ date_from + '\' and  \''+ date_to+'\' or ba."NGAYLAP" IS NULL group by "TENKHOA"'
    print(query)
    return [dict(u) for u in db.execute(query).fetchall()]
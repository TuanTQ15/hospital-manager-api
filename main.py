from fastapi import FastAPI, Depends, status, Response, HTTPException
from core.schemas import schemas
from core.model import model, database
from sqlalchemy.orm import Session
from datetime import datetime

now = datetime.now()

app = FastAPI()

model.Base.metadata.create_all(database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/departments", status_code=status.HTTP_201_CREATED)
def insert_department(request: schemas.Department, db: Session = Depends(get_db)):
    new_department = model.model.DepartmentModel(TENKHOA=request.TENKHOA, SODT=request.SODT, EMAIL=request.EMAIL)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


@app.get('/departments')
def get_all_departments(db: Session = Depends(get_db)):
    departments = db.query(model.DepartmentModel).all()
    return departments


@app.get('/departments/{id}', status_code=200)
def get_department_by_id(id, response: Response, db: Session = Depends(get_db)):
    department = db.query(model.DepartmentModel).filter(model.DepartmentModel.MAKHOA == id).first()
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy khoa")
    return department


@app.delete('/departments/{id}')
def destroy_department(id, db: Session = Depends(get_db)):
    department = db.query(model.DepartmentModel).filter(model.DepartmentModel.MAKHOA ==
                                                        id)
    if not department.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Không tìm thấy khoa')
    department.delete(synchronize_session=False)
    db.commit()
    return


@app.put('/departments/{id}')
def update_department(id, request: schemas.Department, db: Session = Depends(get_db)):
    department = db.query(model.DepartmentModel).filter(model.DepartmentModel.MAKHOA == id)
    if not department.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Không tìm thấy khoa')
    x = department.first()
    x.TENKHOA = request.TENKHOA
    x.EMAIL = request.EMAIL
    x.SODT = request.SODT
    x.updated_at = now
    db.commit()
    return

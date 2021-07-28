from fastapi import FastAPI,Depends
from data import model,schemas,database
from sqlalchemy.orm import Session

app = FastAPI()

model.Base.metadata.create_all(database.engine)
def get_db():
    db=database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/departments")
def insert_department(request: schemas.Department,db:Session=Depends(get_db)):

    new_department = model.DepartmentModel(TENKHOA=request.tenKhoa,SODT=request.soDT,EMAIL=request.email)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department
@app.get('/departments')
def get_all_departments(db: Session=Depends(get_db)):
    departments=db.query(model.DepartmentModel).all()
    return departments
@app.get('/departments/{id}')
def get_department_by_id(id,db: Session=Depends(get_db)):
    department=db.query(model.DepartmentModel).filter(model.DepartmentModel.MAKHOA==id).first()
    return department
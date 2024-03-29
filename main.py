from fastapi import FastAPI
from core.model import database, models
from core.routers import department, employee, patient,authentication,services,medicalrecord,payment

app = FastAPI()
models.Base.metadata.create_all(database.engine)
app.include_router(authentication.router)
app.include_router(department.router)
app.include_router(employee.router)
app.include_router(patient.router)
app.include_router(services.router)
app.include_router(medicalrecord.router)
app.include_router(payment.router)

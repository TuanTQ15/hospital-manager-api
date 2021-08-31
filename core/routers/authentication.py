from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from core.model.database import get_db
from core.model import models
from ..utility.hashing import Hash
from ..utility import token

router = APIRouter(prefix="/api", tags=["Authentication"])


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    userPatientLogin = db.query(models.PatientLoginModel).filter(models.PatientLoginModel.CMND == request.username).first()
    userEmployee = db.query(models.EmployeeLoginModel).filter(models.EmployeeLoginModel.USERNAME == request.username).first()
    if not userPatientLogin and not userEmployee:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    if userPatientLogin:
        if not Hash.verify(userPatientLogin.PASSWORD, request.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password")
        access_token = token.create_access_token(data={"sub": userPatientLogin.CMND})
        patient=db.query(models.PatientModel).filter(models.PatientModel.CMND==userPatientLogin.CMND).first()
        return {"access_token": access_token, "account_role": "patient", "token_type": "bearer",
                "username":userPatientLogin.CMND,"fullname":patient.HOTEN,"email":patient.EMAIL,"image_url":userPatientLogin.HINHANH}
    elif userEmployee:
        if not Hash.verify(userEmployee.PASSWORD, request.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password")
        access_token = token.create_access_token(data={"sub": userEmployee.MANV})
        employee = db.query(models.PatientModel).filter(models.PatientModel.MANV == userPatientLogin.MANV).first()
        return {"access_token": access_token, "account_role": "doctor", "token_type": "bearer",
                "username":userEmployee.MANV,"fullname":employee.HOTEN,"email":employee.EMAIL,"image_url":employee.HINHANH}

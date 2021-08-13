from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,status
from core.model.database import get_db
from core.model import models
from ..utility.hashing import Hash
from ..utility import token
router = APIRouter(prefix="/api",tags=["Authentication"])
@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db : Session =Depends(get_db)):
    userPatient = db.query(models.PatientModel).filter(models.PatientModel.USERNAME==request.username).first()
    userEmployee = db.query(models.EmployeeModel).filter(models.EmployeeModel.USERNAME==request.username).first()
    if not userPatient and not userEmployee:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    if userPatient:
        if not Hash.verify(userPatient.PASSWORD,request.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password")
        access_token = token.create_access_token( data={"sub": userPatient.USERNAME})
        return {"access_token": access_token, "token_type": "bearer"}
    elif userEmployee:
        if not Hash.verify(userEmployee.PASSWORD, request.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password")
        access_token = token.create_access_token(data={"sub": userEmployee.USERNAME})
        return {"access_token": access_token, "token_type": "bearer"}
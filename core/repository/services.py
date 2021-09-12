from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from core.model.models import ServiceModel


from datetime import datetime
now = datetime.now()



def get_all_service(db: Session):
    services = db.query(ServiceModel).all()
    if not services:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return services

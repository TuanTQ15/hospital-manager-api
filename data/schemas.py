from pydantic import BaseModel
class Department(BaseModel):
    maKhoa :int
    tenKhoa :str
    soDT :str
    email :str
from pydantic import BaseModel

class UserEdit(BaseModel):
    fldSNombre: str
    fldSColor1: str
    fldSColor2: str
    fldSLogo: str

class UserBase(UserEdit):
    fldSCorreo: str
    fldSUsername: str

class UserNew(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True
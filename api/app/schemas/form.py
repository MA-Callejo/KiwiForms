from datetime import datetime

from pydantic import BaseModel

class FormNew(BaseModel):
    fldSTitulo: str
    fldSDescripcion: str

class FormNewBody(FormNew):
    fldSBody: str

class FormBase(FormNew):
    id: int
    fldDCreacion: datetime
    class Config:
        orm_mode = True

class Form(FormBase):
    fldSBody: str
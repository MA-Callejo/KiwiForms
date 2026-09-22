from sqlalchemy import Column, Integer, String, Date, DATETIME

from app.core.db import Base

class tbl_formulario(Base):
    id = Column(Integer, primary_key=True, index=True)
    fldSTitulo = Column(String)
    fldSDescripcion = Column(String)
    fldSBody = Column(String)
    fkCreador = Column(Integer)
    fldDCreacion = Column(DATETIME)
from sqlalchemy import Column, Integer, String, Date

from app.core.db import Base

class tbl_users(Base):
    id = Column(Integer, primary_key=True, index=True)
    fldSNombre = Column(String)
    fldSCorreo = Column(String)
    fldSHashPass = Column(String)
    fldSToken = Column(String)
    fldSLogo = Column(String)
    fldSColor1 = Column(String)
    fldSColor2 = Column(String)
    fldSUsername = Column(String)
    fldBActive = Column(Integer)
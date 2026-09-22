import json
import re
from datetime import datetime, timedelta
from typing import Any, Optional
from urllib.parse import unquote

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from fastapi import APIRouter, Body, Depends, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import or_

from app import models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import verify_password
from app.models import tbl_users

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    app: int = 1,
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(tbl_users).filter(or_(tbl_users.fldSCorreo == form_data.username, tbl_users.fldSNombre == form_data.username)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.fldSHashPass:
        raise HTTPException(status_code=403, detail="Incorrect email or password")
    if not verify_password(form_data.password, user.fldSHashPass):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    db.close()
    id = user.id
    return {
        "access_token": security.create_access_token(
            subject=id
        ),
        "token_type": "bearer",
        "email": user.fldSCorreo,
        "user": id
    }


@router.post("/login/test-token")
def test_token(current_user: models.tbl_users = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user

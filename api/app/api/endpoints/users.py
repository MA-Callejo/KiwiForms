from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api import deps
from app.core.security import get_password_hash, generar_token
from app.models import tbl_users
from app.schemas import User
from app.schemas.user import UserBase, UserNew, UserEdit

router = APIRouter()

@router.get("/", response_model=User)
def get_user_me(
        *,
        current_user: tbl_users = Depends(deps.get_current_user),
) -> Any:
    return current_user

@router.get("/{id}", response_model=User)
def get_user(
        *,
        id: int,
        db: Session = Depends(deps.get_db),
) -> Any:
    user = db.query(tbl_users).get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/passwd/", response_model=User)
def update_user(
        *,
        password: str,
        db: Session = Depends(deps.get_db),
        current_user: tbl_users = Depends(deps.get_current_user),
) -> Any:
    user = db.query(tbl_users).get(current_user.id)
    user.fldSHashPass = get_password_hash(password)
    db.commit()
    db.refresh(user)
    return user

@router.post("/", response_model=User)
def update_user(
        *,
        user_in: UserEdit,
        db: Session = Depends(deps.get_db),
        current_user: tbl_users = Depends(deps.get_current_user),
) -> Any:
    user = db.query(tbl_users).get(current_user.id)
    user.fldSNombre = user_in.fldSNombre
    user.fldSColor1 = user_in.fldSColor1
    user.fldSColor2 = user_in.fldSColor2
    user.fldSLogo = user_in.fldSLogo
    db.commit()
    db.refresh(user)
    return user

@router.put("/", response_model=User)
def create_user(
        *,
        user_in: UserNew,
        db: Session = Depends(deps.get_db),
) -> Any:
    libremail = db.query(func.count(tbl_users.id)).filter(tbl_users.fldSCorreo == user_in.fldSCorreo).scalar()
    if libremail:
        raise HTTPException(status_code=400, detail="Email already exists")
    libreusername = db.query(func.count(tbl_users.id)).filter(tbl_users.fldSUsername == user_in.fldSUsername).scalar()
    if libreusername:
        raise HTTPException(status_code=400, detail="Username already exists")
    token = generar_token(200)
    new_user = tbl_users(
        fldSUsername = user_in.fldSUsername,
        fldSNombre = user_in.fldSNombre,
        fldSCorreo = user_in.fldSCorreo,
        fldSColor1 = user_in.fldSColor1,
        fldSColor2 = user_in.fldSColor2,
        fldSLogo = user_in.fldSLogo,
        fldSHashPass = get_password_hash(user_in.password),
        fldSToken = token,
        fldBActive = 0
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/password/", response_model=int)
def solicitar_password(
        *,
        correo: str,
        db: Session = Depends(deps.get_db),
) -> Any:
    user = db.query(tbl_users).filter(tbl_users.fldSCorreo == correo).first()
    if not user:
        return 1
    token = generar_token(200)
    user.fldSToken = token
    db.commit()
    db.refresh(user)
    return user

@router.post("/active/{token}", response_model=User)
def active_user(
        *,
        token: str,
        db: Session = Depends(deps.get_db),
) -> Any:
    user = db.query(tbl_users).filter(tbl_users.fldSToken == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.fldSToken = None
    user.fldBActive = 1
    db.commit()
    db.refresh(user)
    return user

@router.post("/password/{token}", response_model=User)
def reset_password(
        *,
        token: str,
        password: str,
        db: Session = Depends(deps.get_db),
) -> Any:
    user = db.query(tbl_users).filter(tbl_users.fldSToken == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.fldSToken = None
    user.fldSHashPass = get_password_hash(password)
    db.commit()
    db.refresh(user)
    return user
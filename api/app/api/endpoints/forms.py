import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from app.api import deps
from app.core.security import get_password_hash, generar_token
from app.models import tbl_users, tbl_formulario
from app.schemas import User
from app.schemas.form import FormBase, Form, FormNew, FormNewBody
from app.schemas.user import UserBase, UserNew, UserEdit

router = APIRouter()

@router.get("/", response_model=List[FormBase])
def get_forms_list(
        *,
        limit: int = 100,
        offset: int = 0,
        patron: str = "",
        db: Session = Depends(deps.get_db),
        current_user: tbl_users = Depends(deps.get_current_user),
) -> Any:
    return [r for r in db.query(tbl_formulario).filter(tbl_formulario.fkCreador == current_user.id).filter(or_(tbl_formulario.fldSDescripcion.like('%'+patron+'%'), tbl_formulario.fldSTitulo.like('%'+patron+'%'))).order_by(tbl_formulario.fldDCreacion.desc()).limit(limit).offset(offset).all()]


@router.get("/{id}", response_model=FormBase)
def get_by_id(
        *,
        id: int,
        db: Session = Depends(deps.get_db),
        current_user: tbl_users = Depends(deps.get_current_user),
) -> Any:
    item = db.query(tbl_formulario).get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/cabecera/{id}", response_model=FormBase)
def update_cabecera(
        *,
        id: int,
        form_in: FormNew,
        db: Session = Depends(deps.get_db),
        current_user: tbl_users = Depends(deps.get_current_user),
) -> Any:
    formulario = db.query(tbl_formulario).get(id)
    if not formulario:
        raise HTTPException(status_code=404, detail="Formulario not found")
    if not formulario.fkCreador == current_user.id:
        raise HTTPException(status_code=403, detail="Creador not authorized")
    formulario.fldSDescripcion = form_in.fldSDescripcion
    formulario.fldSTitulo = form_in.fldSTitulo
    db.commit()
    db.refresh(formulario)
    return formulario

@router.post("/body/{id}", response_model=FormBase)
def update_body(
        *,
        id: int,
        body: str,
        db: Session = Depends(deps.get_db),
        current_user: tbl_users = Depends(deps.get_current_user),
) -> Any:
    formulario = db.query(tbl_formulario).get(id)
    if not formulario:
        raise HTTPException(status_code=404, detail="Formulario not found")
    if not formulario.fkCreador == current_user.id:
        raise HTTPException(status_code=403, detail="Creador not authorized")
    formulario.fldSBody = body
    db.commit()
    db.refresh(formulario)
    return formulario


@router.delete("/{id}", response_model=int)
def delete_form(
        *,
        id: int,
        db: Session = Depends(deps.get_db),
        current_user: tbl_users = Depends(deps.get_current_user),
) -> Any:
    formulario = db.query(tbl_formulario).get(id)
    if not formulario:
        raise HTTPException(status_code=404, detail="Formulario not found")
    if not formulario.fkCreador == current_user.id:
        raise HTTPException(status_code=403, detail="Creador not authorized")
    db.delete(formulario)
    db.commit()
    return 1


@router.put("/", response_model=FormBase)
def create_form(
        *,
        item_in: FormNewBody,
        db: Session = Depends(deps.get_db),
) -> Any:
    new_item = tbl_formulario(
        fldSTitulo=item_in.fldSTitulo,
        fldSDescripcion=item_in.fldSDescripcion,
        fldSBody=item_in.fldSBody,
        fkCreador=current_user.id,
        fldDCreacion=datetime.datetime.now(),
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

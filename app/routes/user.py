from fastapi import APIRouter, Depends
from app.models.user import CreateUser
from sqlalchemy.orm import Session
from app.database.db import get_db
from typing import Annotated
from app.database.schema.user_schema import UserSchema
from sqlalchemy import select
from fastapi.responses import JSONResponse
from app.dependancies import autheticate_user
from app.models.auth import AuthUser
from app.helper import hashPassword

router = APIRouter(prefix="/user")

@router.get("/")
def display(db: Annotated[Session, Depends(get_db)], authUser:Annotated[AuthUser, Depends(autheticate_user)]):
    user_data = select(UserSchema.id, UserSchema.name, UserSchema.email, UserSchema.is_active)
    data = db.execute(user_data).mappings().all()
    return JSONResponse(
        {"message": "Data fetch successfully", "data":data, "authUser": authUser}, status_code=200
    )

@router.get("/{id}")
def find_by_id(id: int, db: Annotated[Session, Depends(get_db)]):
    data = db.query(UserSchema).filter(UserSchema.id == id).first()
    return JSONResponse(
        {"message":"Data fetch successfully", "data":data}, status_code=200
    )

@router.post("/")
def create_user(item: CreateUser, db: Annotated[Session, Depends(get_db)]):
    user_data = UserSchema(name=item.name, email=item.email, is_active=item.is_active, password=hashPassword(item.password))
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return JSONResponse(
        {"message":"Data save successfully", "data": user_data}, status_code=200
    )

@router.delete("/{id}")
def delete_by_id(id: int, db: Annotated[Session, Depends(get_db)]):
    data = db.query(UserSchema).filter(UserSchema.id == id).first()
    if not data:
        return JSONResponse(
            {"message":"Item not found"}, status_code=201
        )
    db.delete(data)
    db.commit()
    return JSONResponse(
        {"message": "Item deleted successfully"}, status_code=201
    )

@router.put("/{id}")
def update_by_id(id: int, item: CreateUser, db: Annotated[Session, Depends(get_db)]):
    data = db.query(UserSchema).filter(UserSchema.id == id).first()
    if not data:
        return JSONResponse(
            {"message":"Item not found"}, status_code=201
        )
    data.name = item.name
    data.email = item.email
    data.is_active = item.is_active
    data.password = hashPassword(item.password)
    db.commit()
    db.refresh(data)
    return JSONResponse(
        {"message":"Item update successfully", "data": data}, status_code=200
    )
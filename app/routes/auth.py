from fastapi import APIRouter, Depends
from app.models.auth import Register, Login
from sqlalchemy.orm import Session
from app.database.db import get_db
from typing import Annotated
from app.database.schema.user_schema import UserSchema
from fastapi.responses import JSONResponse
from app.helper import hashPassword, verifyPassword, createAcessToken

router = APIRouter(prefix="/auth")

@router.post("/login")
def login(data: Login, db: Annotated[Session, Depends(get_db)]):
    user = db.query(UserSchema).filter(UserSchema.email == data.email).first()
    if not user or not verifyPassword(data.password, user.password):
        return JSONResponse(
            {"message":"Invalid email or password"}, status_code=401
        )
    payload = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
    token = createAcessToken(payload)
    payload["access_token"] = "Bearer " + token
    return {"message":"Login successful", "data":payload}

@router.post("/register")
def register(data: Register, db: Annotated[Session, Depends(get_db)]):
    # Check if user with t he same email address exists
    existing_user = db.query(UserSchema).filter(UserSchema.email == data.email).first()
    if existing_user:
        return JSONResponse({"message": "Email-Id already exists"}, status_code=400)
    
    # Create a new user
    new_user = UserSchema(
        name = data.name,
        email = data.email,
        password = hashPassword(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return JSONResponse({"message" : "User register successfully"}, status_code=200)
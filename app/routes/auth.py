from fastapi import APIRouter, Depends
from app.models.auth import Register
from sqlalchemy.orm import Session
from app.database.db import get_db
from typing import Annotated
from app.database.schema.user_schema import UserSchema
from fastapi.responses import JSONResponse
from app.helper import hashPassword

router = APIRouter(prefix="/auth")

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
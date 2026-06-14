from pydantic import BaseModel, EmailStr, Field, ValidationInfo

class CreateUser(BaseModel):
    name: str = Field(... , max_length=20, min_length=2)
    email: EmailStr
    password: str = Field(... , min_length=6, max_length=10)
    is_active: bool = True
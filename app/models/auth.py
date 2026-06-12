from pydantic import BaseModel, Field, EmailStr, ValidationInfo, field_validator

class Login(BaseModel):
    email: EmailStr
    password: str = Field(... , min_length=6, max_length=10)

class Register(BaseModel):
    name: str = Field(... , min_length=2, max_length=20)
    email: EmailStr
    password: str = Field(... , min_length=6, max_length=10)
    confirm_password: str = Field(... , min_length=6, max_length=10)
    
    @field_validator("confirm_password")
    @classmethod
    def password_match(cls, v, info: ValidationInfo):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError("Password not matched")
        return v
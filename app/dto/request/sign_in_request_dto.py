from pydantic import BaseModel, EmailStr


class SignInRequestDto(BaseModel):
    email_or_username: str
    plain_password: str

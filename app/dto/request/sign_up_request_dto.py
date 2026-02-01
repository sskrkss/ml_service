from pydantic import BaseModel, EmailStr, field_validator


class SignUpRequestDto(BaseModel):
    email: EmailStr
    username: str
    plain_password: str

    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        if len(value) < 5:
            raise ValueError("Username must be at least 5 characters")
        if len(value) > 50:
            raise ValueError("Username must not exceed 50 characters")
        return value

    @field_validator("plain_password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        return value

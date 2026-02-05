from pydantic import BaseModel, Field, field_validator


class RunMlTaskRequestDto(BaseModel):
    input_text: str = Field(
        min_length=5,
        max_length=200,
        description="Text for emotion analysis"
    )

    @field_validator('input_text')
    def validate(cls, value: str) -> str:
        if len(value) > 200:
            raise ValueError("Text exceeds maximum length of 200 characters")

        return value

from pydantic import BaseModel, Field, field_validator


class RunMlTaskRequestDto(BaseModel):
    input_text: str = Field(
        min_length=10,
        max_length=2000,
        description="Text for emotion analysis"
    )

    @field_validator('input_text')
    def validate_for_roberta(cls, value: str) -> str:
        if len(value) > 2000:
            raise ValueError("Text exceeds maximum length of 2000 characters")

        return value

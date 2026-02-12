from pydantic import BaseModel, Field, field_validator


class RunMlTaskRequestDto(BaseModel):
    input_text: str = Field(
        min_length=5,
        max_length=200,
        description="Text for emotion analysis"
    )

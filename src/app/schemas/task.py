from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("title cannot be null")
        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool

    model_config = {"from_attributes": True}

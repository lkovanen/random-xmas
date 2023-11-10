from pydantic import BaseModel, EmailStr, Field


class Elf(BaseModel):
    name: str
    email: EmailStr
    wishes: list[str] = Field(default_factory=list)

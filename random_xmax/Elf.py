from pydantic import BaseModel, EmailStr


class Elf(BaseModel):
    name: str
    email: EmailStr
    wishes: list[str]

from typing import Optional
from sqlmodel import SQLModel,Field

class User(SQLModel):
    id : Optional[int] = Field(default=None, primary_key=True)
    username: str
    email : str
    password : str
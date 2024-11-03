from pydantic import BaseModel #formato basemodel para user
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None #hacer el id opcional
    username: str
    email: str
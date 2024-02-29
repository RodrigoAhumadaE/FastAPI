from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str]      # definimos el campo id como opcional para que no debamos enviarlo nosotros y lo genere mongodb automaticamente, y este es string
    username: str
    email: str
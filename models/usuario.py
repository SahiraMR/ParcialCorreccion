from pydantic import BaseModel
from typing import Literal, Optional

class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    edad: Optional[int] = None
    tipo: Literal["Premium", "Inactivo"]

from pydantic import BaseModel
from typing import Literal
from datetime import date

class Tarea(BaseModel):
    id: int
    nombre: str
    descripcion: str
    fecha_creacion: date
    fecha_modificacion: date
    estado: Literal["Pendiente", "En ejecucion", "Realizada", "Cancelada"]
    usuario: int  # ID del usuario asociado

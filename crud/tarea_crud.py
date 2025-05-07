import csv
from typing import List, Optional
from datetime import datetime
from models.tarea import Tarea

RUTA_CSV_TAREAS = "data/tareas.csv"

def leer_tareas() -> List[Tarea]:
    tareas = []
    with open(RUTA_CSV_TAREAS, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tareas.append(Tarea(**{
                "id": int(row["id"]),
                "nombre": row["nombre"],
                "descripcion": row["descripcion"],
                "fecha_creacion": datetime.strptime(row["fecha_creacion"], "%Y-%m-%d").date(),
                "fecha_modificacion": datetime.strptime(row["fecha_modificacion"], "%Y-%m-%d").date(),
                "estado": row["estado"],
                "usuario": int(row["usuario"])
            }))
    return tareas

def guardar_tareas(lista: List[Tarea]):
    with open(RUTA_CSV_TAREAS, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "nombre", "descripcion", "fecha_creacion",
            "fecha_modificacion", "estado", "usuario"
        ])
        writer.writeheader()
        for t in lista:
            writer.writerow({
                **t.dict(),
                "fecha_creacion": t.fecha_creacion.isoformat(),
                "fecha_modificacion": t.fecha_modificacion.isoformat()
            })

def agregar_tarea(tarea: Tarea):
    tareas = leer_tareas()
    tareas.append(tarea)
    guardar_tareas(tareas)

def obtener_tarea_por_id(tarea_id: int) -> Optional[Tarea]:
    tareas = leer_tareas()
    for t in tareas:
        if t.id == tarea_id:
            return t
    return None

def eliminar_tarea(tarea_id: int) -> bool:
    tareas = leer_tareas()
    nuevas = [t for t in tareas if t.id != tarea_id]
    if len(nuevas) == len(tareas):
        return False
    guardar_tareas(nuevas)
    return True

def actualizar_tarea(tarea_id: int, datos: Tarea) -> bool:
    tareas = leer_tareas()
    actualizado = False
    for i, t in enumerate(tareas):
        if t.id == tarea_id:
            tareas[i] = datos
            actualizado = True
            break
    if actualizado:
        guardar_tareas(tareas)
    return actualizado

def filtrar_tareas_por_estado(estado: str) -> List[Tarea]:
    tareas = leer_tareas()
    return [t for t in tareas if t.estado.lower() == estado.lower()]

def tareas_por_usuario(user_id: int) -> List[Tarea]:
    tareas = leer_tareas()
    return [t for t in tareas if t.usuario == user_id]

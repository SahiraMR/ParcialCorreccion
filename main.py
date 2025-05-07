from fastapi import FastAPI, HTTPException
from models.usuario import Usuario
from models.tarea import Tarea
from crud.usuario_crud import (
    leer_usuarios, obtener_usuario_por_id, actualizar_usuario
)
from crud.tarea_crud import (
    leer_tareas, obtener_tarea_por_id, agregar_tarea,
    actualizar_tarea, eliminar_tarea, filtrar_tareas_por_estado
)

app = FastAPI(title="API de Usuarios y Tareas")

# -------------------- USUARIOS --------------------

@app.get("/usuarios", response_model=list[Usuario])
def listar_usuarios():
    return leer_usuarios()

@app.get("/usuarios/{user_id}", response_model=Usuario)
def obtener_usuario(user_id: int):
    usuario = obtener_usuario_por_id(user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{user_id}/estado", response_model=Usuario)
def actualizar_estado_usuario(user_id: int, nuevo_estado: str):
    usuario = obtener_usuario_por_id(user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if nuevo_estado not in ["Premium", "Normal", "Inactivo"]:
        raise HTTPException(status_code=400, detail="Estado inválido")
    usuario.tipo = nuevo_estado
    actualizar_usuario(user_id, usuario)
    return usuario

@app.put("/usuarios/{user_id}/hacer-premium", response_model=Usuario)
def hacer_premium(user_id: int):
    usuario = obtener_usuario_por_id(user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.tipo = "Premium"
    actualizar_usuario(user_id, usuario)
    return usuario

@app.get("/usuarios/inactivos", response_model=list[Usuario])
def usuarios_inactivos():
    return [u for u in leer_usuarios() if u.tipo == "Inactivo"]

@app.get("/usuarios/premium", response_model=list[Usuario])
def usuarios_premium():
    return [u for u in leer_usuarios() if u.tipo == "Premium"]

# -------------------- TAREAS --------------------

@app.get("/tareas", response_model=list[Tarea])
def listar_tareas():
    return leer_tareas()

@app.get("/tareas/{tarea_id}", response_model=Tarea)
def obtener_tarea(tarea_id: int):
    tarea = obtener_tarea_por_id(tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.post("/tareas", response_model=Tarea)
def crear_tarea(tarea: Tarea):
    if obtener_tarea_por_id(tarea.id):
        raise HTTPException(status_code=400, detail="ID de tarea ya existe")
    agregar_tarea(tarea)
    return tarea

@app.put("/tareas/{tarea_id}", response_model=Tarea)
def actualizar(tarea_id: int, datos: Tarea):
    if not actualizar_tarea(tarea_id, datos):
        raise HTTPException(status_code=404, detail="No se pudo actualizar")
    return datos

@app.delete("/tareas/{tarea_id}")
def borrar_tarea(tarea_id: int):
    if not eliminar_tarea(tarea_id):
        raise HTTPException(status_code=404, detail="No se pudo eliminar la tarea")
    return {"mensaje": "Tarea eliminada"}

@app.get("/tareas/estado/{estado}", response_model=list[Tarea])
def tareas_por_estado(estado: str):
    resultados = filtrar_tareas_por_estado(estado)
    return resultados

import csv
from typing import List, Optional
from models.usuario import Usuario

RUTA_CSV = "data/usuarios.csv"

def leer_usuarios() -> List[Usuario]:
    usuarios = []
    with open(RUTA_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            usuarios.append(Usuario(**{
                "id": int(row["id"]),
                "nombre": row["nombre"],
                "email": row["email"],
                "edad": int(row["edad"]) if row["edad"] else None,
                "tipo": row["tipo"]
            }))
    return usuarios

def guardar_usuarios(lista: List[Usuario]):
    with open(RUTA_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nombre", "email", "edad", "tipo"])
        writer.writeheader()
        for u in lista:
            writer.writerow(u.dict())

def agregar_usuario(usuario: Usuario):
    usuarios = leer_usuarios()
    usuarios.append(usuario)
    guardar_usuarios(usuarios)

def obtener_usuario_por_id(usuario_id: int) -> Optional[Usuario]:
    usuarios = leer_usuarios()
    for u in usuarios:
        if u.id == usuario_id:
            return u
    return None

def eliminar_usuario(usuario_id: int) -> bool:
    usuarios = leer_usuarios()
    nuevas = [u for u in usuarios if u.id != usuario_id]
    if len(nuevas) == len(usuarios):
        return False
    guardar_usuarios(nuevas)
    return True

def actualizar_usuario(usuario_id: int, datos: Usuario) -> bool:
    usuarios = leer_usuarios()
    actualizado = False
    for i, u in enumerate(usuarios):
        if u.id == usuario_id:
            usuarios[i] = datos
            actualizado = True
            break
    if actualizado:
        guardar_usuarios(usuarios)
    return actualizado

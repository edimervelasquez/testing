from fastapi import FastAPI, HTTPException
import pymysql

app = FastAPI(title="API de Prueba - Usuarios SIES")

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456', 
    'database': 'yullita_creaciones',
    'cursorclass': pymysql.cursors.DictCursor
}

@app.get("/")
def inicio():
    return {"mensaje": "API de prueba funcionando correctamente"}

@app.post("/api/login-rapido")
def login_rapido(correo: str):
    conexion = pymysql.connect(**DB_CONFIG)
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM usuario WHERE correo_usuario = %s"
            cursor.execute(sql, (correo,))
            usuario = cursor.fetchone()
            
            if not usuario:
                raise HTTPException(status_code=404, detail="El correo no existe en la base de datos.")
            
            return {
                "estado": "Éxito",
                "mensaje": f"Bienvenido, {usuario['empleado']}",
                "rol": usuario['id_rol']
            }
    finally:
        conexion.close()

@app.get("/api/usuarios")
def listar_usuarios():
    conexion = pymysql.connect(**DB_CONFIG)
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT id_usuario, correo_usuario, empleado, id_rol FROM usuario"
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            return {
                "total": len(usuarios),
                "usuarios": usuarios
            }
    finally:
        conexion.close()
from fastapi import FastAPI     # importamos fastapi
from routers import products, users, jwt_auth_users, users_db  # con esto tendremos acceso a los endpoint
from fastapi.staticfiles import StaticFiles     # para poder acceder a nuestro archivos estaticos en el proyecto

app = FastAPI()                 # instanciamos fastapi

# Routers
app.include_router(products.router)     #con esto incluimos en router de products
app.include_router(users.router)     #con esto incluimos en router de products
# app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static") 
# la funcion mount nos pide 3 argumentos; el path, el directorio y el nombre para poder exponer nuestros recursos estaticos

# url local: http://127.0.0.1:8000/

@app.get("/")                   # funcion que retorna un mensaje
async def root():
    return "Hola FastAPI"

# url local: http://127.0.0.1:8000/url

@app.get("/url")                # funcion que retorna un json
async def url():
    return {"url_curso":"https://mouredev.com/python"}

# Iniciar el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc

# comando para generar el archivo requirements.txt ~ pip freeze > requirements.txt
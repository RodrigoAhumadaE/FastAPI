from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema     # importamos el esquema
# creamos la carpeta models y dentro de ella el archivo user.py dentro de este archivo definimos nuestra clase User y la importamos para poder utilizarla acá
from db.client import db_client             # importamos la conecciona a base de datos
from bson import ObjectId                   # esto se importa para poder trabajar con el id de mongodb



router = APIRouter(prefix="/userdb", tags={"usersdb"}, responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})


# <<GET>>
# obtener la lista de usuarios
@router.get("/list", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


# llamar por Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))
    

# llamar por Query

@router.get("/")
async def userQuery(id: str):
    return search_user("_id", ObjectId(id))


# <<POST>>
# agregar usuario
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    # comprobamos si el correo existe
    if type(search_user("email",user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    user_dict = dict(user)
    # creamos una variable "user_dict" para poder tranformar nuestro usuario en un diccionario, ya que un json basicamente es un diccionario y mongodb trabaja con json
    del user_dict["id"]         # al crear el usuario si no le enviamos el id, se insertará este campo como null para evitar eso eliminamos este campo

    id = db_client.users.insert_one(user_dict).inserted_id
    # vamos a nuestra conexion a bd en local creamos el esquema o la tabla users u usamos la funcion insert_one para agregar el usuario

    new_user = user_schema(db_client.users.find_one({"_id":id}))       # el nombre de la clave unica creada por mongodb es "_id", conbertimos este json que nos entrrega mongodb en el esquema
    # una vez creado el usuario insertamos el id y lo guardamos en una variable para poder luego confirmar si se creó el usuario consultando el id entregado por la oprecion anterior

    return User(**new_user)
    
    

# <<PUT>>
# actualizar usuario
@router.put("/", response_model=User, status_code=status.HTTP_202_ACCEPTED)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error":"usuario no Actualizado"}
            # return {"message":"Usuario actualizado correctamente"}
    
    return search_user("_id", ObjectId(user.id))
        
    


# DELETE

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "No se ha eliminado el usuario"}


# Funciones

# para que la busqueda sea mas generica definimos un field tipo string que defina el campo y key para que sea dato que buscamos
def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
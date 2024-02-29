from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/user", tags={"users"})

# Iniciar el server: uvicorn users:app --reload

#definimo nuestra entidad user
class User(BaseModel):
    id:int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name="Alex", surname="Draven", url="alexdev.cl", age=18),
              User(id=2, name="Annette", surname="Cardenas", url="Ann.cl", age=20),
              User(id=3, name="Montserrat", surname="Alvarez", url="montse.cl", age=25)]

@router.get("/json")
async def usersjson():
    return [{"name":"Alex", "surname":"Draven"},
            {"name":"Annette", "surname":"Cardenas"},
            {"name":"Montserrat", "surname":"Alvarez"},]

@router.get("/list")
async def users():
    return users_list


# llamar por Path
@router.get("/{id}")
async def user(id: int):
    # users = filter(lambda user: user.id == id, users_list)
    # try:
    #     return list(users)[0]
    # except:
    #     return {"error":"usuario no encontrado"}
    # esto puede ser reducido a una funcion que busque por id para optimizar codigo
    return search_user(id)
    

# llamar por Query

@router.get("/")
async def userQuery(id: int):
    return search_user(id)

# http://127.0.0.1:8000/userquery/?id=1

# funcion search_user
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"usuario no encontrado"}
    


# POST
    
@router.post("/", status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return {"message":"Usuario agregado correctamente"}
    

# PUT

@router.put("/")
async def user(user: User):
    for index, save_user in enumerate(users_list):
        if save_user.id == user.id:
            users_list[index] = user
            return {"message":"Usuario actualizado correctamente"}
        
    return {"error":"usuario no encontrado"}


# DELETE

@router.delete("/{id}")
async def user(id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            return {"message":"usuario borrado correctamente"}
    
    return {"error":"Usuario no encontrado"}
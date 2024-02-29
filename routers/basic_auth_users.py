from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# OAuth2PasswordBearer -> clase que se encarga de gestionar la autenticación
# OAuth2PasswordRequestForm -> forma en la que se envian nuestros criterios de autenticacion a nuestra API

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "AlexDraven": {
        "username": "AlexDraven",
        "full_name": "Alex Draven",
        "email": "alex@mail.cl",
        "disabled": False,
        "password": "123456"
    },
    "Chronoss": {
        "username": "Chronoss",
        "full_name": "Rodrigo Ahumada",
        "email": "chronoss@mail.cl",
        "disabled": False,
        "password": "987654"
    },
    "Chriss": {
        "username": "Chriss",
        "full_name": "Christobal Melendez",
        "email": "chriss@mail.cl",
        "disabled": True,
        "password": "654321"
    }
}

# funcion para obtener un usuario desde la base de datos con el username
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
# creamos un criterio de dependencia
async def current_user(token: str= Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales erroneas",
            headers={"WWW-Authenticate":"Bearer"})
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="usuario inactivo")
    
    return user

# implementamos la operacion de autenticacion
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token":user.username, "token_type":"bearer"}

# implementamos una operacion para obtener datos del usuario una vez autenticados
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
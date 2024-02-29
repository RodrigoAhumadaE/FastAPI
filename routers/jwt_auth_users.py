from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext        # algoritmo de encriptacion
from datetime import datetime, timedelta        # manejo de fechas para la duración del token

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "9ced2982469472e6eb92b8fbe34305d5d6bb3363c4c10e02a6bddc1ff18e1758"

router =APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# concepto de encriptación
crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$hMvC62R6Hti6E1BnKilrpe7gDWkqZD9xnqRl51WrpmbD3nYFdniR2"
    },
    "Chronoss": {
        "username": "Chronoss",
        "full_name": "Rodrigo Ahumada",
        "email": "chronoss@mail.cl",
        "disabled": False,
        "password": "$2a$12$55q7DJYKgmXp2u7i3Ogv5OzHTj5CbUEvczyqUkqnvlCEbkuXfefu6"
    },
    "Chriss": {
        "username": "Chriss",
        "full_name": "Christobal Melendez",
        "email": "chriss@mail.cl",
        "disabled": True,
        "password": "$2a$12$eOjxzA5J2zGjdx.0vH8c0e/k69x8F9MIWiw04JqRcVSzYEBUmJXKO"
    }
}

# funcion para obtener un usuario desde la base de datos con el username
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
# funcion para desencodear el token y obtener el username    
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales erroneas",
            headers={"WWW-Authenticate":"Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return search_user(username)

# Criterio de dependencia   
async def current_user(user: User = Depends(auth_user)):
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

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    # access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)          tiempo de expiracion
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)         momento de expiracion

    access_token = {
        "sub":user.username,
        "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }    

    return {"access_token":jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type":"bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
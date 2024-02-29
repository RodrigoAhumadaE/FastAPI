# definimos una función que recibirá nuestro usuario como objeto y lo transformará en un diccionario para que pueda ser manejado por el modelo que hemos creado
def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]
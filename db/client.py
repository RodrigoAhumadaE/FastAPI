from pymongo import MongoClient           # una vez instalado la librería pymongo creamos el archivo client.py e importamos desde pymongo la clase  MongoClient

# base de datos local
# db_client = MongoClient().local                  # instanciamos MongoClient a la variable db_client, se conecta por defecto a la base de datos en localhost

# base de datos remota
db_client = MongoClient("mongodb+srv://test:test@cluster0.fghi771.mongodb.net/?retryWrites=true&w=majority").test

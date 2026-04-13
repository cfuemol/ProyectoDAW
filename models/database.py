#* Importar módulos necesarios del sistema
import os

#* Importar módulos necesarios de mongoengine
from mongoengine import connect

#* Importar módulos necesarios de la librería dotenv
from dotenv import load_dotenv

#* Carga las variables de entorno
load_dotenv()

#* Inicializa la conexión a la base de datos
def init_db():
    connect(
        db=os.getenv("MONGO_DB"),
        host=f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}:27017/{os.getenv('MONGO_DB')}?authSource=admin"
    )

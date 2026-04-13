#* Importar módulos necesarios de mongoengine
from mongoengine import Document, ReferenceField, StringField

#* Importar modelo (clase) de la base de datos
from .usuario import Usuario

#* Objeto (clase) que representa un saliente
class Saliente(Document):
    profesional = ReferenceField(Usuario, required=True)
    nombre = StringField(required=True)
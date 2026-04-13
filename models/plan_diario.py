#* Importar módulos necesarios de mongoengine
from mongoengine import Document, StringField, IntField

#* Objeto (clase) que representa un plan diario
class PlanDiario(Document):
    nombre = StringField(required=True)
    apellidos = StringField(required=True)
    categoria = StringField(required=True)
    centro = StringField(required=True)
    telefono = IntField(required=True)

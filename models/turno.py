from mongoengine import Document, ReferenceField, DateField, StringField
from .usuario import Usuario

class Turno(Document):
    profesional = ReferenceField(Usuario, required=True)
    fecha = DateField(required=True)
    tipo = StringField(required=True, choices = ["7h", "17h", "24h"])
from mongoengine import Document, ReferenceField, StringField
from .usuario import Usuario

class Saliente(Document):
    profesional = ReferenceField(Usuario, required=True)
    nombre = StringField(required=True)
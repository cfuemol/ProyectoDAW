from mongoengine import Document, ReferenceField, DateField
from .usuario import Usuario

class Cambio(Document):
    profesional1 = ReferenceField(Usuario, required=True)
    profesional2 = ReferenceField(Usuario, required=True)
    fecha_original = DateField(required=True)
    fecha_final = DateField(required=True)
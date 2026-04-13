#* Importar módulos necesarios de mongoengine
from mongoengine import Document, ReferenceField, DateField, StringField, BooleanField

#* Importar modelo (clase) de la base de datos
from .usuario import Usuario

#* Objeto (clase) que representa un cambio entre dos profesionales
class Cambio(Document):
    profesional1 = ReferenceField(Usuario, required=True)
    profesional2 = ReferenceField(Usuario, required=True)
    fecha_original = DateField(required=True)
    fecha_final = DateField(required=True)
    tipo_p1 = StringField(required=True)
    tipo_p2 = StringField(required=True)
    estado = StringField(default='pendiente', choices=['pendiente', 'aceptado', 'rechazado'])
    visto_por_direccion = BooleanField(default=False)
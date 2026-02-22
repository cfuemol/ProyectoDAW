from mongoengine import Document, StringField, IntField
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(Document):
    
    #* Datos personales del profesional
    dni = StringField(required=True, unique=True)
    nombre = StringField(required=True)
    apellidos = StringField(required=True)
    categoria = StringField(required=True)
    centro_asignado = StringField(required=True)
    telefono = IntField(required=True)

    #* Datos de acceso
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

    #* Rol en el sistema
    rol = StringField(required=True, choices=['administrador', 'profesional', 'mostrador', 'direccion'])

    #* Métodos de Seguridad
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
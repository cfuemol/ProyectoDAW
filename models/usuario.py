from mongoengine import Document, StringField, IntField
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(Document):
    meta = {'collection': 'usuarios'}
    
    #* Datos personales del profesional
    nombre = StringField(required=True)
    apellidos = StringField(required=True)
    categoria = StringField(required=True, unique=True)
    centro_asignado = StringField(required=True, unique=True)
    telefono = IntField(required=True, unique=True)
    email = StringField(required=True, unique=True)

    #* Datos de acceso
    dni = StringField(required=True, unique=True)
    password_hash = StringField(required=True)

    #* Rol en el sistema
    rol = StringField(required=True, choices=['administrador', 'profesional', 'mostrador', 'direccion'])

    #* Métodos de Seguridad
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
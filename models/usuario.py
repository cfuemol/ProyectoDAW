from mongoengine import Document, StringField, IntField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(Document):
    meta = {'collection': 'usuarios'}
    
    #* Datos personales del profesional
    nombre = StringField(required=True)
    apellidos = StringField(required=True)
    categoria = StringField(required=True)
    unidad_asignada = StringField(required=True, choices=['ZBS Albuñol', 'ZBS Motril', 'Dispositivo Apoyo Granada', 'ZBS Almuñecar', 'SAS', 'Dispositivo Apoyo Granada Sur'])
    centro_asignado = StringField(required=True)
    telefono = IntField(required=True)
    email = StringField(required=True, unique=True)

    #* Datos de acceso
    dni = StringField(required=True, unique=True)
    password_hash = StringField(required=True)

    #* Rol en el sistema
    rol = StringField(required=True, choices=['administrador', 'profesional', 'direccion'])

    #* Gestión de Salientes
    es_saliente = BooleanField(default=False)
    total_salientes = IntField(default=0)

    #* Métodos de Seguridad
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
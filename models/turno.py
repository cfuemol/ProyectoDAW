#* Importar módulos necesarios de mongoengine
from mongoengine import Document, ReferenceField, DateField, StringField

#* Importar modelo (clase) de la base de datos
from .usuario import Usuario

#* Objeto (clase) que representa un turno
class Turno(Document):
    profesional = ReferenceField(Usuario, required=True)
    fecha = DateField(required=True)
    tipo = StringField(required=True, choices = ["7h", "17h", "24h"])
    centro_especial = StringField() # Para casos como salientes o coberturas

    #* Método que devuelve el centro de trabajo
    @property #* Indica que es un método que se comporta como un atributo de solo lectura
    def centro_trabajo(self):
        if self.centro_especial:
            return self.centro_especial
        if self.tipo == "24h" and self.fecha.weekday() < 5:
            return f"{self.profesional.centro_asignado} + Urgencias"
        elif self.tipo in ["17h", "24h"]:
            return "Urgencias Albuñol"
        else:
            return self.profesional.centro_asignado
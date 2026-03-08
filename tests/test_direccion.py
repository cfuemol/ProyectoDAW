import pytest
from models.usuario import Usuario
from models.turno import Turno
from flask import session
from datetime import datetime

def test_direccion_registration_restrictions(client):
    """Verificar que Dirección tiene restricciones de rol y unidad."""
    with client.session_transaction() as sess:
        sess['rol'] = 'direccion'
        sess['dni'] = 'DIR001'

    # 1. Intentar registrar un administrador (Bloqueado)
    data_admin = {
        'dni': '12345678Z',
        'nombre': 'Administrador',
        'apellidos': 'Denegado Por Permisos',
        'categoria': 'profesional',
        'centro_asignado': 'Albuñol',
        'telefono': '600000001',
        'email': 'adminpro@test.com',
        'password': 'Pass123!#',
        'rol': 'administrador',
        'unidad_asignada': 'SAS'
    }
    response = client.post('/register', data=data_admin, follow_redirects=True)
    assert "No tienes permisos" in response.get_data(as_text=True)

    # 2. Registrar con unidad no permitida para Dirección (Bloqueado)
    data_invalid_unit = {
        'dni': '87654321X', 
        'nombre': 'Unidad',
        'apellidos': 'No Valida',
        'categoria': 'Médico/a',
        'centro_asignado': 'Motril',
        'telefono': '600000003',
        'email': 'invalidunit@test.com',
        'password': 'Pass123!#',
        'rol': 'profesional',
        'unidad_asignada': 'ZBS Motril'
    }
    response = client.post('/register', data=data_invalid_unit, follow_redirects=True)
    assert "unidad asignada no es válida" in response.get_data(as_text=True)

    # 3. Registrar con "Dispositivo Apoyo Granada Sur" (Válido, fuerza centro)
    data_dispositivo = {
        'dni': '88888888Y', 
        'nombre': 'Profesional',
        'apellidos': 'Dispositivo',
        'categoria': 'DUE',
        'centro_asignado': 'Albuñol', # Intentamos poner otro centro
        'telefono': '611222333',
        'email': 'dispo@test.com',
        'password': 'Pass123!#',
        'rol': 'profesional',
        'unidad_asignada': 'Dispositivo Apoyo Granada Sur'
    }
    response = client.post('/register', data=data_dispositivo, follow_redirects=True)
    assert "Usuario añadido correctamente" in response.get_data(as_text=True)
    
    user = Usuario.objects(dni='88888888Y').first()
    assert user.unidad_asignada == 'Dispositivo Apoyo Granada Sur'
    assert user.centro_asignado == 'Dispositivo Apoyo Granada Sur' # Forzado

def test_direccion_cannot_delete_users(client):
    """Verificar que Dirección no tiene acceso a borrar usuarios."""
    # Crear un usuario para intentar borrar
    Usuario(dni='11111111B', nombre='Test', apellidos='User', categoria='DUE', 
            unidad_asignada='ZBS Albuñol', centro_asignado='Albuñol', telefono=666555444,
            email='testborrar@test.com', rol='profesional', password_hash='...').save()

    with client.session_transaction() as sess:
        sess['rol'] = 'direccion'
    
    # Intentar borrar (redirect a / si no tiene rol)
    response = client.post('/borrar_usuario/11111111B', follow_redirects=True)
    assert Usuario.objects(dni='11111111B').first() is not None

def test_gestion_turnos_batch_insertion(client):
    """Probar inserción de turnos por lotes por Dirección."""
    prof = Usuario(dni='22222222T', nombre='Turno', apellidos='User', categoria='DUE', 
                   unidad_asignada='ZBS Albuñol', centro_asignado='Centro Test', telefono=666555444,
                   email='testbatch@test.com', rol='profesional', password_hash='...').save()

    with client.session_transaction() as sess:
        sess['rol'] = 'direccion'
    
    data = {
        'profesional_dni[]': ['22222222T', '22222222T'],
        'fecha[]': ['2026-03-09', '2026-03-10'], # Lunes y Martes
        'tipo[]': ['7h', '17h']
    }
    response = client.post('/gestion_turnos', data=data, follow_redirects=True)
    assert "Se han procesado 2 turnos correctamente" in response.get_data(as_text=True)
    
    turnos = Turno.objects(profesional=prof)
    assert turnos.count() == 2
    
    # Verificar ubicación en el HTML (opcional pero bueno)
    response_get = client.get('/gestion_turnos')
    html = response_get.get_data(as_text=True)
    assert "Centro Test" in html # Ubicación para 7h
    assert "Urgencias Albuñol" in html # Ubicación para 17h

def test_descargar_pdf_dia(client):
    """Verificar que la descarga de PDF funciona."""
    # Asegurar que hay al menos un turno hoy que cumpla con las reglas
    prof = Usuario.objects(dni='22222222T').first()
    hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    Turno.objects(profesional=prof, fecha=hoy).delete()
    # Hoy es Domingo, así que usamos 24h para cumplir la nueva regla
    Turno(profesional=prof, fecha=hoy, tipo='24h').save()

    with client.session_transaction() as sess:
        sess['rol'] = 'direccion'
    
    response = client.get('/descargar_pdf_dia')
    assert response.status_code == 200
    assert response.mimetype == 'application/pdf'
def test_validacion_descanso_post_guardia(client):
    """Verificar que no se puede asignar un turno el día después de una guardia."""
    prof = Usuario.objects(dni='22222222T').first()
    
    # 1. Asignar guardia el día 10
    fecha_guardia = datetime(2026, 3, 10)
    Turno(profesional=prof, fecha=fecha_guardia, tipo='24h').save()
    
    with client.session_transaction() as sess:
        sess['rol'] = 'direccion'
    
    # 2. Intentar asignar turno el día 11 (Debe fallar)
    data = {
        'profesional_dni[]': ['22222222T'],
        'fecha[]': ['2026-03-11'],
        'tipo[]': ['7h']
    }
    response = client.post('/gestion_turnos', data=data, follow_redirects=True)
    assert "debe descansar el 11/03/2026" in response.get_data(as_text=True)
    
    # Verificar que el turno del día 11 no se guardó
    turno_dia_11 = Turno.objects(profesional=prof, fecha=datetime(2026, 3, 11)).first()
def test_restriccion_fin_de_semana(client):
    """Verificar que en fin de semana solo se permiten turnos de 24h."""
    prof = Usuario.objects(dni='22222222T').first()
    
    # Sábado 14 de marzo 2026
    fecha_sabado = '2026-03-14'
    
    with client.session_transaction() as sess:
        sess['rol'] = 'direccion'
    
    # 1. Intentar asignar 17h en sábado (Debe fallar)
    data_fail = {
        'profesional_dni[]': ['22222222T'],
        'fecha[]': [fecha_sabado],
        'tipo[]': ['17h']
    }
    response = client.post('/gestion_turnos', data=data_fail, follow_redirects=True)
    assert "Solo se permiten turnos de 24h" in response.get_data(as_text=True)
    
    # 2. Asignar 24h en sábado (Debe pasar)
    data_pass = {
        'profesional_dni[]': ['22222222T'],
        'fecha[]': [fecha_sabado],
        'tipo[]': ['24h']
    }
    response = client.post('/gestion_turnos', data=data_pass, follow_redirects=True)
    assert "Se han procesado 1 turnos correctamente" in response.get_data(as_text=True)
    
    # 3. Intentar modificar el turno del sábado a 7h (Debe fallar)
    turno = Turno.objects(profesional=prof, fecha=datetime(2026, 3, 14)).first()
    response = client.post(f'/modificar_turno/{turno.id}', data={'tipo': '7h'}, follow_redirects=True)
    assert "Solo se permiten turnos de 24h" in response.get_data(as_text=True)
    assert Turno.objects(id=turno.id).first().tipo == '24h'

def test_restricciones_categoria(client):
    """Verificar las reglas específicas por categoría profesional."""
    # 1. Celadores: Solo 24h
    celador = Usuario(
        nombre="Juan", apellidos="Celador", categoria="Celador/a-Conductor/a",
        unidad_asignada="ZBS Albuñol", centro_asignado="Albuñol",
        telefono=600111222, email="juan@celador.com", dni="11111111H", rol="profesional"
    )
    celador.set_password("pass")
    celador.save()

    with client.session_transaction() as sess:
        sess['rol'] = 'direccion'

    # Intentar asignar 7h a celador (debe fallar)
    response = client.post('/gestion_turnos', data={
        'profesional_dni[]': ['11111111H'],
        'fecha[]': ['2026-03-09'], # Lunes
        'tipo[]': ['7h']
    }, follow_redirects=True)
    assert "solo puede realizar turnos de 24h" in response.get_data(as_text=True)

    # 2. Administrativos/Consulta: Solo 7h y L-V
    admin = Usuario(
        nombre="Ana", apellidos="Admin", categoria="Administrativo/a",
        unidad_asignada="ZBS Albuñol", centro_asignado="Albuñol",
        telefono=600333444, email="ana@admin.com", dni="33333333L", rol="profesional"
    )
    admin.set_password("pass")
    admin.save()

    # Intentar asignar 17h a administrativo (debe fallar)
    response = client.post('/gestion_turnos', data={
        'profesional_dni[]': ['33333333L'],
        'fecha[]': ['2026-03-09'], # Lunes
        'tipo[]': ['17h']
    }, follow_redirects=True)
    assert "solo puede realizar turnos de 7h" in response.get_data(as_text=True)

    # Intentar asignar 7h en Sábado a administrativo (debe fallar)
    response = client.post('/gestion_turnos', data={
        'profesional_dni[]': ['33333333L'],
        'fecha[]': ['2026-03-14'], # Sábado
        'tipo[]': ['7h']
    }, follow_redirects=True)
    out = response.get_data(as_text=True)
    assert "solo trabaja de Lunes a Viernes" in out, f"ERROR: Mensaje no encontrado en HTML: {out[:500]}..."

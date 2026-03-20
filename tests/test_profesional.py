import pytest
from models.usuario import Usuario
from models.turno import Turno
from models.cambio import Cambio
from datetime import datetime, timedelta
from flask import session
import re


# ===================================================
#  HELPERS
# ===================================================

def crear_profesional(dni, nombre, apellidos, categoria='Médico/a', email=None, telefono=600000000):
    email = email or f'{dni.lower()}@test.com'
    return Usuario(
        dni=dni,
        nombre=nombre,
        apellidos=apellidos,
        categoria=categoria,
        unidad_asignada='ZBS Albuñol',
        centro_asignado='Albuñol',
        telefono=telefono,
        email=email,
        rol='profesional',
        password_hash='...'
    ).save()


# ===================================================
#  ACCESO Y DASHBOARD
# ===================================================

def test_acceso_sin_sesion_redirige(client):
    """Las rutas protegidas deben redirigir si no hay sesión."""
    for ruta in ['/profesional_dashboard', '/profesional/ver_cuadrante',
                 '/profesional/pedir_cambio', '/profesional/solicitudes_cambio',
                 '/profesional/historico_cambios']:
        resp = client.get(ruta, follow_redirects=True)
        assert resp.status_code == 200
        # No debe mostrar contenido protegido
        assert 'Panel Profesional' not in resp.get_data(as_text=True)


def test_profesional_dashboard_access(client):
    """Verificar acceso al dashboard de profesional."""
    crear_profesional('PROF001', 'Juan', 'Perez Test')

    with client.session_transaction() as sess:
        sess['rol'] = 'profesional'
        sess['dni'] = 'PROF001'

    response = client.get('/profesional_dashboard')
    assert response.status_code == 200
    assert "Panel Profesional" in response.get_data(as_text=True)


# ===================================================
#  CUADRANTE
# ===================================================

def test_ver_cuadrante_mensual(client):
    """Verificar que el profesional puede ver su cuadrante."""
    prof = crear_profesional('PROF002', 'Ana', 'Sanz Test', categoria='DUE', telefono=600000001,
                             email='anasanz@test.com')
    hoy = datetime.now()
    Turno(profesional=prof, fecha=hoy, tipo='17h').save()

    with client.session_transaction() as sess:
        sess['rol'] = 'profesional'
        sess['dni'] = 'PROF002'

    response = client.get(f'/profesional/ver_cuadrante?mes={hoy.month}&anio={hoy.year}')
    assert response.status_code == 200
    assert "Urgencias Albuñol" in response.get_data(as_text=True)


def test_cuadrante_sin_turnos(client):
    """Cuadrante sin turnos debe mostrar mensaje informativo."""
    crear_profesional('PROF005', 'Pedro', 'Ruiz Test', email='pedro@test.com', telefono=600000005)

    with client.session_transaction() as sess:
        sess['rol'] = 'profesional'
        sess['dni'] = 'PROF005'

    response = client.get('/profesional/ver_cuadrante?mes=1&anio=2099')
    assert response.status_code == 200
    assert "No hay turnos registrados" in response.get_data(as_text=True)


# ===================================================
#  DESCARGA DE PDF
# ===================================================

def test_descargar_pdf_mensual(client):
    """Verificar que el profesional puede descargar su PDF mensual."""
    prof = crear_profesional('PROF003', 'Luis', 'Lopez Test', email='luis@test.com', telefono=600000002)
    hoy = datetime.now()
    Turno(profesional=prof, fecha=hoy, tipo='24h').save()

    with client.session_transaction() as sess:
        sess['rol'] = 'profesional'
        sess['dni'] = 'PROF003'

    response = client.get(f'/profesional/descargar_pdf?mes={hoy.month}&anio={hoy.year}')
    assert response.status_code == 200
    assert response.mimetype == 'application/pdf'
    assert 'attachment' in response.headers['Content-Disposition']

    # El servidor usa el nombre del mes en español (Capitalizado)
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_nombre = meses[hoy.month - 1]
    assert f'turnos_Luis_{mes_nombre}_{hoy.year}' in response.headers['Content-Disposition']


# ===================================================
#  CONTRASEÑA
# ===================================================

def test_cambiar_password_validacion(client):
    """Probar las reglas de complejidad al cambiar contraseña."""
    crear_profesional('PROF004', 'Elena', 'Gomez Test', categoria='DUE',
                      email='elena@test.com', telefono=600000003)

    with client.session_transaction() as sess:
        sess['rol'] = 'profesional'
        sess['dni'] = 'PROF004'

    # 1. Contraseña débil (sin mayúscula ni símbolo)
    response = client.post('/cambiar_password', data={
        'new_password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    assert "La contraseña debe tener entre 8 y 12 caracteres" in response.get_data(as_text=True)

    # 2. Contraseña válida (Mayús + Minús + Número + Símbolo, 8-12 chars)
    response = client.post('/cambiar_password', data={
        'new_password': 'Valid123!',
        'confirm_password': 'Valid123!'
    }, follow_redirects=True)
    assert "Contraseña actualizada correctamente" in response.get_data(as_text=True)


# ===================================================
#  SOLICITUDES DE CAMBIO
# ===================================================

def test_categoria_no_permitida_no_accede_a_pedir_cambio(client):
    """Categorías sin permiso (ej. TCAE) deben ser redirigidas al dashboard."""
    crear_profesional('TCAE001', 'Marta', 'Torres Test', categoria='TCAE',
                      email='marta@test.com', telefono=600000006)

    with client.session_transaction() as sess:
        sess['rol'] = 'profesional'
        sess['dni'] = 'TCAE001'

    response = client.get('/profesional/pedir_cambio', follow_redirects=True)
    assert response.status_code == 200
    # Redirige al dashboard, no muestra la página de pedir cambio
    assert "Panel Profesional" in response.get_data(as_text=True)


def test_pedir_cambio_turno_exitoso(client):
    """Verificar que se puede crear una solicitud de cambio de turno válida."""
    prof1 = crear_profesional('CAMB001', 'Carlos', 'Medico Uno', categoria='Médico/a',
                              email='carlos@test.com', telefono=600000010)
    prof2 = crear_profesional('CAMB002', 'Sofia', 'Medico Dos', categoria='Médico/a',
                              email='sofia@test.com', telefono=600000011)

    # Turnos futuros para que sean elegibles
    fecha1 = datetime.now() + timedelta(days=10)
    fecha2 = datetime.now() + timedelta(days=20)
    t1 = Turno(profesional=prof1, fecha=fecha1, tipo='17h').save()
    t2 = Turno(profesional=prof2, fecha=fecha2, tipo='24h').save()

    with client.session_transaction() as sess:
        sess['rol'] = 'profesional'
        sess['dni'] = 'CAMB001'

    response = client.post('/profesional/pedir_cambio', data={
        'mi_turno_id': str(t1.id),
        'companero_dni': 'CAMB002',
        'companero_turno_id': str(t2.id)
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Solicitud de cambio enviada correctamente" in response.get_data(as_text=True)
    assert Cambio.objects(profesional1=prof1, profesional2=prof2).count() == 1


def test_responder_cambio_rechazar(client):
    """Verificar que el profesional 2 puede rechazar una solicitud."""
    prof1 = crear_profesional('RESP001', 'Alicia', 'Medico Tres', categoria='DUE',
                              email='alicia@test.com', telefono=600000020)
    prof2 = crear_profesional('RESP002', 'Pablo', 'Medico Cuatro', categoria='DUE',
                              email='pablo@test.com', telefono=600000021)

    fecha1 = datetime.now() + timedelta(days=5)
    fecha2 = datetime.now() + timedelta(days=15)

    cambio = Cambio(
        profesional1=prof1,
        profesional2=prof2,
        fecha_original=fecha1.date(),
        fecha_final=fecha2.date(),
        tipo_p1='17h',
        tipo_p2='17h',
        estado='pendiente'
    ).save()

    with client.session_transaction() as sess:
        sess['rol'] = 'profesional'
        sess['dni'] = 'RESP002'

    response = client.post(f'/profesional/responder_cambio/{cambio.id}/rechazar',
                           follow_redirects=True)
    assert response.status_code == 200
    assert "rechazado" in response.get_data(as_text=True)
    assert Cambio.objects(id=cambio.id).first().estado == 'rechazado'


def test_solicitudes_cambio_pendientes(client):
    """Verificar que se muestran las solicitudes pendientes dirigidas al usuario."""
    prof1 = crear_profesional('SOL001', 'Diego', 'Medico Cinco', categoria='Médico/a',
                              email='diego@test.com', telefono=600000030)
    prof2 = crear_profesional('SOL002', 'Laura', 'Medico Seis', categoria='Médico/a',
                              email='laura@test.com', telefono=600000031)

    fecha1 = datetime.now() + timedelta(days=5)
    fecha2 = datetime.now() + timedelta(days=15)

    Cambio(
        profesional1=prof1, profesional2=prof2,
        fecha_original=fecha1.date(), fecha_final=fecha2.date(),
        tipo_p1='17h', tipo_p2='24h', estado='pendiente'
    ).save()

    with client.session_transaction() as sess:
        sess['rol'] = 'profesional'
        sess['dni'] = 'SOL002'

    response = client.get('/profesional/solicitudes_cambio')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    # La solicitud del prof1 a prof2 debe aparecer
    assert "Diego" in html


def test_historico_cambios_aceptados(client):
    """Verificar que el histórico muestra cambios aceptados del usuario."""
    prof1 = crear_profesional('HIST001', 'Raul', 'Historico Uno', categoria='DUE',
                              email='raul@test.com', telefono=600000040)
    prof2 = crear_profesional('HIST002', 'Carmen', 'Historico Dos', categoria='DUE',
                              email='carmen@test.com', telefono=600000041)

    fecha1 = datetime.now() - timedelta(days=10)
    fecha2 = datetime.now() - timedelta(days=5)

    Cambio(
        profesional1=prof1, profesional2=prof2,
        fecha_original=fecha1.date(), fecha_final=fecha2.date(),
        tipo_p1='17h', tipo_p2='17h', estado='aceptado'
    ).save()

    with client.session_transaction() as sess:
        sess['rol'] = 'profesional'
        sess['dni'] = 'HIST001'

    response = client.get('/profesional/historico_cambios')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Histórico de Cambios" in html
    assert "Carmen" in html

import pytest
from models.usuario import Usuario
from flask import session

def test_admin_access_required(client):
    """Verificar que las rutas de admin redirigen si no hay sesión iniciada."""
    response = client.get('/admin_dashboard', follow_redirects=True)
    assert response.status_code == 200
    # Como no hay sesión, requiere_rol redirige a /
    assert b"Panel de Administrador" not in response.data

def test_user_registration_logic(client):
    """Probar el registro de un nuevo usuario con datos válidos."""
    # Simular sesión de administrador
    with client.session_transaction() as sess:
        sess['rol'] = 'administrador'
        sess['dni'] = '12345678A'

    # Datos válidos (Nombre y Apellidos >= 6 letras, Pass compleja, Email inicio letra)
    data = {
        'dni': '87654321X',
        'nombre': 'Alberto',
        'apellidos': 'García López',
        'categoria': 'profesional',
        'centro_asignado': 'ZBS Motril',
        'telefono': '600000001',
        'email': 'alberto@test.com',
        'password': 'Pass123!#',
        'rol': 'profesional',
        'unidad_asignada': 'SAS'
    }
    
    # Mock de la base de datos ya está activo por conftest
    response = client.post('/register', data=data, follow_redirects=True)
    assert "Usuario añadido correctamente" in response.get_data(as_text=True)
    
    # Verificar en "BD"
    user = Usuario.objects(dni='87654321X').first()
    assert user is not None
    assert user.nombre == "Alberto"


def test_user_deletion(client):
    """Probar que un administrador puede borrar un usuario."""
    # Crear usuario previo
    from werkzeug.security import generate_password_hash
    u = Usuario(
        dni='12345678Z', 
        nombre='Manuela', 
        apellidos='Del Campo Largo',
        categoria='profesional',
        centro_asignado='ZBS Motril',
        unidad_asignada='SAS',
        telefono=666777888,
        email='manuela@test.com',
        rol='profesional',
        password_hash=generate_password_hash('Pass123!#')
    ).save()

    with client.session_transaction() as sess:
        sess['rol'] = 'administrador'
        sess['dni'] = 'ADMIN001' # Otro DNI para no borrarse a sí mismo

    client.post(f'/borrar_usuario/12345678Z')
    with client.session_transaction() as sess:
        flashes = sess.get('_flashes', [])
        assert any("borrado exitosamente" in f[1] for f in flashes)
    assert Usuario.objects(dni='12345678Z').first() is None

def test_short_name_registration(client):
    """Verificar regla de nombres >= 6 caracteres."""
    with client.session_transaction() as sess:
        sess['rol'] = 'administrador'
    
    data = {
        'dni': '22222222J',
        'nombre': 'Ana', # < 6
        'apellidos': 'Sanz', # < 6
        'categoria': 'profesional',
        'centro_asignado': 'ZBS Motril',
        'telefono': '600000003',
        'email': 'ana@test.com',
        'password': 'ValidPass1!',
        'rol': 'profesional',
        'unidad_asignada': 'SAS'
    }
    
    client.post('/register', data=data)
    with client.session_transaction() as sess:
        flashes = sess.get('_flashes', [])
        assert any("al menos 6 caracteres" in f[1] for f in flashes)

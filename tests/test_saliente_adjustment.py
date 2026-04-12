import pytest
from models.usuario import Usuario
from models.turno import Turno
from models.cambio import Cambio
from datetime import datetime, timedelta
import random

def crear_profesional(dni, nombre, apell, cat='Médico/a', es_saliente=False):
    return Usuario(
        dni=dni,
        nombre=nombre,
        apellidos=apell,
        categoria=cat,
        unidad_asignada='ZBS Albuñol',
        centro_asignado='Albuñol',
        telefono=600000000 + random.randint(100, 999),
        email=f'{dni.lower()}@test.com',
        rol='profesional',
        es_saliente=es_saliente,
        password_hash='pbkdf2:sha256:...' # Requerido por el modelo
    ).save()

def test_saliente_ajuste_cambio_exitoso(client):
    """
    Verifica que al intercambiar dos guardias (L-J), los salientes antiguos se borran
    y se crean los nuevos para los nuevos dueños.
    """
    # 1. Preparar usuarios
    p1 = crear_profesional('P111', 'Juan', 'Primero')
    p2 = crear_profesional('P222', 'Ana', 'Segunda')
    p_sal = crear_profesional('PSAL', 'Pedro', 'Saliente', es_saliente=True)

    # 2. Asignar guardias en días que GENERAN saliente (ej: Lunes y Martes)
    # Buscamos un lunes próximo
    lunes = datetime.now() + timedelta(days=(7 - datetime.now().weekday()) % 7 + 7) # Siguiente lunes
    martes = lunes + timedelta(days=1)
    
    # Simular la creación de turnos desde la app para que dispare asignar_saliente_automatico
    # Como son guardias, la lógica de app.py debería asignar salientes
    # Usaremos el cliente para publicar los turnos si hay un endpoint, o llamaremos a la función directamente
    from app import asignar_saliente_automatico
    
    t1 = Turno(profesional=p1, fecha=lunes, tipo='24h').save()
    asignar_saliente_automatico(t1)
    
    t2 = Turno(profesional=p2, fecha=martes, tipo='24h').save()
    asignar_saliente_automatico(t2)

    # 3. Verificar que existen los salientes iniciales
    # Saliente de P1 (martes) y Saliente de P2 (miércoles)
    sal_p1 = Turno.objects(tipo='7h', fecha=lunes + timedelta(days=1), centro_especial__contains=f"Saliente de {p1.nombre}").first()
    sal_p2 = Turno.objects(tipo='7h', fecha=martes + timedelta(days=1), centro_especial__contains=f"Saliente de {p2.nombre}").first()
    
    assert sal_p1 is not None
    assert sal_p2 is not None
    assert sal_p1.profesional == p_sal
    assert sal_p2.profesional == p_sal

    # 4. Simular el cambio de turno (P1 le da lunes a P2, P2 le da martes a P1)
    cambio = Cambio(
        profesional1=p1,
        profesional2=p2,
        fecha_original=lunes,
        fecha_final=martes,
        tipo_p1='24h',
        tipo_p2='24h',
        estado='pendiente'
    ).save()

    with client.session_transaction() as sess:
        sess['dni'] = p2.dni
        sess['rol'] = 'profesional'

    # Aceptar el cambio
    response = client.post(f'/profesional/responder_cambio/{cambio.id}/aceptar', follow_redirects=True)
    assert response.status_code == 200

    # 5. VERIFICACIÓN FINAL
    # Los salientes antiguos deben haber desaparecido
    assert Turno.objects(id=sal_p1.id).first() is None
    assert Turno.objects(id=sal_p2.id).first() is None

    # Deben existir salientes nuevos con los nombres cambiados
    # Ahora el lunes es de P2, por tanto el martes debe haber un saliente de P2
    # El martes es de P1, por tanto el miércoles debe haber un saliente de P1
    
    nuevo_sal_p2 = Turno.objects(tipo='7h', fecha=lunes + timedelta(days=1), centro_especial__contains=f"Saliente de {p2.nombre}").first()
    nuevo_sal_p1 = Turno.objects(tipo='7h', fecha=martes + timedelta(days=1), centro_especial__contains=f"Saliente de {p1.nombre}").first()

    assert nuevo_sal_p2 is not None, "El saliente para el nuevo dueño del lunes (P2) no se creó"
    assert nuevo_sal_p1 is not None, "El saliente para el nuevo dueño del martes (P1) no se creó"

def test_saliente_ajuste_fin_de_semana(client):
    """
    Verifica que si un cambio involucra un día que NO genera saliente (ej: Viernes),
    no se cree saliente erróneamente.
    """
    p1 = crear_profesional('P333', 'Luis', 'Tercero')
    p2 = crear_profesional('P444', 'Marta', 'Cuarta')
    p_sal = crear_profesional('PSAL2', 'Pedro2', 'Saliente2', es_saliente=True)

    # Buscamos un Jueves (genera saliente Viernes) y un Viernes (NO genera saliente Sábado)
    lunes = datetime.now() + timedelta(days=(7 - datetime.now().weekday()) % 7 + 7)
    jueves = lunes + timedelta(days=3)
    viernes = lunes + timedelta(days=4)
    
    from app import asignar_saliente_automatico
    
    t_jue = Turno(profesional=p1, fecha=jueves, tipo='17h').save()
    asignar_saliente_automatico(t_jue)
    
    t_vie = Turno(profesional=p2, fecha=viernes, tipo='17h').save()
    asignar_saliente_automatico(t_vie)

    # Verificar salientes iniciales
    sal_jue = Turno.objects(tipo='7h', fecha=viernes, centro_especial__contains=f"Saliente de {p1.nombre}").first()
    sal_vie = Turno.objects(tipo='7h', fecha=viernes + timedelta(days=1), centro_especial__contains=f"Saliente de {p2.nombre}").first()
    
    assert sal_jue is not None, "Jueves debería tener saliente el Viernes"
    assert sal_vie is None, "Viernes NO debería tener saliente el Sábado"

    # Cambiar Jueves de P1 por Viernes de P2
    cambio = Cambio(
        profesional1=p1,
        profesional2=p2,
        fecha_original=jueves,
        fecha_final=viernes,
        tipo_p1='17h',
        tipo_p2='17h',
        estado='pendiente'
    ).save()

    with client.session_transaction() as sess:
        sess['dni'] = p2.dni
        sess['rol'] = 'profesional'

    client.post(f'/profesional/responder_cambio/{cambio.id}/aceptar', follow_redirects=True)

    # Resultados esperados:
    # 1. El saliente de P1 del viernes debe haber desaparecido.
    # 2. Debe haber un saliente de P2 el viernes (porque ahora P2 hace el jueves).
    # 3. NO debe haber saliente el sábado para P1 (porque ahora P1 hace el viernes).

    assert Turno.objects(id=sal_jue.id).first() is None
    
    nuevo_sal_p2 = Turno.objects(tipo='7h', fecha=viernes, centro_especial__contains=f"Saliente de {p2.nombre}").first()
    assert nuevo_sal_p2 is not None, "P2 ahora hace el Jueves, debería tener saliente el Viernes"

    sal_sab_p1 = Turno.objects(tipo='7h', fecha=viernes + timedelta(days=1), centro_especial__contains=f"Saliente de {p1.nombre}").first()
    assert sal_sab_p1 is None, "P1 ahora hace el Viernes, NO debería tener saliente el Sábado"

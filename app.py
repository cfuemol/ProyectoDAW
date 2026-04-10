from flask import Flask, render_template, request, redirect, session, url_for, flash, send_file
import os
import io
from datetime import datetime, timedelta
from fpdf import FPDF
from models.database import init_db
from models.usuario import Usuario
from models.turno import Turno
from models.cambio import Cambio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

#* Registro de usuarios activos: {dni: datetime_ultimo_ping}
usuarios_activos = {}

#* Inicializar MongoDB (evitar en tests)
if __name__ == "__main__" or "pytest" not in str(os.environ):
    init_db()

#*-------------------------------------------------------------------------------------
#* COMPROBAR EL ROL CON EL QUE SE ACCEDE (CIERTAS ACCIONES ESTÁN RESTRINGIDAS)
#*-------------------------------------------------------------------------------------
def requiere_rol(*roles):
    def decorador(func):
        def wrapper(*args, **kwargs):
            if session.get('rol') not in roles:
                return redirect('/')
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__ # Hace que el nombre del wrapper sea el mismo que el de la función original
        return wrapper
    return decorador

#*---------------------------------------------------
#* FUNCIONES AUXILIARES
#*---------------------------------------------------

def validar_descanso_reutilizable(usuario, fecha_nueva, fecha_a_soltar):
    """
    Comprueba si un usuario puede realizar un turno en fecha_nueva
    considerando que va a soltar su turno en fecha_a_soltar.
    Retorna (boolean, mensaje)
    """
    dia_antes = fecha_nueva - timedelta(days=1)
    dia_despues = fecha_nueva + timedelta(days=1)
    
    # Buscamos otros turnos del usuario en esos días (ignorando el que va a soltar)
    conflictos = Turno.objects(
        profesional=usuario, 
        fecha__in=[dia_antes, dia_despues, fecha_nueva],
        tipo__in=["17h", "24h"]
    ).filter(fecha__ne=fecha_a_soltar)

    if conflictos.first():
        return False, "no cumpliría el descanso obligatorio de 1 día con sus otros turnos."
    
    return True, ""

import re
import random

def eliminar_saliente_previo(profesional_descanso, fecha_descanso):
    """Elimina el turno de 7h de saliente si existía para cubrir a este profesional este día."""
    # Buscamos turnos de 7h que tengan el centro_especial marcado con la referencia al profesional
    Turno.objects(tipo="7h", fecha=fecha_descanso, centro_especial__contains=f"Saliente de {profesional_descanso.nombre}").delete()

def asignar_saliente_automatico(turno_guardia):
    """Asigna un saliente para cubrir el descanso de una guardia."""
    if turno_guardia.tipo == "7h":
        return
    
    fecha_descanso = turno_guardia.fecha + timedelta(days=1)
    # L(0), M(1), X(2), J(3), V(4), S(5), D(6)
    # Solo si el descanso cae de Lunes a Viernes
    if fecha_descanso.weekday() > 4:
        return

    # Buscar candidatos salientes de la misma categoría
    candidatos = Usuario.objects(
        es_saliente=True, 
        categoria=turno_guardia.profesional.categoria,
        rol='profesional'
    ).order_by('total_salientes')

    if not candidatos:
        return

    # Equidad: Mínimo número de asignaciones
    min_asignaciones = candidatos.first().total_salientes
    finalistas = [u for u in candidatos if u.total_salientes == min_asignaciones]
    
    elegido = random.choice(finalistas)
    
    # Crear el turno de 7h
    nuevo_turno = Turno(
        profesional=elegido,
        fecha=fecha_descanso,
        tipo="7h",
        centro_especial=f"Saliente de {turno_guardia.profesional.nombre} - {turno_guardia.profesional.centro_asignado}"
    )
    nuevo_turno.save()
    
    # Incrementar conteo
    elegido.update(inc__total_salientes=1)

@app.context_processor
def inject_global_data():
    """Inyecta datos globales en todas las plantillas."""
    if 'dni' not in session:
        return dict(solicitudes_pendientes_count=0, notificaciones_pendientes_count=0, usuario=None)
    
    rol = session.get('rol')
    dni = session.get('dni')
    
    #* Registrar actividad del usuario actual
    usuarios_activos[dni] = datetime.utcnow()

    solicitudes_count = 0
    notificaciones_count = 0
    usuario = Usuario.objects(dni=dni).first()
    
    try:
        if rol == 'profesional' and usuario:
            # Solicitudes pendientes para el profesional actual
            solicitudes_count = Cambio.objects(profesional2=usuario, estado='pendiente').count()
        
        elif rol == 'direccion':
            # Cambios aceptados o rechazados que el director no ha visto
            notificaciones_count = Cambio.objects(estado__in=['aceptado', 'rechazado'], visto_por_direccion=False).count()
    except Exception:
        pass
        
    return dict(
        solicitudes_pendientes_count=solicitudes_count,
        notificaciones_pendientes_count=notificaciones_count,
        usuario=usuario
    )


@app.route("/api/usuarios_online")
def api_usuarios_online():
    """Devuelve el número de usuarios con actividad en los últimos 2 minutos."""
    if 'dni' not in session:
        return {"count": 0}, 403
    
    #* Refrescar el timestamp del usuario que hace el ping
    ahora = datetime.utcnow()
    usuarios_activos[session['dni']] = ahora

    #* Limpiar usuarios inactivos (más de 2 min) para mantener el diccionario limpio
    umbral = ahora - timedelta(minutes=2)
    
    # Creamos una lista de DNIs a eliminar para no modificar el dict mientras iteramos
    para_eliminar = [dni for dni, ts in usuarios_activos.items() if ts < umbral]
    for dni in para_eliminar:
        usuarios_activos.pop(dni, None)

    return {"count": len(usuarios_activos)}


#*---------------------------------
#* LOGIN
#*---------------------------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        dni = request.form['dni']
        password = request.form['password']

        usuario = Usuario.objects(dni=dni).first()

        if usuario and usuario.check_password(password):
            
            #* Guardar datos de la sesion
            session['username'] = usuario.nombre
            session['rol'] = usuario.rol
            session['dni'] = usuario.dni

            #* Redirección según el rol

            if usuario.rol == "administrador":
                return redirect(url_for("admin_dashboard"))
            elif usuario.rol == "direccion":
                return redirect(url_for("direccion_dashboard"))
            elif usuario.rol == "profesional":
                return redirect(url_for("profesional_dashboard"))
            
        flash ("Credenciales incorrectas")

    return render_template("login.html")

#*---------------------------------
#* LOGOUT
#*---------------------------------

@app.route("/logout")
def logout():
    #* Eliminar al usuario del registro de activos al cerrar sesión
    dni = session.get('dni')
    if dni and dni in usuarios_activos:
        del usuarios_activos[dni]
    session.clear()
    return redirect("/")

#*---------------------------------------------------
#* REGISTRO DE USUARIOS (SÓLO ADMIN Y DIRECCIÓN)
#*---------------------------------------------------

#* Importar re para validaciones (expresiones regulares)
import re

def validar_dni_nie(documento):
    documento = documento.upper()
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    
    # NIF: 8 números + 1 letra
    if re.match(r"^\d{8}[A-Z]$", documento):
        numero = int(documento[:8])
        return letras[numero % 23] == documento[8]
    
    # NIE: X/Y/Z + 7 números + 1 letra
    elif re.match(r"^[XYZ]\d{7}[A-Z]$", documento):
        mapeo = {'X': 0, 'Y': 1, 'Z': 2}
        primer_digito = mapeo[documento[0]]
        numero = int(str(primer_digito) + documento[1:8])
        return letras[numero % 23] == documento[8]
    
    return False

@app.route("/register", methods=["GET", "POST"])
@requiere_rol("administrador", "direccion")
def register():
    if request.method == "POST":
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        categoría = request.form['categoria']
        unidad_asignada = request.form['unidad_asignada']
        centro_asignado = request.form['centro_asignado']
        telefono = request.form['telefono']
        email = request.form['email']
        rol = request.form['rol']

        #* Validaciones de entrada
        if not validar_dni_nie(dni):
            flash("El DNI/NIE no tiene un formato válido.", "error")
            return redirect(url_for('register'))

        if not re.match(r"^[a-zA-Z][^\s@]*@[^\s@]+\.[^\s@]+$", email):
            flash("El email debe comenzar por una letra y tener un formato válido.", "error")
            return redirect(url_for('register'))

        if not re.match(r"^[6789]\d{8}$", telefono):
            flash("El teléfono debe tener 9 dígitos y empezar por 6, 7, 8 o 9.", "error")
            return redirect(url_for('register'))
            
        # Validación de nombre y apellidos (mínimo 6 caracteres, letras y espacios internos)
        name_regex = r"^[a-zA-ZÁéíóúñÑÁÉÍÓÚ][a-zA-ZÁéíóúñÑÁÉÍÓÚ\s]{4,}[a-zA-ZÁéíóúñÑÁÉÍÓÚ]$"
        if not re.match(name_regex, nombre) or not re.match(name_regex, apellidos):
            flash("El nombre y los apellidos deben tener al menos 6 caracteres, empezar/terminar con letra y solo contener letras/espacios.", "error")
            return redirect(url_for('register'))

        #* Lógica especial por rol que registra
        es_direccion = session.get('rol') == 'direccion'

        if es_direccion:
            if rol in ['administrador', 'direccion']:
                flash("No tienes permisos para asignar este rol.", "error")
                return redirect(url_for('register'))
            
            # Restricción de unidad para Dirección
            if unidad_asignada not in ['ZBS Albuñol', 'Dispositivo Apoyo Granada Sur']:
                flash("La unidad asignada no es válida para tu rol.", "error")
                return redirect(url_for('register'))
            
            # Forzado de centro si es Dispositivo
            if unidad_asignada == 'Dispositivo Apoyo Granada Sur':
                centro_asignado = 'Dispositivo Apoyo Granada Sur'

        #* Lógica especial para administradores registrados
        if rol == "administrador":
            categoría = "Técnico Especialista en Informática"
            unidad_asignada = "SAS"
            centro_asignado = "Distrito Sanitario Granada Sur (SAS)"
        
        if unidad_asignada == "SAS":
            centro_asignado = "Distrito Sanitario Granada Sur (SAS)"

        #* Validaciones de unicidad
        if Usuario.objects(email=email).first():
            flash("El email ya está registrado", "error")
            return redirect(url_for('register'))
        
        if Usuario.objects(dni=dni).first():
            flash("El DNI ya está registrado", "error")
            return redirect(url_for('register'))

        try:
            usuario = Usuario(
                dni=dni,
                nombre=nombre,
                apellidos=apellidos,
                categoria=categoría,
                unidad_asignada=unidad_asignada,
                centro_asignado=centro_asignado,
                telefono=int(telefono),
                email=email,
                rol=rol,
                es_saliente=request.form.get('es_saliente') == 'on'
            )
            # Asignar contraseña por defecto según el rol
            default_pass = "admin" if rol == "administrador" else "admin123"
            usuario.set_password(default_pass)
            usuario.save()
            flash("Usuario añadido correctamente", "success")
            return redirect(url_for('admin_dashboard')) if session.get('rol') == 'administrador' else redirect(url_for('direccion_dashboard'))
        except Exception as e:
            flash(f"Error al registrar usuario: {str(e)}")
            return redirect(url_for('register'))

    return render_template("admin/register.html")


#*---------------------------------------------------
#* LISTADO Y BORRADO DE USUARIOS (SÓLO ADMIN)
#*---------------------------------------------------

@app.route("/borrar_usuarios", methods=["GET"])
@requiere_rol("administrador")
def listar_usuarios():
    # Obtener todos los usuarios para mostrarlos en la tabla
    todos_usuarios = Usuario.objects()
    return render_template("admin/borrar_usuarios.html", usuarios=todos_usuarios)

@app.route("/borrar_usuario/<dni>", methods=["POST"])
@requiere_rol("administrador")
def borrar_usuario(dni):
    # Evitar que el admin se borre a sí mismo
    if dni == session.get('dni'):
        flash("No puedes borrar tu propio usuario.", "error")
        return redirect(url_for("listar_usuarios"))

    usuario_a_borrar = Usuario.objects(dni=dni).first()
    if usuario_a_borrar:
        usuario_a_borrar.delete()
        flash(f"Usuario {usuario_a_borrar.nombre} borrado exitosamente.", "error")
    else:
        flash("Usuario no encontrado.", "error")
        
    return redirect(url_for("listar_usuarios"))

@app.route("/edit_usuario/<dni>", methods=["GET", "POST"])
@requiere_rol("administrador")
def editar_usuario(dni):
    usuario = Usuario.objects(dni=dni).first()
    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("listar_usuarios"))

    if request.method == "POST":
        # Actualizar campos
        usuario.nombre = request.form['nombre']
        usuario.apellidos = request.form['apellidos']
        usuario.categoria = request.form['categoria']
        usuario.unidad_asignada = request.form['unidad_asignada']
        
        usuario.rol = request.form['rol']
        usuario.centro_asignado = request.form['centro_asignado']
        
        #* Lógica especial para administradores
        if usuario.rol == "administrador":
            usuario.categoria = "Técnico Especialista en Informática"
            usuario.unidad_asignada = "SAS"
            usuario.centro_asignado = "Distrito Sanitario Granada Sur (SAS)"

        if usuario.unidad_asignada == "SAS":
            usuario.centro_asignado = "Distrito Sanitario Granada Sur (SAS)"
        
        usuario.telefono = int(request.form['telefono'])
        usuario.email = request.form['email']
        usuario.es_saliente = request.form.get('es_saliente') == 'on'
        
        # Opcional: Actualizar contraseña si se proporciona
        new_password = request.form.get('password')
        if new_password and new_password.strip():
            usuario.set_password(new_password)
            
        usuario.save()
        flash(f"Usuario {usuario.dni} actualizado correctamente.", "success")
        return redirect(url_for("listar_usuarios"))

    return render_template("admin/edit_usuario.html", usuario=usuario)

@app.route("/cambiar_password", methods=["GET", "POST"])
def cambiar_password():
    if 'dni' not in session:
        return redirect(url_for('login'))
        
    usuario = Usuario.objects(dni=session['dni']).first()
    if not usuario:
        return redirect(url_for('logout'))

    if request.method == "POST":
        new_password = request.form.get('new_password')
        
        # Validación de seguridad de la contraseña
        pass_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]).{8,12}$"
        if not re.match(pass_regex, new_password):
            flash("La contraseña debe tener entre 8 y 12 caracteres, incluir una mayúscula, una minúscula, un número y un símbolo.", "error")
            return redirect(url_for('cambiar_password'))
            
        usuario.set_password(new_password)
        usuario.save()
        flash("Contraseña actualizada correctamente.", "success")
        
        # Redireccionar según el rol
        if usuario.rol == "administrador":
            return redirect(url_for("admin_dashboard"))
        elif usuario.rol == "direccion":
            return redirect(url_for("direccion_dashboard"))
        else:
            return redirect(url_for("profesional_dashboard"))

    return render_template("profesional/cambiar_password.html", usuario=usuario)

#*---------------------------------
#* ENDPOINTS POR ROL
#*---------------------------------

@app.route("/admin_dashboard")
@requiere_rol("administrador")
def admin_dashboard():
    return render_template("admin/admin_dashboard.html")

@app.route("/direccion_dashboard")
@requiere_rol("direccion")
def direccion_dashboard():
    return render_template("direccion/direccion_dashboard.html")

@app.route("/profesional_dashboard")
@requiere_rol("profesional")
def profesional_dashboard():
    usuario = Usuario.objects(dni=session.get('dni')).first()
    return render_template("profesional/profesional_dashboard.html", usuario=usuario)

@app.route("/profesional/ver_cuadrante")
@requiere_rol("profesional")
def profesional_ver_cuadrante():
    usuario = Usuario.objects(dni=session.get('dni')).first()
    
    # Obtener mes y año de los parámetros de consulta, por defecto el actual
    mes_actual = datetime.now().month
    anio_actual = datetime.now().year
    
    mes = request.args.get('mes', default=mes_actual, type=int)
    anio = request.args.get('anio', default=anio_actual, type=int)
    
    # Filtrar turnos por el rango de fechas del mes seleccionado
    fecha_inicio = datetime(anio, mes, 1)
    if mes == 12:
        fecha_fin = datetime(anio + 1, 1, 1)
    else:
        fecha_fin = datetime(anio, mes + 1, 1)
        
    turnos = Turno.objects(
        profesional=usuario,
        fecha__gte=fecha_inicio,
        fecha__lt=fecha_fin
    ).order_by('fecha')
    
    return render_template("profesional/ver_cuadrante.html", 
                           profesionales=[usuario], 
                           turnos=turnos, 
                           usuario=usuario,
                           mes_sel=mes,
                           anio_sel=anio)

@app.route("/profesional/descargar_pdf")
@requiere_rol("profesional")
def profesional_descargar_pdf():
    usuario = Usuario.objects(dni=session.get('dni')).first()
    
    mes = request.args.get('mes', type=int)
    anio = request.args.get('anio', type=int)
    
    if not mes or not anio:
        return {"error": "Mes y año son requeridos."}, 400

    # Rango de fechas
    fecha_inicio = datetime(anio, mes, 1)
    if mes == 12:
        fecha_fin = datetime(anio + 1, 1, 1)
    else:
        fecha_fin = datetime(anio, mes + 1, 1)
        
    turnos = Turno.objects(
        profesional=usuario,
        fecha__gte=fecha_inicio,
        fecha__lt=fecha_fin
    ).order_by('fecha')

    if not turnos:
        # Si no hay turnos, enviamos un PDF con un mensaje indicativo en lugar de error
        # para que la experiencia de usuario sea mejor que un JSON de error.
        pass

    pdf = FPDF()
    pdf.add_page()
    
    # Configurar fuentes y cabecera
    pdf.set_font("helvetica", "B", 16)
    meses_nombres = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                     "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    titulo = f"Turnos - {meses_nombres[mes-1]} {anio}"
    pdf.cell(190, 10, titulo, align="C")
    pdf.ln(15)

    # Información del profesional
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(190, 7, f"Profesional: {usuario.nombre} {usuario.apellidos}", ln=True)
    pdf.cell(190, 7, f"Categoría: {usuario.categoria}", ln=True)
    pdf.cell(190, 7, f"DNI: {usuario.dni}", ln=True)
    pdf.ln(10)

    # Tabla de turnos
    pdf.set_font("helvetica", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    
    # Anchos de columna: Fecha (40), Tipo (40), Centro (110)
    pdf.cell(40, 10, "Fecha", 1, fill=True, align="C")
    pdf.cell(40, 10, "Tipo", 1, fill=True, align="C")
    pdf.cell(110, 10, "Centro de Trabajo", 1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("helvetica", "", 10)
    if not turnos:
        pdf.cell(190, 10, "No hay turnos registrados para este mes.", 1, align="C")
    else:
        for turno in turnos:
            fecha_str = turno.fecha.strftime('%d/%m/%Y')
            pdf.cell(40, 10, fecha_str, 1, align="C")
            pdf.cell(40, 10, turno.tipo, 1, align="C")
            pdf.cell(110, 10, turno.centro_trabajo, 1, align="C")
            pdf.ln()

    # Pie de página con fecha de generación
    pdf.set_y(-15)
    pdf.set_font("helvetica", "I", 8)
    pdf.cell(0, 10, f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}", align="R")

    # Generar el PDF en memoria
    output = io.BytesIO()
    pdf_content = pdf.output()
    output.write(pdf_content)
    output.seek(0)

    nombre_archivo = f"turnos_{usuario.nombre}_{meses_nombres[mes-1]}_{anio}.pdf".replace(" ", "_")
    
    return send_file(
        output,
        as_attachment=True,
        download_name=nombre_archivo,
        mimetype="application/pdf"
    )

#*---------------------------------------------------
#* GESTIÓN DE TURNOS (SÓLO DIRECCIÓN)
#*---------------------------------------------------

@app.route("/gestion_turnos", methods=["GET", "POST"])
@requiere_rol("direccion")
def gestion_turnos():
    if request.method == "POST":
        profesionales_dnis = request.form.getlist('profesional_dni[]')
        fechas_str = request.form.getlist('fecha[]')
        tipos = request.form.getlist('tipo[]')

        exitos = 0
        errores = 0

        for dni, fecha_s, tipo in zip(profesionales_dnis, fechas_str, tipos):
            if not dni or not fecha_s or not tipo:
                continue
                
            profesional = Usuario.objects(dni=dni).first()
            if not profesional:
                errores += 1
                continue

            try:
                fecha = datetime.strptime(fecha_s, '%Y-%m-%d')
                
                # Validar descanso post-guardia (Día anterior 17h o 24h)
                dia_anterior = fecha - timedelta(days=1)
                turno_previo = Turno.objects(profesional=profesional, fecha=dia_anterior).first()
                if turno_previo and turno_previo.tipo in ["17h", "24h"]:
                    flash(f"Error: {profesional.nombre} {profesional.apellidos} realizó una guardia el {dia_anterior.strftime('%d/%m/%Y')} y debe descansar el {fecha.strftime('%d/%m/%Y')}.", "error")
                    errores += 1
                    continue

                # RESTRICCIONES POR CATEGORÍA
                categorias_consulta = ["TCAE", "Aux Administrativo/a", "Administrativo/a", "Técnico/a de Rayos", "Odontólogo/a", "Trabajador/a Social", "Fisioterapeuta", "Matrón/a"]
                if profesional.categoria in categorias_consulta:
                    if fecha.weekday() in [5, 6]:
                        flash(f"Error: {profesional.nombre} ({profesional.categoria}) solo trabaja de Lunes a Viernes.", "error")
                        errores += 1
                        continue
                    if tipo != "7h":
                        flash(f"Error: {profesional.nombre} ({profesional.categoria}) solo puede realizar turnos de 7h.", "error")
                        errores += 1
                        continue

                # RESTRICCIÓN FIN DE SEMANA GENERAL (SÓLO 24H)
                if fecha.weekday() in [5, 6] and tipo != "24h":
                    flash(f"Error: El día {fecha.strftime('%d/%m/%Y')} es fin de semana. Solo se permiten turnos de 24h.", "error")
                    errores += 1
                    continue

                # Celadores: Solo 24h
                if profesional.categoria == "Celador/a-Conductor/a" and tipo != "24h":
                    flash(f"Error: {profesional.nombre} es Celador/a y solo puede realizar turnos de 24h.", "error")
                    errores += 1
                    continue

                # NO permitir si ya existe un turno este día (REQUISITO NUEVO)
                turno_existente = Turno.objects(profesional=profesional, fecha=fecha).first()
                if turno_existente:
                    flash(f"Error: {profesional.nombre} ya tiene un turno ({turno_existente.tipo}) asignado para el {fecha.strftime('%d/%m/%Y')}. Usa el botón de modificar si quieres cambiarlo.", "error")
                    errores += 1
                    continue
                
                turno = Turno(
                    profesional=profesional,
                    fecha=fecha,
                    tipo=tipo
                )
                turno.save()
                exitos += 1
                
                # ASIGNAR SALIENTE SI ES GUARDIA (17h/24h)
                if tipo in ["17h", "24h"]:
                    asignar_saliente_automatico(turno)
            except Exception:
                errores += 1

        if exitos > 0:
            flash(f"Se han procesado {exitos} turnos correctamente.", "success")
        if errores > 0:
            flash(f"Hubo errores en {errores} turnos.", "error")

    # Obtener profesionales para el select
    profesionales = Usuario.objects(rol='profesional')
    # Obtener todos los turnos para mostrar el cuadrante
    turnos = Turno.objects().order_by('fecha')
    
    return render_template("direccion/gestion_turnos.html", profesionales=profesionales, turnos=turnos)

@app.route("/notificaciones_cambios")
@requiere_rol("direccion")
def notificaciones_cambios():
    # Obtener todos los cambios de turno registrados
    cambios = Cambio.objects().order_by('-fecha_original')
    # Al entrar aquí, marcamos todos los aceptados/rechazados como vistos por el director
    Cambio.objects(estado__in=['aceptado', 'rechazado'], visto_por_direccion=False).update(set__visto_por_direccion=True)
    return render_template("direccion/notificaciones_cambios.html", cambios=cambios)

@app.route("/descargar_pdf_dia")
@requiere_rol("direccion", "profesional")
def descargar_pdf_dia():
    fecha_str = request.args.get('fecha')
    if fecha_str:
        try:
            hoy = datetime.strptime(fecha_str, '%Y-%m-%d')
        except ValueError:
            return {"error": "Formato de fecha inválido."}, 400
    else:
        hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    turnos_hoy = Turno.objects(fecha=hoy)

    if not turnos_hoy:
        return {"error": f"No hay turnos registrados para el {hoy.strftime('%d/%m/%Y')}."}, 404

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(190, 10, f"Trabajadores con turno el día: {hoy.strftime('%d/%m/%Y')}", align="C")
    pdf.ln(10)

    pdf.set_font("helvetica", "B", 9)
    pdf.set_fill_color(220, 220, 220)
    # 190 width total
    pdf.cell(40, 10, "Nombre y Apellidos", 1, fill=True, align="C")
    pdf.cell(40, 10, "Categoría", 1, fill=True, align="C")
    pdf.cell(25, 10, "Teléfono", 1, fill=True, align="C")
    pdf.cell(15, 10, "Turno", 1, fill=True, align="C")
    pdf.cell(70, 10, "Centro", 1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("helvetica", "", 8)
    for turno in turnos_hoy:
        nombre_completo = f"{turno.profesional.nombre} {turno.profesional.apellidos}"
        pdf.cell(40, 10, nombre_completo, 1, align="C")
        pdf.cell(40, 10, turno.profesional.categoria, 1, align="C")
        pdf.cell(25, 10, str(turno.profesional.telefono), 1, align="C")
        pdf.cell(15, 10, turno.tipo, 1, align="C")
        
        centro = turno.centro_trabajo
            
        pdf.cell(70, 10, centro, 1, align="C")
        pdf.ln()

    # Generar el PDF en memoria
    output = io.BytesIO()
    pdf_content = pdf.output()
    output.write(pdf_content)
    output.seek(0)

    # Elimino el flash success del backend dado que Fetch gestiona sus propias notificaciones para evitar dobles mensajes si recarga.
    return send_file(
        output,
        as_attachment=True,
        download_name=f"turnos_{hoy.strftime('%Y%m%d')}.pdf",
        mimetype="application/pdf"
    )

#*---------------------------------
#* GESTIÓN DE CORTESÍA / CAMBIOS PROFESIONAL
#*---------------------------------

@app.route("/api/validar_cambio")
@requiere_rol("profesional")
def api_validar_cambio():
    mi_turno_id = request.args.get('mi_turno_id')
    companero_turno_id = request.args.get('companero_turno_id')

    if not mi_turno_id or not companero_turno_id:
        return {"valido": False, "error": "Faltan datos para validar."}

    mi_turno = Turno.objects(id=mi_turno_id).first()
    companero_turno = Turno.objects(id=companero_turno_id).first()

    if not mi_turno or not companero_turno:
        return {"valido": False, "error": "Turnos no encontrados."}

    # Validar P1 (quien pide el cambio)
    es_valido, msg = validar_descanso_reutilizable(mi_turno.profesional, companero_turno.fecha, mi_turno.fecha)
    if not es_valido:
        return {"valido": False, "mensaje": f"No puedes recibir este turno: {msg}"}

    # Validar P2 (el compañero)
    es_valido_p2, msg_p2 = validar_descanso_reutilizable(companero_turno.profesional, mi_turno.fecha, companero_turno.fecha)
    if not es_valido_p2:
        return {"valido": False, "mensaje": f"Tu compañero {msg_p2}"}

    return {"valido": True}


@app.route("/profesional/pedir_cambio", methods=["GET", "POST"])
@requiere_rol("profesional")
def pedir_cambio_turno():
    usuario = Usuario.objects(dni=session.get('dni')).first()
    categorias_permitidas = ["Médico/a", "DUE", "Celador/a-Conductor/a"]
    
    if usuario.categoria not in categorias_permitidas:
        return redirect(url_for("profesional_dashboard"))

    # Turnos propios que sean 17h o 24h
    mis_turnos = Turno.objects(profesional=usuario, tipo__in=["17h", "24h"], fecha__gte=datetime.now()).order_by('fecha')
    
    # Compañeros de la MISMA categoría (excluyendose a si mismo)
    companeros = Usuario.objects(categoria=usuario.categoria, dni__ne=usuario.dni)

    if request.method == "POST":
        mi_turno_id = request.form.get("mi_turno_id")
        companero_dni = request.form.get("companero_dni")
        companero_turno_id = request.form.get("companero_turno_id")

        if not mi_turno_id or not companero_dni or not companero_turno_id:
            flash("Faltan datos para realizar la solicitud.", "error")
            return redirect(url_for("pedir_cambio_turno"))

        mi_turno = Turno.objects(id=mi_turno_id, profesional=usuario).first()
        companero = Usuario.objects(dni=companero_dni).first()
        companero_turno = Turno.objects(id=companero_turno_id, profesional=companero).first()

        if not mi_turno or not companero or not companero_turno:
            flash("Error en los datos proporcionados.", "error")
            return redirect(url_for("pedir_cambio_turno"))

        # Validations
        if companero.categoria != usuario.categoria:
            flash("Solo puedes cambiar turnos con compañeros de tu misma categoría.", "error")
            return redirect(url_for("pedir_cambio_turno"))

        if mi_turno.tipo not in ["17h", "24h"] or companero_turno.tipo not in ["17h", "24h"]:
            flash("Solo se pueden cambiar turnos de 17h o 24h.", "error")
            return redirect(url_for("pedir_cambio_turno"))

        # Validar descanso para P1 (el que pide el cambio)
        # P1 va a recibir el turno de P2 (fecha_final)
        dia_antes_f2 = companero_turno.fecha - timedelta(days=1)
        dia_despues_f2 = companero_turno.fecha + timedelta(days=1)

        # Buscamos otros turnos de P1 en esos días (ignorando el que va a soltar)
        p1_conflictos = Turno.objects(
            profesional=usuario, 
            fecha__in=[dia_antes_f2, dia_despues_f2, companero_turno.fecha],
            tipo__in=["17h", "24h"]
        ).filter(fecha__ne=mi_turno.fecha)

        if p1_conflictos.first():
            flash(f"No puedes solicitar este cambio porque no cumplirías el descanso obligatorio con tus otros turnos.", "error")
            return redirect(url_for("pedir_cambio_turno"))

        # Create Request
        cambio = Cambio(
            profesional1=usuario,
            profesional2=companero,
            fecha_original=mi_turno.fecha,
            fecha_final=companero_turno.fecha,
            tipo_p1=mi_turno.tipo,
            tipo_p2=companero_turno.tipo,
            estado='pendiente'
        )
        cambio.save()
        flash("Solicitud de cambio enviada correctamente.", "success")
        return redirect(url_for("profesional_dashboard"))

    return render_template("profesional/pedir_cambio.html", usuario=usuario, mis_turnos=mis_turnos, companeros=companeros)

@app.route("/api/turnos_companero/<dni>")
@requiere_rol("profesional")
def api_turnos_companero(dni):
    companero = Usuario.objects(dni=dni).first()
    if not companero:
        return {"turnos": []}
    
    turnos = Turno.objects(profesional=companero, tipo__in=["17h", "24h"], fecha__gte=datetime.now()).order_by('fecha')
    return {"turnos": [{"id": str(t.id), "fecha": t.fecha.strftime('%d/%m/%Y'), "tipo": t.tipo} for t in turnos]}


@app.route("/profesional/solicitudes_cambio")
@requiere_rol("profesional")
def solicitudes_cambio():
    usuario = Usuario.objects(dni=session.get('dni')).first()
    categorias_permitidas = ["Médico/a", "DUE", "Celador/a-Conductor/a"]
    
    if usuario.categoria not in categorias_permitidas:
        return redirect(url_for("profesional_dashboard"))

    solicitudes = Cambio.objects(profesional2=usuario, estado='pendiente').order_by('fecha_original')
    return render_template("profesional/solicitudes_cambio.html", usuario=usuario, solicitudes=solicitudes)


@app.route("/profesional/responder_cambio/<cambio_id>/<accion>", methods=["POST"])
@requiere_rol("profesional")
def responder_cambio(cambio_id, accion):
    usuario = Usuario.objects(dni=session.get('dni')).first()
    cambio = Cambio.objects(id=cambio_id, profesional2=usuario, estado='pendiente').first()

    if not cambio:
        flash("Solicitud no válida o ya gestionada.", "error")
        return redirect(url_for("solicitudes_cambio"))

    if accion == "rechazar":
        cambio.estado = 'rechazado'
        cambio.visto_por_direccion = False
        cambio.save()
        flash("Has rechazado el cambio de turno.", "success")
        return redirect(url_for("solicitudes_cambio"))

    elif accion == "aceptar":
        # Extraer turnos actuales
        turno_p1 = Turno.objects(profesional=cambio.profesional1, fecha=cambio.fecha_original).first()
        turno_p2 = Turno.objects(profesional=cambio.profesional2, fecha=cambio.fecha_final).first()
        
        if not turno_p1 or not turno_p2:
            flash("Uno de los turnos ya no existe o fue modificado.", "error")
            return redirect(url_for("solicitudes_cambio"))

        # Validar tiempo de descanso (1 día) para ambos.
        
        # P1 va a recibir fecha_final (su turno original es fecha_original)
        es_valido_p1, msg_p1 = validar_descanso_reutilizable(cambio.profesional1, cambio.fecha_final, cambio.fecha_original)
        if not es_valido_p1:
            flash(f"Error: {cambio.profesional1.nombre} {msg_p1}", "error")
            return redirect(url_for("solicitudes_cambio"))

        # P2 va a recibir fecha_original (su turno original es fecha_final)
        es_valido_p2, msg_p2 = validar_descanso_reutilizable(cambio.profesional2, cambio.fecha_original, cambio.fecha_final)
        if not es_valido_p2:
            flash(f"Error: {msg_p2}", "error")
            return redirect(url_for("solicitudes_cambio"))

        # All good, do swap
        turno_p1.profesional = cambio.profesional2
        turno_p2.profesional = cambio.profesional1

        # Limpiar salientes previos de ambos días por si acaso
        eliminar_saliente_previo(cambio.profesional1, cambio.fecha_original + timedelta(days=1))
        eliminar_saliente_previo(cambio.profesional2, cambio.fecha_final + timedelta(days=1))

        turno_p1.save()
        turno_p2.save()

        # Reasignar salientes según los nuevos turnos
        if turno_p1.tipo in ["17h", "24h"]:
            asignar_saliente_automatico(turno_p1)
        if turno_p2.tipo in ["17h", "24h"]:
            asignar_saliente_automatico(turno_p2)

        cambio.estado = 'aceptado'
        cambio.visto_por_direccion = False
        cambio.save()

        flash("Cambio de turno aceptado con éxito.", "success")
        return redirect(url_for("solicitudes_cambio"))

    return redirect(url_for("solicitudes_cambio"))

@app.route("/profesional/historico_cambios")
@requiere_rol("profesional")
def historico_cambios():
    usuario = Usuario.objects(dni=session.get('dni')).first()
    categorias_permitidas = ["Médico/a", "DUE", "Celador/a-Conductor/a"]
    
    if usuario.categoria not in categorias_permitidas:
        return redirect(url_for("profesional_dashboard"))

    # Buscar cambios donde el usuario sea p1 o p2 y esté aceptado
    # MongoEngine Q objects allow for complex queries, but we can just use filtering
    # Since Q objects aren't imported, let's just do it manual or import Q
    # We can fetch both and merge
    cambios_p1 = list(Cambio.objects(profesional1=usuario, estado='aceptado'))
    cambios_p2 = list(Cambio.objects(profesional2=usuario, estado='aceptado'))
    
    # Merge and format unique
    todos_cambios = {str(c.id): c for c in (cambios_p1 + cambios_p2)}
    # Sort backwards by original date
    cambios = sorted(todos_cambios.values(), key=lambda x: x.fecha_original, reverse=True)

    return render_template("profesional/historico_cambios.html", usuario=usuario, cambios=cambios)

#*---------------------------------
#* GESTIÓN DE TURNOS (BORRAR / MODIFICAR)
#*---------------------------------

@app.route('/borrar_turno/<turno_id>', methods=['POST'])
@requiere_rol("direccion")
def borrar_turno(turno_id):
    try:
        turno = Turno.objects(id=turno_id).first()
        if turno:
            # Si era una guardia, limpiar su saliente
            if turno.tipo in ["17h", "24h"]:
                eliminar_saliente_previo(turno.profesional, turno.fecha + timedelta(days=1))
            turno.delete()
        flash("Turno eliminado correctamente.", "success")
    except Exception as e:
        flash(f"Error al eliminar turno: {str(e)}", "error")
    return redirect(url_for('gestion_turnos'))

@app.route('/modificar_turno/<turno_id>', methods=['POST'])
@requiere_rol("direccion")
def modificar_turno(turno_id):
    try:
        nuevo_tipo = request.form.get('tipo')
        turno_actual = Turno.objects(id=turno_id).first()
        
        if turno_actual:
            # RESTRICCIONES POR CATEGORÍA
            profesional = turno_actual.profesional
            
            # Categorías de Consulta: Solo 7h y L-V
            categorias_consulta = ["TCAE", "Aux Administrativo/a", "Administrativo/a", "Técnico/a de Rayos", "Odontólogo/a", "Trabajador/a Social", "Fisioterapeuta", "Matrón/a"]
            if profesional.categoria in categorias_consulta:
                if turno_actual.fecha.weekday() in [5, 6]:
                    flash(f"Error: {profesional.nombre} ({profesional.categoria}) solo trabaja de Lunes a Viernes.", "error")
                    return redirect(url_for('gestion_turnos'))
                if nuevo_tipo != "7h":
                    flash(f"Error: {profesional.nombre} ({profesional.categoria}) solo puede realizar turnos de 7h.", "error")
                    return redirect(url_for('gestion_turnos'))

            # Validar fin de semana en modificación GENERAL (SÓLO 24H)
            if turno_actual.fecha.weekday() in [5, 6] and nuevo_tipo != "24h":
                flash(f"Error: El día {turno_actual.fecha.strftime('%d/%m/%Y')} es fin de semana. Solo se permiten turnos de 24h.", "error")
                return redirect(url_for('gestion_turnos'))

            # Celadores: Solo 24h
            if profesional.categoria == "Celador/a-Conductor/a" and nuevo_tipo != "24h":
                flash(f"Error: {profesional.nombre} es Celador/a y solo puede realizar turnos de 24h.", "error")
                return redirect(url_for('gestion_turnos'))

        # Limpiar saliente previo por si el tipo cambia de guardia a normal
        eliminar_saliente_previo(turno_actual.profesional, turno_actual.fecha + timedelta(days=1))
        
        Turno.objects(id=turno_id).update_one(set__tipo=nuevo_tipo)
        
        # Si el nuevo tipo es guardia, asignar nuevo saliente
        if nuevo_tipo in ["17h", "24h"]:
            # Recargar el objeto para tener el tipo actualizado
            turno_actual.reload()
            asignar_saliente_automatico(turno_actual)
            
        flash("Turno modificado correctamente.", "success")
    except Exception as e:
        flash(f"Error al modificar turno: {str(e)}", "error")
    return redirect(url_for('gestion_turnos'))

#*----------------------------------------------------------------------
#* MAIN (SOLO SE EJECUTARÁ CUANDO SE EJECUTE EL ARCHIVO DIRECTAMENTE)
#*----------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
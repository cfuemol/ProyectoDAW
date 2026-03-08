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
            elif usuario.rol == "mostrador":
                return redirect(url_for("mostrador_dashboard"))
            
        flash ("Credenciales incorrectas")

    return render_template("login.html")

#*---------------------------------
#* LOGOUT
#*---------------------------------

@app.route("/logout")
def logout():
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
    
    # NIE: X, Y o Z + 7 números + 1 letra
    if re.match(r"^[XYZ]\d{7}[A-Z]$", documento):
        prefijo = {"X": "0", "Y": "1", "Z": "2"}
        documento_transformado = prefijo[documento[0]] + documento[1:]
        numero = int(documento_transformado[:8])
        return letras[numero % 23] == documento[-1]
    
    return False

@app.route("/register", methods=["GET", "POST"])
@requiere_rol("administrador", "direccion")
def register():
    if request.method == "POST":
        dni = request.form['dni'].strip().upper()
        nombre = request.form['nombre'].strip()
        apellidos = request.form['apellidos'].strip()
        categoría = request.form['categoria']
        centro_asignado = request.form['centro_asignado']
        telefono = request.form['telefono'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        rol = request.form['rol']
        unidad_asignada = request.form['unidad_asignada']

        #* Validaciones de formato
        if not validar_dni_nie(dni):
            flash("El DNI/NIE no tiene un formato válido.", "error")
            return redirect(url_for('register'))

        if not re.match(r"^[a-zA-Z][^\s@]*@[^\s@]+\.[^\s@]+$", email):
            flash("El email debe comenzar por una letra y tener un formato válido.", "error")
            return redirect(url_for('register'))

        if not re.match(r"^[6789]\d{8}$", telefono):
            flash("El teléfono debe tener 9 dígitos y empezar por 6, 7, 8 o 9.", "error")
            return redirect(url_for('register'))
            
        # Validación de contraseña
        pass_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]).{8,12}$"
        if not re.match(pass_regex, password):
            flash("La contraseña debe tener entre 8 y 12 caracteres, incluir una mayúscula, una minúscula, un número y un símbolo.", "error")
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
                rol=rol
            )
            usuario.set_password(password)
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
        
        # Opcional: Actualizar contraseña si se proporciona
        new_password = request.form.get('password')
        if new_password and new_password.strip():
            usuario.set_password(new_password)
            
        usuario.save()
        flash(f"Usuario {usuario.dni} actualizado correctamente.", "success")
        return redirect(url_for("listar_usuarios"))

    return render_template("admin/edit_usuario.html", usuario=usuario)

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
    return render_template("profesional/profesional_dashboard.html")

@app.route("/mostrador_dashboard")
@requiere_rol("mostrador")
def mostrador_dashboard():
    return render_template("mostrador/mostrador_dashboard.html")

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
            except Exception:
                errores += 1

        if exitos > 0:
            flash(f"Se han procesado {exitos} turnos correctamente.", "success")
        if errores > 0:
            flash(f"Hubo errores en {errores} turnos.", "error")

    # Obtener profesionales para el select
    profesionales = Usuario.objects(rol__in=['profesional', 'mostrador'])
    # Obtener todos los turnos para mostrar el cuadrante
    turnos = Turno.objects().order_by('fecha')
    
    return render_template("direccion/gestion_turnos.html", profesionales=profesionales, turnos=turnos)

@app.route("/notificaciones_cambios")
@requiere_rol("direccion")
def notificaciones_cambios():
    # Obtener todos los cambios de turno registrados
    cambios = Cambio.objects().order_by('-fecha_original')
    return render_template("direccion/notificaciones_cambios.html", cambios=cambios)

@app.route("/descargar_pdf_dia")
@requiere_rol("direccion")
def descargar_pdf_dia():
    hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    turnos_hoy = Turno.objects(fecha=hoy)

    if not turnos_hoy:
        flash("No hay turnos registrados para hoy.", "info")
        return redirect(url_for('direccion_dashboard'))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(190, 10, f"Trabajadores con turno hoy: {hoy.strftime('%d/%m/%Y')}", align="C")
    pdf.ln(10)

    pdf.set_font("helvetica", "B", 9)
    pdf.cell(35, 10, "Nombre", 1)
    pdf.cell(35, 10, "Apellidos", 1)
    pdf.cell(35, 10, "Categoría", 1)
    pdf.cell(25, 10, "Teléfono", 1)
    pdf.cell(20, 10, "Turno", 1)
    pdf.cell(35, 10, "Centro", 1)
    pdf.ln()

    pdf.set_font("helvetica", "", 8)
    for turno in turnos_hoy:
        pdf.cell(35, 10, turno.profesional.nombre, 1)
        pdf.cell(35, 10, turno.profesional.apellidos, 1)
        pdf.cell(35, 10, turno.profesional.categoria, 1)
        pdf.cell(25, 10, str(turno.profesional.telefono), 1)
        pdf.cell(20, 10, turno.tipo, 1)
        
        # Lógica de ubicación 24h L-V
        if turno.tipo == "24h" and turno.fecha.weekday() < 5:
            centro = f"{turno.profesional.centro_asignado} + Urgencias"
        elif turno.tipo in ["17h", "24h"]:
            centro = "Urgencias Albuñol"
        else:
            centro = turno.profesional.centro_asignado
            
        pdf.cell(35, 10, centro, 1)
        pdf.ln()

    # Generar el PDF en memoria
    output = io.BytesIO()
    pdf_content = pdf.output()
    output.write(pdf_content)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name=f"turnos_{hoy.strftime('%Y%m%d')}.pdf",
        mimetype="application/pdf"
    )

#*---------------------------------
#* GESTIÓN DE TURNOS (BORRAR / MODIFICAR)
#*---------------------------------

@app.route('/borrar_turno/<turno_id>', methods=['POST'])
@requiere_rol("direccion")
def borrar_turno(turno_id):
    try:
        Turno.objects(id=turno_id).delete()
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

        Turno.objects(id=turno_id).update_one(set__tipo=nuevo_tipo)
        flash("Turno modificado correctamente.", "success")
    except Exception as e:
        flash(f"Error al modificar turno: {str(e)}", "error")
    return redirect(url_for('gestion_turnos'))

#*----------------------------------------------------------------------
#* MAIN (SOLO SE EJECUTARÁ CUANDO SE EJECUTE EL ARCHIVO DIRECTAMENTE)
#*----------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
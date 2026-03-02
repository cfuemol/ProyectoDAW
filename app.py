from flask import Flask, render_template, request, redirect, session, url_for, flash
import os
from models.database import init_db
from models.usuario import Usuario

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
        print(f"DEBUG: Entrando en POST register para {request.form.get('dni')}")
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

        print(f"DEBUG: Datos recibidos - Nombre: {nombre}, Pass: {password}")

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

        #* Lógica especial para administradores
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


#*----------------------------------------------------------------------
#* MAIN (SOLO SE EJECUTARÁ CUANDO SE EJECUTE EL ARCHIVO DIRECTAMENTE)
#*----------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
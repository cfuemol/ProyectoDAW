from flask import Flask, render_template, request, redirect, session, url_for, flash
from models.database import init_db
from models.usuario import Usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

#* Inicializar MongoDB
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

@app.route("/register", methods=["GET", "POST"])
@requiere_rol("administrador", "direccion")
def register():
    if request.method == "POST":
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        categoría = request.form['categoria']
        centro_asignado = request.form['centro_asignado']
        telefono = request.form['telefono']
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']

        #* Validaciones
        if Usuario.objects(email=email).first():
            return "El email ya está registrado"
        
        if Usuario.objects(dni=dni).first():
            return "El dni ya está registrado"

        usuario = Usuario(
            dni=dni,
            nombre=nombre,
            apellidos=apellidos,
            categoria=categoría,
            centro_asignado=centro_asignado,
            telefono=int(telefono),
            email=email,
            rol=rol
        )
        usuario.set_password(password)
        usuario.save()

        flash("Usuario registrado exitosamente")

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
        flash("No puedes borrar tu propio usuario.")
        return redirect(url_for("listar_usuarios"))

    usuario_a_borrar = Usuario.objects(dni=dni).first()
    if usuario_a_borrar:
        usuario_a_borrar.delete()
        flash(f"Usuario {usuario_a_borrar.nombre} borrado exitosamente.")
    else:
        flash("Usuario no encontrado.")
        
    return redirect(url_for("listar_usuarios"))

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
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# Importamos TU configuración y TUS modelos
from config import Config
from app.models import db, Usuario 

app = Flask(__name__)
app.config.from_object(Config)

# Inicializamos la DB con la app
db.init_app(app)

# Configuración de Login Manager (Para manejar sesiones fácilmente)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Crear tablas si no existen (Solo la primera vez)
with app.app_context():
    db.create_all()

@app.route('/')
def inicio():
    return redirect(url_for('login'))

# ================================
# LOGIN (Versión SQLAlchemy)
# ================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        passwd = request.form['password']

        # BUSCAR USUARIO CON SQLALCHEMY (Mucho más limpio)
        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and check_password_hash(usuario.password_hash, passwd):
            login_user(usuario) # Esto inicia la sesión automáticamente
            return redirect(url_for('usuario_bienvenida'))
        
        flash("Correo o contraseña incorrectos") # Usa flash para mensajes de error
        return render_template('login.html')

    return render_template('login.html')

# ================================
# REGISTRO (Versión SQLAlchemy)
# ================================
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Recibir datos
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        dni = request.form['dni']
        ruc = request.form['ruc']
        negocio_nombre = request.form['negocio_nombre']
        telefono = request.form['telefono']
        correo = request.form['correo']
        password = request.form['password']

        # Verificar si existe
        if Usuario.query.filter_by(correo=correo).first():
            return "El correo ya está registrado"

        # Crear el objeto Usuario (Usando tu modelo)
        nuevo_usuario = Usuario(
            nombres=nombres,
            apellidos=apellidos,
            dni=dni,
            ruc=ruc,
            negocio_nombre=negocio_nombre,
            telefono=telefono,
            correo=correo,
            password_hash=generate_password_hash(password)
        )

        try:
            # Guardar en base de datos
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return f"Error al registrar: {str(e)}"

    return render_template('registro.html')

@app.route('/usuario')
@login_required # Protege la ruta para que solo entren logueados
def usuario_bienvenida():
    # Podemos pasar el objeto 'current_user' al HTML
    return render_template('user.html', usuario=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

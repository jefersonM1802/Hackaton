from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import desc
from config import Config
from app.models import *

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar DB
db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# ================================
# CREAR TABLAS
# ================================
with app.app_context():
    db.create_all()


# ================================
# RUTA INICIO
# ================================
@app.route('/')
def inicio():
    return redirect(url_for('login'))


# ================================
# LOGIN
# ================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        passwd = request.form['password']

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and check_password_hash(usuario.password_hash, passwd):
            login_user(usuario)
            return redirect(url_for('dashboard_home'))

        flash("Correo o contraseña incorrectos")
        return render_template('login.html')

    return render_template('login.html')


# ================================
# REGISTRO
# ================================
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':

        correo = request.form['correo']

        if Usuario.query.filter_by(correo=correo).first():
            return "El correo ya está registrado"

        nuevo = Usuario(
            nombres=request.form['nombres'],
            apellidos=request.form['apellidos'],
            dni=request.form['dni'],
            ruc=request.form['ruc'],
            negocio_nombre=request.form['negocio_nombre'],
            telefono=request.form['telefono'],
            correo=correo,
            password_hash=generate_password_hash(request.form['password'])
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('registro.html')


# ================================
# DASHBOARD HOME
# ================================


# ================================
# DASHBOARD HOME (CONECTADO A BD)
# ================================
@app.route('/dashboard')
@login_required
def dashboard_home():
    # 1. Obtener los últimos INDICADORES (Ingresos, Gastos, etc.)
    # Buscamos el registro más reciente de este usuario
    kpi = IndicadorFinanciero.query.filter_by(id_usuario=current_user.id_usuario)\
        .order_by(desc(IndicadorFinanciero.anio), desc(IndicadorFinanciero.mes))\
        .first()

    # 2. Obtener el último RIESGO calculado
    riesgo = Riesgo.query.filter_by(id_usuario=current_user.id_usuario)\
        .order_by(desc(Riesgo.fecha_registro))\
        .first()

    # 3. Obtener los últimos 4 DOCUMENTOS subidos
    docs_recientes = Documento.query.filter_by(id_usuario=current_user.id_usuario)\
        .order_by(desc(Documento.fecha_subida))\
        .limit(4)\
        .all()

    # Si no hay KPIs todavía (usuario nuevo), creamos un objeto vacío para que no de error
    if not kpi:
        class DummyKPI:
            ingresos = 0
            gastos = 0
            utilidad = 0
            flujo = 0
        kpi = DummyKPI()

    # Renderizar pasando todos los datos
    return render_template('dashboard/home.html', 
                           usuario=current_user,
                           stats=kpi,
                           riesgo=riesgo,
                           docs=docs_recientes)

@login_required
def dashboard_home():
    return render_template('dashboard/home.html', usuario=current_user)


# ================================
# DEMÁS MÓDULOS
# ================================
@app.route('/documentos')
@login_required
def documentos_view():
    return render_template('dashboard/upload.html', usuario=current_user)


@app.route('/ia/analisis')
@login_required
def ia_analisis_view():
    return render_template('modules/analysis.html', usuario=current_user)


@app.route('/validacion')
@login_required
def validacion_view():
    return render_template('modules/validate.html', usuario=current_user)


@app.route('/indicadores')
@login_required
def indicadores_view():
    return render_template('modules/kpis.html', usuario=current_user)


@app.route('/riesgos')
@login_required
def riesgos_view():
    return render_template('modules/risk.html', usuario=current_user)


@app.route('/proyecciones')
@login_required
def proyecciones_view():
    return render_template('modules/projection.html', usuario=current_user)


@app.route('/reportes')
@login_required
def reportes_view():
    return render_template('modules/reports.html', usuario=current_user)


@app.route('/blockchain')
@login_required
def blockchain_view():
    return render_template('modules/chain.html', usuario=current_user)


@app.route('/perfil')
@login_required
def perfil_view():
    return render_template('profile/profile.html', usuario=current_user)


@app.route('/configuracion')
@login_required
def configuracion_view():
    return render_template('profile/settings.html', usuario=current_user)


# ================================
# LOGOUT
# ================================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ================================
# RUN
# ================================
if __name__ == '__main__':
    app.run(debug=True)

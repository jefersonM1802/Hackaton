from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db   # conexión MySQL

app = Flask(__name__)


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

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        datos = cursor.fetchone()
        conn.close()

        if datos and check_password_hash(datos["password_hash"], passwd):
            return redirect(url_for('usuario_bienvenida'))

        return "Correo o contraseña incorrectos"

    return render_template('login.html')


# ================================
# REGISTRO
# ================================
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombres         = request.form['nombres']
        apellidos       = request.form['apellidos']
        dni             = request.form['dni']
        ruc             = request.form['ruc']
        negocio_nombre  = request.form['negocio_nombre']
        telefono        = request.form['telefono']
        correo          = request.form['correo']
        password        = request.form['password']

        hash_pw = generate_password_hash(password)

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO usuarios 
                (nombres, apellidos, dni, ruc, negocio_nombre, telefono, correo, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombres, apellidos, dni, ruc, negocio_nombre, telefono, correo, hash_pw))

            conn.commit()
            conn.close()
            return "Registro exitoso"

        except Exception as e:
            conn.close()
            return "Error: " + str(e)

    return render_template('registro.html')


@app.route('/usuario')
def usuario_bienvenida():
    return render_template('user.html')


if __name__ == '__main__':
    app.run(debug=True)

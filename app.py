from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from applications.chatbot import chatbot_bp  # Blueprint existente

# --- Configuración de la app ---
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'tu_clave_secreta_cámbiala')

# --- Configuración de MySQL ---
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'      # o 'appuser'
app.config['MYSQL_PASSWORD'] = ''          # contraseña vacía o la que hayas definido
app.config['MYSQL_DB']       = 'stai_system'
mysql = MySQL(app)

# Registro del Blueprint para el chatbot
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

# Decorador para permisos por rol
def login_requerido(rol_esperado=None):
    def decorador(funcion):
        def wrapper(*args, **kwargs):
            if 'usuario' not in session:
                return redirect(url_for('login'))
            if rol_esperado and session.get('rol') != rol_esperado:
                return render_template('error_acceso.html', mensaje='Acceso denegado.')
            return funcion(*args, **kwargs)
        wrapper.__name__ = funcion.__name__
        return wrapper
    return decorador

# --- Rutas principales ---
@app.route('/')
def index():
    if 'usuario' in session:
        if session.get('rol') == 'Plataforma':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('usuario_perfil'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # Campos del formulario
        username = request.form['username']
        email    = request.form['email']
        password = request.form['password']
        work_area= request.form['work_area']
        department = request.form['department']
        branch     = request.form['branch']
        entidad_financiera = request.form['entidad_financiera']
        # Inserción en BD
        cur = mysql.connection.cursor()
        cur.execute(
          """INSERT INTO users
             (username,email,password,work_area,department,branch,entidad_financiera)
             VALUES (%s,%s,%s,%s,%s,%s,%s)""",
          (username,email,password,work_area,department,branch,entidad_financiera)
        )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        email    = request.form['username']  # usa 'email' si renombras el input
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(
          "SELECT id, username, password, work_area AS rol"
          " FROM users WHERE email=%s", (email,)
        )
        user = cur.fetchone()
        cur.close()
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['usuario'] = user['username']
            session['rol']     = user['rol']
            if session['rol'] == 'Plataforma':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('usuario_perfil'))
        else:
            error = 'Credenciales incorrectas.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Rutas Admin ---
@app.route('/admin/dashboard')
@login_requerido(rol_esperado='Plataforma')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/admin/mapas')
@login_requerido(rol_esperado='Plataforma')
def admin_mapas():
    return render_template('admin/mapas.html')

@app.route('/admin/programar')
@login_requerido(rol_esperado='Plataforma')
def admin_programar():
    return render_template('admin/programar.html')

# --- Rutas Usuario ---
@app.route('/usuario/perfil')
@login_requerido(rol_esperado='usuario')
def usuario_perfil():
    return render_template('usuario/perfil.html')

@app.route('/usuario/chatbot')
@login_requerido(rol_esperado='usuario')
def usuario_chatbot():
    return render_template('usuario/chatbot.html')

@app.route('/usuario/test')
@login_requerido(rol_esperado='usuario')
def usuario_test():
    return render_template('usuario/test.html')

@app.route('/usuario/calendario')
@login_requerido(rol_esperado='usuario')
def usuario_calendario():
    return render_template('usuario/calendario.html')

@app.route('/error_acceso')
def error_acceso():
    return render_template('error_acceso.html', mensaje='No tienes permiso para acceder a esta página.')

if __name__ == '__main__':
    app.run(debug=True)
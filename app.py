from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # ¡Cambia esto por algo seguro!

# Simulación de usuarios y roles (para propósitos de plantilla)
USUARIOS = {
    'admin': {'contrasena': 'admin', 'rol': 'admin'},
    'user1': {'contrasena': 'user1', 'rol': 'usuario'},
    'user2': {'contrasena': 'user2', 'rol': 'usuario'}
}

def login_requerido(rol_esperado=None):
    def decorador(funcion):
        def wrapper(*args, **kwargs):
            if 'usuario' not in session:
                return redirect(url_for('login'))
            if rol_esperado and USUARIOS.get(session['usuario'], {}).get('rol') != rol_esperado:
                return render_template('error_acceso.html', mensaje='Acceso denegado.')
            return funcion(*args, **kwargs)
        wrapper.__name__ = funcion.__name__
        return wrapper
    return decorador

@app.route('/')
def index():
    if 'usuario' in session:
        if USUARIOS[session['usuario']]['rol'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('usuario_perfil'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = request.form['username']
        contrasena = request.form['password']
        if usuario in USUARIOS and USUARIOS[usuario]['contrasena'] == contrasena:
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            error = 'Usuario o contraseña incorrectos.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

# Rutas para administradores
@app.route('/admin/dashboard')
@login_requerido(rol_esperado='admin')
def admin_dashboard():
    return render_template('admin/dashboard.html', USUARIOS=USUARIOS)

@app.route('/admin/mapas')
@login_requerido(rol_esperado='admin')
def admin_mapas():
    return render_template('admin/mapas.html', USUARIOS=USUARIOS)

@app.route('/admin/programar')
@login_requerido(rol_esperado='admin')
def admin_programar():
    return render_template('admin/programar.html', USUARIOS=USUARIOS)

# Rutas para usuarios
@app.route('/usuario/perfil')
@login_requerido(rol_esperado='usuario')
def usuario_perfil():
    return render_template('usuario/perfil.html', USUARIOS=USUARIOS)

@app.route('/usuario/chatbot')
@login_requerido(rol_esperado='usuario')
def usuario_chatbot():
    return render_template('usuario/chatbot.html', USUARIOS=USUARIOS)

@app.route('/usuario/test')
@login_requerido(rol_esperado='usuario')
def usuario_test():
    return render_template('usuario/test.html', USUARIOS=USUARIOS)

@app.route('/usuario/calendario')
@login_requerido(rol_esperado='usuario')
def usuario_calendario():
    return render_template('usuario/calendario.html', USUARIOS=USUARIOS)

@app.route('/error_acceso')
def error_acceso():
    return render_template('error_acceso.html', mensaje='No tienes permiso para acceder a esta página.')

if __name__ == '__main__':
    app.run(debug=True)
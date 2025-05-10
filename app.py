from flask import Flask, render_template, request, redirect, url_for, session
from applications.chatbot import chatbot_bp  # Importamos el chatbot correctamente

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # ¡Cambia esto por algo seguro!

# Registro del Blueprint para el chatbot
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

# Simulación de usuarios y roles
USUARIOS = {
    'admin': {'contrasena': 'admin', 'rol': 'admin'},
    'user1': {'contrasena': 'user1', 'rol': 'usuario'},
    'user2': {'contrasena': 'user2', 'rol': 'usuario'}
}

# Función de autenticación con validación de sesión
def login_requerido(rol_esperado=None):
    def decorador(funcion):
        def wrapper(*args, **kwargs):
            usuario = session.get('usuario')
            if not usuario:
                return redirect(url_for('login'))
            if rol_esperado and USUARIOS.get(usuario, {}).get('rol') != rol_esperado:
                return render_template('error_acceso.html', mensaje='Acceso denegado.')
            return funcion(*args, **kwargs)
        wrapper.__name__ = funcion.__name__
        return wrapper
    return decorador

# Página de inicio - Redirige al login si no hay sesión activa
@app.route('/')
def index():
    usuario = session.get('usuario')
    if usuario:
        if USUARIOS.get(usuario, {}).get('rol') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('usuario_perfil'))
    
    return redirect(url_for('login'))  # Si no hay sesión, va al login

# Página de login con validación
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = request.form['username']
        contrasena = request.form['password']

        if usuario in USUARIOS and USUARIOS[usuario]['contrasena'] == contrasena:
            session['usuario'] = usuario
            # Redirección según el rol
            if USUARIOS[usuario]['rol'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('usuario_perfil'))
        else:
            error = 'Usuario o contraseña incorrectos.'
    
    return render_template('login.html', error=error)

# Cerrar sesión
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

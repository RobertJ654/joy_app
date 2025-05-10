# joy_app

## Descripción

Un ayudante para la salud mental con el propósito de ayudar en el mapeo y recolección de datos para hacer proyecciones.

Integración de un chatbot psicológico para la ayuda inmediata y primeros auxilios psicológicos basados en el perfil del usuario.

Esta aplicación fue desarrollada como parte de una Hackaton de Neurotecnología "NEURO X PLORE"


## Instalación

Pasos para la instalación:

1.  **Clonar el repositorio (si aplica):**
    ```bash
    https://github.com/RobertJ654/joy_app.git
    cd joy_app
    ```

2.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuración de la base de datos:**
    * Asegúrate de tener un servidor MySQL corriendo.
    * Crea una base de datos llamada `stai_system`
    * Configura las credenciales de la base de datos en `app.py`:
        ```python
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = ''  # Reemplazar con la contraseña personal
        app.config['MYSQL_DB'] = 'stai_system'
        ```
    * Ejecutar con los Scripts de `init_db.sql`


## Ejecución

Ejecutar la aplicación con los siguientes comandos:

1.  **Ejecuta la aplicación Flask:**
    ```bash
    python app.py
    ```

3.  **Accede a la aplicación en tu navegador:**
    Ve a `http://127.0.0.1:5000` en tu navegador.


## Uso

[Describe cómo usar las diferentes funcionalidades de tu aplicación. Podrías mencionar las rutas principales y qué hacen.]

* **/login:** Página de inicio de sesión para usuarios y administradores.
* **/admin/dashboard:** Panel de control para administradores (requiere inicio de sesión con rol de administrador).
* **/usuario/perfil:** Perfil de usuario (requiere inicio de sesión con rol de usuario).
* **/usuario/chatbot:** Interfaz del chatbot (requiere inicio de sesión con rol de usuario).
* Más pestañas disponibles.


## Tecnologías Utilizadas

[Lista las principales tecnologías y librerías que utilizaste.]

* Python
* Flask
* Flask-MySQLdb
* Jinja2 (para las plantillas)


## Estado del Proyecto

**En Desarrollo Beta**.

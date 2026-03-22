import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- 1. ESTA PARTE ES NUEVA (Mejora la ruta de la base de datos) ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "Database", "landing_page.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        configuracion = conn.execute("SELECT * FROM configuracion_sitio LIMIT 1").fetchone()
        hero = conn.execute("SELECT * FROM hero LIMIT 1").fetchone()
        estadisticas = conn.execute("SELECT * FROM estadisticas ORDER BY orden").fetchall()
        cursos = conn.execute("SELECT * FROM cursos ORDER BY orden").fetchall()
        curso_caracteristicas = conn.execute("SELECT * FROM curso_caracteristicas ORDER BY curso_id, orden").fetchall()
        nosotros = conn.execute("SELECT * FROM nosotros LIMIT 1").fetchone()
        valores = conn.execute("SELECT * FROM valores ORDER BY orden").fetchall()
        conn.close()

        return render_template(
            'index.html',
            configuracion=configuracion,
            hero=hero,
            estadisticas=estadisticas,
            cursos=cursos,
            curso_caracteristicas=curso_caracteristicas,
            nosotros=nosotros,
            valores=valores
        )
    except sqlite3.OperationalError as e:
        return f"Error: No se encontró la base de datos o una tabla. Detalles: {e}"

# --- 2. REEMPLAZA TU FUNCIÓN ENVIAR POR ESTA (Con validaciones) ---
@app.route('/enviar-contacto', methods=['POST'])
def enviar_contacto():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')

    # Validación básica para que no guarde basura
    if not nombre or not email or not mensaje:
        return "Todos los campos son obligatorios", 400

    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO mensajes_contacto (nombre, email, mensaje) VALUES (?, ?, ?)",
            (nombre, email, mensaje)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error al guardar el mensaje: {e}"

if __name__ == '__main__':
    # Usamos debug=True para que veas los errores en el navegador
    app.run(debug=True)
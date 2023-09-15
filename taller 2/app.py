from flask import Flask, render_template, request, redirect, url_for
import pyodbc  # Para conectarse a la base de datos de Access

app = Flask(__name__)

# Configuración de la conexión a la base de datos Access
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\cuc\Documents\taller 2\TasksDB.accdb;'  # Cambia a la ubicación de tu archivo .accdb
)

@app.route('/')
def mostrar_tareas():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Tareas')
    tareas = cursor.fetchall()
    conn.close()
    return render_template('tareas.html', tareas=tareas)

@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    descripcion = request.form['descripcion']
    cursor.execute("INSERT INTO Tareas (descripcion) VALUES (?)", (descripcion,))
    conn.commit()
    conn.close()
    return redirect(url_for('mostrar_tareas'))

@app.route('/marcar_completada/<int:tarea_id>')
def marcar_completada(tarea_id):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("UPDATE Tareas SET estado = 1 WHERE id = ?", (tarea_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('mostrar_tareas'))

@app.route('/eliminar_tarea/<int:tarea_id>')
def eliminar_tarea(tarea_id):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tareas WHERE id = ?", (tarea_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('mostrar_tareas'))


if __name__ == '__main__':
    app.run(debug=True)
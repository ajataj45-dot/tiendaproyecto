from flask import Flask, request, redirect, render_template, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'


def get_db_connection():
    conn = sqlite3.connect("bd_tienda.db")  
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return redirect(url_for('clientes'))  






@app.route("/clientes")
def clientes():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route("/nuevo_cliente", methods=['GET','POST'])
def nuevo_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        telefono = request.form['telefono']
        conn = get_db_connection()
        conn.execute("INSERT INTO clientes (nombre, apellidos, telefono) VALUES(?,?,?)", (nombre, apellidos, telefono))
        conn.commit()
        conn.close()
        flash('Cliente agregado correctamente', 'success')
        return redirect(url_for('clientes'))
    return render_template('form_clientes.html')

@app.route('/cliente/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    conn = get_db_connection()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        telefono = request.form['telefono']
        conn.execute("UPDATE clientes SET nombre = ?, apellidos = ?, telefono = ? WHERE id = ?", (nombre, apellidos, telefono, id))
        conn.commit()
        conn.close()
        flash('Cliente actualizado', 'success')
        return redirect(url_for('clientes'))
    
    cliente = conn.execute("SELECT * FROM clientes WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template('form_clientes.html', cliente=cliente)

@app.route("/cliente/eliminar/<int:id>")
def eliminar_cliente(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Cliente eliminado', 'success')
    return redirect(url_for('clientes'))





if __name__ == '__main__':
    app.run(debug=True)
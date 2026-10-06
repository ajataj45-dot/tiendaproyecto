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





@app.route("/productos")
def productos():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route("/nuevo_producto", methods=['GET','POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre_producto = request.form['nombre_producto']
        precio = request.form['precio']
        stock = request.form['stock']
        conn = get_db_connection()
        conn.execute("INSERT INTO productos (nombre_producto, precio, stock) VALUES(?,?,?)",(nombre_producto, precio, stock))
        conn.commit()
        conn.close()
        flash('Producto agregado correctamente','success')
        return redirect(url_for('productos'))
    return render_template('form_producto.html')

@app.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conn = get_db_connection()
    if request.method == 'POST':
        nombre_producto = request.form['nombre_producto']
        precio = request.form['precio']
        stock = request.form['stock']
        conn.execute("UPDATE productos SET nombre_producto = ?, precio = ?, stock = ? WHERE id = ?", (nombre_producto, precio, stock, id))
        conn.commit()
        conn.close()
        flash ('Productos actualizados','success')
        return redirect(url_for('productos'))
    
    producto = conn.execute("SELECT * FROM productos WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template('form_producto.html', producto=producto)

@app.route("/producto/eliminar/<int:id>")
def eliminar_producto(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM productos WHERE id = ?",(id,))
    conn.commit()
    conn.close()
    flash('Producto eliminado','success')
    return redirect(url_for('productos'))








@app.route("/pedidos")
def pedidos():
    conn = get_db_connection()
    pedidos = conn.execute(
        """
        SELECT p.id, p.fecha_pedido, p.cantidad, 
               c.nombre ||' '|| c.apellidos as cliente, 
               pr.nombre_producto as producto
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        JOIN productos pr ON p.producto_id = pr.id
        """
    ).fetchall()
    conn.close()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route("/pedido/nuevo", methods=['GET','POST'])
def nuevo_pedido():
    conn = get_db_connection()
    if request.method == 'POST':
        fecha_pedido = request.form['fecha_pedido']
        cantidad = request.form['cantidad']
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        conn.execute(
            """
            INSERT INTO pedidos (fecha_pedido, cantidad, cliente_id, producto_id)
            VALUES(?,?,?,?)
            """,(fecha_pedido, cantidad, cliente_id, producto_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('pedidos'))
        
    clientes = conn.execute("SELECT id, nombre ||' '|| apellidos as nombre FROM clientes").fetchall()
    productos = conn.execute("SELECT id, nombre_producto FROM productos").fetchall()
    conn.close()
    return render_template('form_pedido.html', clientes=clientes, productos=productos)

@app.route("/pedido/eliminar/<int:id>")
def eliminar_pedido(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM pedidos WHERE id = ?",(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('pedidos'))




if __name__ == '__main__':
    app.run(debug=True)
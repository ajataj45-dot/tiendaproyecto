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








if __name__ == '__main__':
    app.run(debug=True)
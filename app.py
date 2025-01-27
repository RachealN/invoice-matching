from flask import Flask
from flask import render_template
from app import app 
import mysql.connector
app = Flask(__name__, template_folder='app/templates')


db_config = {
    'host': 'db',  
    'user': 'user',
    'password': 'secret123',
    'database': 'invoice-matching'
}

@app.route('/')
def home():
    return "<b>There has been a change</b>"


@app.route('/template')
def template():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices;") 
    data = cursor.fetchall()
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=80)
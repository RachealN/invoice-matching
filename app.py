from flask import Flask
from flask import render_template
from app import app 
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder='app/templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:secret123@db/invoice-matching'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Initialize SQLAlchemy
db = SQLAlchemy(app)


@app.route('/')
def home():
    return "<b>There has been a change</b>"


@app.route('/template')
def template(): 
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5000)

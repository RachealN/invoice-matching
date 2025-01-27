from flask import Flask
from flask import render_template
from app import app 
app = Flask(__name__, template_folder='app/templates')

@app.route('/')
def home():
    return "<b>There has been a change</b>"


@app.route('/template')
def template():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=80)
from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

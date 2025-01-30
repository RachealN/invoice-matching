from app import app 
from flask import render_template
from flask import Blueprint

bp = Blueprint("main", __name__)

@bp.route('/')
def index():
    return "Hello, World!"


@bp.route('/template')
def template():
    return render_template('home.html')
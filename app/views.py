from flask import Blueprint, render_template


bp = Blueprint('views', __name__)

@bp.route('/')
def index():
    return "Hello, World!"

@bp.route('/')
def home():
    return render_template('home.html')

from flask import Blueprint, render_template


bp = Blueprint('views', __name__)

@bp.route('/test')
def index():
    return "Hello, World - Testing!"

@bp.route('/')
def home():
    return render_template('home.html')

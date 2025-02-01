from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from app.routes.routes import routes 

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import invoice, invoice_line_item, delivery, delivery_line_item
    from routes.routes import routes
    app.register_blueprint(routes)

    from app.views import bp  
    app.register_blueprint(bp)

    return app

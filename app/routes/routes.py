from flask import Blueprint
from app.controllers.invoice_controller import invoice_controller
from app.routes.routes import routes

routes = Blueprint('invoice_routes', __name__)
routes.register_blueprint(invoice_controller, url_prefix='/invoices')

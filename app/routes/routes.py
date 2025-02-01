from flask import Blueprint
from app.controllers.invoice_controller import invoice_controller
from app.controllers.delivery_controller import delivery_controller

routes = Blueprint('invoice_routes', __name__)
routes.register_blueprint(invoice_controller, url_prefix='/invoices')
routes.register_blueprint(delivery_controller, url_prefix='/deliveries')

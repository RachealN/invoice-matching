from flask import Blueprint, jsonify
from app.services.delivery_service import DeliveryService

delivery_controller = Blueprint("delivery_controller", __name__)

@delivery_controller.route("/all", methods=["GET"])
def get_deliveries():
    deliveries = DeliveryService.get_all_deliveries()
    return jsonify({"deliveries": deliveries}), 200
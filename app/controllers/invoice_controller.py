from flask import Blueprint, jsonify
from app.services.invoice_service import MatchingService


invoice_controller = Blueprint('invoice_controller', __name__)

@invoice_controller.route("/match", methods=["POST"])
def match_invoices():
    result = MatchingService.process_invoice_matching()
    return jsonify(result)

@invoice_controller.route("/all", methods=["GET"])
def get_invoices():
    try:
        invoices = MatchingService.get_all_invoices()
        return jsonify({"invoices": invoices}), 200
    except Exception as e:
        print(f"Error fetching invoices: {str(e)}") 
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
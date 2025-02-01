from flask import Blueprint, jsonify
from app.services.invoice_matching_service import MatchingService

invoice_controller = Blueprint('invoice_controller', __name__)

@invoice_controller.route('/match', methods=['POST'])
def match_invoices():
    result = MatchingService.match_invoice_to_delivery()
    return jsonify(result)

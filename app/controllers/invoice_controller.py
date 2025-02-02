from flask import Blueprint, jsonify, request
from app.services.invoice_service import InvoiceService
from app.services.invoice_service import InvoiceService
from app.repositories.invoice_repository import InvoiceRepository
from app.services.delivery_service import DeliveryService
from app.services.invoice_service import InvoiceService


invoice_controller = Blueprint('invoice_controller', __name__)

@invoice_controller.route("/match", methods=["POST"])
def create_invoice_with_line_items():
    try:
        data = request.get_json()
        print("DEBUG: Received JSON payload:", data)

        # Validate payload
        validated = InvoiceService.validate_payload(data)
        if isinstance(validated, tuple):
            invoice_items_payload, delivery_numbers = validated
        else:
            return validated  

        # Create Invoice
        new_invoice = InvoiceService.create_invoice()

        # Create or Verify Deliveries
        DeliveryService.create_or_verify_deliveries(delivery_numbers)

        # Create Delivery Line Items
        DeliveryService.create_delivery_line_items(delivery_numbers)

        # Create Invoice Line Items
        invoice_items = InvoiceService.create_invoice_line_items(invoice_items_payload, new_invoice.id)
        if isinstance(invoice_items, tuple):  
            return jsonify(invoice_items), 400 

        InvoiceRepository.save_invoice_line_items(invoice_items)

        # Match Invoice Line Items with Deliveries
        matched, unmatched = InvoiceService.match_invoice_to_delivery(invoice_items, delivery_numbers)

        return jsonify({
            "message": "Invoice and line items created successfully",
            "matched": len(matched),
            "unmatched": len(unmatched),
            "matched_items": [item.to_dict() for item in matched]
        }), 201

    except Exception as e:
        print(f"DEBUG: Error encountered: {e}")
        return jsonify({"error": str(e)}), 500
    

@invoice_controller.route("/all", methods=["GET"])
def get_invoices():
    try:
        invoices = InvoiceService.get_all_invoices()
        return jsonify({"invoices": invoices}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
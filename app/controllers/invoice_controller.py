import uuid
from flask import Blueprint, jsonify, request
from app.services.invoice_service import MatchingService
from app.models.invoice_line_item import InvoiceLineItem
from app.services.invoice_service import MatchingService
from app.repositories.invoice_repository import InvoiceRepository
from app.models.invoice import Invoice
from app.models.invoice_line_item import InvoiceLineItem
from app.extensions import db


invoice_controller = Blueprint('invoice_controller', __name__)

@invoice_controller.route("/match", methods=["POST"])
def create_invoice_with_line_items():
    try:
        data = request.get_json()

        if 'invoice_items' not in data or 'delivery_numbers' not in data:
            return jsonify({"error": "Invalid request body, 'invoice_items' or 'delivery_numbers' are missing."}), 400

        # Create invoice
        new_invoice = Invoice(
            invoice_number=str(uuid.uuid4()),
            invoice_date="2025-01-01",
            customer_name="Customer X",
            total_amount=1000.00,
            currency="USD"
        )

        InvoiceRepository.save_invoice(new_invoice)
        db.session.commit() 

        # Create line items
        invoice_items = []
        for item in data['invoice_items']:
            line_item = InvoiceLineItem(
                invoice_id=new_invoice.id, 
                delivery_number=item['delivery_number'],
                title=item['title'],
                unit=item['unit'],
                amount=item['amount'],
                price=item['price'],
                description=item.get('description', None),
                subtotal=item.get('subtotal', 0.0)
            )
            invoice_items.append(line_item)

        # Save the line items
        InvoiceRepository.save_invoice_line_items(invoice_items)

        # Match line items to deliveries
        matched, unmatched = MatchingService.match_invoice_to_delivery(invoice_items, data['delivery_numbers'])

        matched_items = [item.to_dict() for item in matched]

        return jsonify({
            "message": "Invoice and line items created successfully",
            "matched": len(matched),
            "unmatched": len(unmatched),
            "matched_items": matched_items 
        }), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@invoice_controller.route("/all", methods=["GET"])
def get_invoices():
    try:
        invoices = MatchingService.get_all_invoices()
        return jsonify({"invoices": invoices}), 200
    except Exception as e:
        print(f"Error fetching invoices: {str(e)}") 
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
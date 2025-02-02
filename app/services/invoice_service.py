from app.repositories.delivery_repository import DeliveryRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.models.invoice_line_item import InvoiceLineItem
from app.models.invoice import Invoice
from flask import jsonify
from app.extensions import db


class InvoiceService:

    @staticmethod
    def get_all_invoices():
        try:
            invoices = InvoiceRepository.get_all_invoices()
            return [invoice.to_dict() for invoice in invoices]  
        except Exception as e:
            raise e  

    @staticmethod
    def match_invoice_to_delivery(invoice_items, delivery_numbers):
        matched_invoices = []
        unmatched_invoices = []
        
        for invoice_item in invoice_items:
            if invoice_item.delivery_number in delivery_numbers:
                matched_invoices.append(invoice_item)
            else:
                unmatched_invoices.append(invoice_item)
        
        return matched_invoices, unmatched_invoices
    
    @staticmethod
    def validate_payload(data):
        if 'invoice_items' not in data or 'delivery_numbers' not in data:
            return jsonify({
                "error": "Invalid request body, 'invoice_items' or 'delivery_numbers' are missing."
            }), 400

        invoice_items_payload = data.get('invoice_items')
        if not isinstance(invoice_items_payload, list):
            return jsonify({"error": "'invoice_items' should be a list."}), 400

        required_item_keys = ['delivery_number', 'title', 'unit', 'amount', 'price']
        for idx, item in enumerate(invoice_items_payload):
            if not isinstance(item, dict):
                return jsonify({"error": f"Invoice item at index {idx} is not a valid object."}), 400
            for key in required_item_keys:
                if key not in item:
                    return jsonify({"error": f"Missing key '{key}' in invoice_items at index {idx}."}), 400

        delivery_numbers = data.get('delivery_numbers', {})
        return (invoice_items_payload, delivery_numbers)
    
    @staticmethod
    def create_invoice():
        last_invoice = db.session.query(Invoice).order_by(Invoice.id.desc()).first()
        new_invoice_number = f"INV-{int(last_invoice.invoice_number.split('-')[1]) + 1:04d}" if last_invoice else "INV-0001"

        new_invoice = Invoice(
            invoice_number=new_invoice_number,
            invoice_date="2025-01-01",
            customer_name="Customer X",
            total_amount=1000.00,
            currency="USD"
        )
        InvoiceRepository.save_invoice(new_invoice)
        db.session.commit()
        return new_invoice

    @staticmethod
    def create_invoice_line_items(invoice_items_payload, invoice_id):
        invoice_items = []
        for idx, item in enumerate(invoice_items_payload):
            try:
                line_item = InvoiceLineItem(
                    invoice_id=invoice_id,
                    delivery_number=item['delivery_number'],
                    title=item['title'],
                    unit=item['unit'],
                    amount=item['amount'],
                    price=item['price'],
                    description=item.get('description', None),
                    subtotal=item.get('subtotal', 0.0)
                )
                invoice_items.append(line_item)
            except KeyError as ke:
                return {"error": f"Missing key {ke} in invoice_items at index {idx}."}, 400

        return invoice_items

    @staticmethod
    def process_invoice_matching():
        try:
            invoice_items = InvoiceRepository.get_all_invoice_line_items()
            if not invoice_items:
                return {"message": "No invoice line items found"}, 400

            delivery_numbers = DeliveryRepository.get_all_delivery_numbers() 
            return InvoiceService.match_invoice_to_delivery(invoice_items, delivery_numbers)

        except Exception as e:
            return {"message": "Internal server error", "error": str(e)}, 500

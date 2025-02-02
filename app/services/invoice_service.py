import difflib
from rapidfuzz import fuzz, process
from app.repositories.delivery_repository import DeliveryRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.models.delivery_line_item import DeliveryLineItem


class MatchingService:

    def get_all_invoices():
        try:
            invoices = InvoiceRepository.get_all_invoices()
            return [invoice.to_dict() for invoice in invoices]  
        except Exception as e:
            print(f"Database error: {e}")
            raise e  

    @staticmethod
    def find_best_match(invoice_number, delivery_numbers):
        # Fuzzy matching using difflib
        matches = difflib.get_close_matches(invoice_number, delivery_numbers, n=1, cutoff=0.8)
        return matches[0] if matches else None

    def match_invoice_to_delivery(invoice_items, delivery_numbers):
        matched_invoices = []
        unmatched_invoices = []

        # Group deliveries by delivery_number
        grouped_delivery_items = {}
        for delivery_number, delivery_item in delivery_numbers.items():
            grouped_delivery_items.setdefault(delivery_number, []).append(delivery_item)

        for invoice_item in invoice_items:
            delivery_items_for_number = grouped_delivery_items.get(invoice_item.delivery_number)

            if delivery_items_for_number:
                matched = False
                for delivery_item in delivery_items_for_number:
                    # Match by comparing amount, title, unit,delivery_number
                    if (invoice_item.amount == delivery_item['amount'] and
                            invoice_item.title.lower() == delivery_item['title'].lower() and
                            invoice_item.unit.lower() == delivery_item['unit'].lower()):
                        # Add matched invoice item to matched_invoices
                        matched_invoices.append(invoice_item)
                        matched = True
                        break

                if not matched:
                    unmatched_invoices.append(invoice_item)
            else:
                unmatched_invoices.append(invoice_item)

        return matched_invoices, unmatched_invoices

    @staticmethod
    def process_invoice_matching():
        try:
            invoice_items = InvoiceRepository.get_all_invoice_line_items()
            if not invoice_items:
                return {"message": "No invoice line items found"}, 400

            delivery_numbers = DeliveryRepository.get_all_delivery_numbers() 
            return MatchingService.match_invoice_to_delivery(invoice_items, delivery_numbers)

        except Exception as e:
            print(f"Error in MatchingService: {e}")
            return {"message": "Internal server error", "error": str(e)}, 500

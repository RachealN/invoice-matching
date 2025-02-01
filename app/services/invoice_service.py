from rapidfuzz import fuzz, process
from app.repositories.delivery_repository import DeliveryRepository
from app.repositories.invoice_repository import InvoiceRepository


class MatchingService:

    def get_all_invoices():
        try:
            invoices = InvoiceRepository.get_all_invoices()
            return [invoice.to_dict() for invoice in invoices]  
        except Exception as e:
            print(f"Database error: {e}")
            raise e  

    @staticmethod
    def find_best_match(delivery_number, delivery_numbers, threshold=85):
        best_match = process.extractOne(delivery_number, delivery_numbers, scorer=fuzz.ratio)
        return best_match[0] if best_match and best_match[1] >= threshold else None

    @staticmethod
    def match_invoice_to_delivery(invoice_items, delivery_numbers):
        matched_invoices = []  
        unmatched_invoices = [] 
        
        for invoice_line in invoice_items:
            exact_match = delivery_numbers.get(invoice_line.delivery_number)

            if exact_match:
                invoice_line.delivery_id = exact_match
                matched_invoices.append(invoice_line)  
            else:
                best_match = MatchingService.find_best_match(invoice_line.delivery_number, list(delivery_numbers.keys()))
                if best_match:
                    invoice_line.delivery_id = delivery_numbers[best_match]
                    matched_invoices.append(invoice_line) 
                else:
                    unmatched_invoices.append(invoice_line)

            InvoiceRepository.update_invoice(invoice_line)

        # Return both matched and unmatched invoices
        return {
            "message": "Matching process completed",
            "matched": len(matched_invoices),
            "unmatched": len(unmatched_invoices),
            "matched_invoices": [invoice.to_dict() for invoice in matched_invoices]
        }

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

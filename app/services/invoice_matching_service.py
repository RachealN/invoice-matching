from rapidfuzz import fuzz, process
from app.repositories.delivery_repository import DeliveryRepository
from app.repositories.invoice_repository import InvoiceRepository

class MatchingService:
    @staticmethod
    def find_best_match(delivery_number, delivery_numbers, threshold=85):
        """Finds the best fuzzy match for a delivery number from available delivery numbers."""
        best_match = process.extractOne(delivery_number, delivery_numbers, scorer=fuzz.ratio)
        if best_match and best_match[1] >= threshold:
            return best_match[0]  
        return None 
    @staticmethod
    def match_invoice_to_delivery():
        """Matches invoice line items to delivery line items using exact and fuzzy matching."""
        deliveries = DeliveryRepository.get_all_delivery_numbers()
        unmatched_invoices = []

        for invoice_line in InvoiceRepository.get_all_invoice_line_items():
            exact_match = deliveries.get(invoice_line.delivery_number)

            if exact_match:
                invoice_line.delivery_id = exact_match
            else:
                best_match = MatchingService.find_best_match(invoice_line.delivery_number, list(deliveries.keys()))
                if best_match:
                    invoice_line.delivery_id = deliveries[best_match]
                else:
                    unmatched_invoices.append(invoice_line)

            InvoiceRepository.update_invoice(invoice_line)

        return {"message": "Matching process completed", "unmatched": len(unmatched_invoices)}

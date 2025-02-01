from app.models.invoice_line_item import InvoiceLineItem
from app.models.invoice import Invoice
from app import db

class InvoiceRepository:
    @staticmethod
    def get_all_invoices():
        return Invoice.query.all()
    
    @staticmethod
    def get_all_invoice_line_items():
        return InvoiceLineItem.query.all()

    @staticmethod
    def update_invoice(invoice_line_item):
        db.session.add(invoice_line_item)
        db.session.commit()
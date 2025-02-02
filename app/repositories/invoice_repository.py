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
    def save_invoice(invoice):
        db.session.add(invoice)
        db.session.commit()
        return invoice

    @staticmethod
    def save_invoice_line_items(line_items):
        db.session.bulk_save_objects(line_items)
        db.session.commit()

    @staticmethod
    def update_invoice(invoice_line_item):
        db.session.add(invoice_line_item)
        db.session.commit()

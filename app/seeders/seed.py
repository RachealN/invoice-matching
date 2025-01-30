from app import create_app, db
from app.models.invoice import Invoice
from app.models.delivery import Delivery
from app.models.invoice_line_item import InvoiceLineItem
from app.models.delivery_line_item import DeliveryLineItem

import uuid
from datetime import datetime

def seed_data():
    app = create_app()

    with app.app_context():
        print("Creating tables...")
        db.create_all()

        if Invoice.query.first():
            print("⚠️ Database already seeded. Skipping...")
            return
        
        # Create invoices
        macbook_invoice = Invoice(
            id=str(uuid.uuid4()),
            invoice_number="INV001",  
            invoice_date=datetime(2025, 1, 1),  
            customer_name="Apple",  
            total_amount=4000.00,  
            currency="USD" 
        )

        iphone_invoice = Invoice(
            id=str(uuid.uuid4()),
            invoice_number="INV002",  
            invoice_date=datetime(2025, 1, 1),  
            customer_name="Apple", 
            total_amount=8000.00,  
            currency="USD"  
        )

        db.session.add_all([macbook_invoice, iphone_invoice])
        
        # Create invoice line items 
        macbook_invoice_line_item = InvoiceLineItem(
            invoice_id=macbook_invoice.id,  
            delivery_number="D345",
            title="macbook",
            unit="pcs",
            amount=4,
            price=1000.00
        )
        iphone_invoice_line_item = InvoiceLineItem(
            invoice_id=iphone_invoice.id,  
            delivery_number="D456",
            title="iphone",
            unit="pcs",
            amount=8,
            price=1000.00
        )
        db.session.add_all([macbook_invoice_line_item, iphone_invoice_line_item])

        # Create delivery entries
        macbook_delivery = Delivery(
            id=str(uuid.uuid4()), 
            delivery_number="D345", 
            delivery_date=datetime(2025, 1, 1)  
        )
        iphone_delivery = Delivery(
            id=str(uuid.uuid4()), 
            delivery_number="D456", 
            delivery_date=datetime(2025, 1, 1)  
        )
        db.session.add_all([macbook_delivery, iphone_delivery])

        macbook_delivery_line_item = DeliveryLineItem(
            delivery_id=macbook_delivery.id, 
            title="macbook",
            unit="pcs",
            amount=2
        )
        iphone_delivery_line_item = DeliveryLineItem(
            delivery_id=iphone_delivery.id,  
            title="iphone",
            unit="pcs",
            amount=2
        )
        db.session.add_all([macbook_delivery_line_item, iphone_delivery_line_item])

        db.session.commit()
        print("✅ Database successfully seeded.")

if __name__ == "__main__":
    seed_data()

import uuid
from app.extensions import db

class Invoice(db.Model):
    __tablename__ = 'invoice'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_number = db.Column(db.String(255), nullable=False, unique=True)
    invoice_date = db.Column(db.Date, nullable=False)
    customer_name = db.Column(db.String(255), nullable=True)
    total_amount = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(10), nullable=True)


    def to_dict(self):
        return {
            "customer": self.customer_name,
            "invoice_number": self.invoice_number,
            "amount": self.total_amount
        }

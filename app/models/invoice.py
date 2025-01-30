import uuid
from app.app import db

class Invoice(db.Model):
    __tablename__ = 'invoice'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
   
    line_items = db.relationship('InvoiceLineItem', backref='invoice', lazy=True)
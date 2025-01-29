from models.database import db

class InvoiceLineItem(db.Model):
    __tablename__ = 'invoice_line_item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    delivery_number = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

    invoice_id = db.Column(db.String(36), db.ForeignKey('invoice.id'), nullable=False)

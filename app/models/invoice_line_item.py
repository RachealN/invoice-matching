from app.extensions import db

class InvoiceLineItem(db.Model):
    __tablename__ = 'invoice_line_item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.String(36), db.ForeignKey('invoice.id'), nullable=False)
    line_item_number = db.Column(db.Integer, nullable=True)
    delivery_number = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    subtotal = db.Column(db.Float, nullable=False, default=0.0)

    invoice = db.relationship('Invoice', backref='line_items')

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'delivery_number': self.delivery_number,
            'title': self.title,
            'unit': self.unit,
            'amount': self.amount,
            'price': self.price,
            'description': self.description,
            'subtotal': self.subtotal
        }

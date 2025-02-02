from app.extensions import db

class DeliveryLineItem(db.Model):
    __tablename__ = 'delivery_line_item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    delivery_id = db.Column(db.String(36), db.ForeignKey('delivery.id'), nullable=False)
    delivery_number = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    delivery = db.relationship('Delivery', backref='line_items') 

    def to_dict(self):
        return {
            "id": self.id,
            "delivery_number": self.delivery_number,
            "title": self.title,
            "unit": self.unit,
            "amount": self.amount
        }


from app.extensions import db

class DeliveryLineItem(db.Model):
    __tablename__ = 'delivery_line_item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    delivery_id = db.Column(db.String(36), db.ForeignKey('delivery.id'), nullable=False)
    line_item_number = db.Column(db.Integer, nullable=True) 
    title = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    delivery_id = db.Column(db.String(36), db.ForeignKey('delivery.id'), nullable=False)

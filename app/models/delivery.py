import uuid
from app.app import db

class Delivery(db.Model):
    __tablename__ = 'delivery'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    delivery_number = db.Column(db.String(255), nullable=False, unique=True)
    
    line_items = db.relationship('DeliveryLineItem', backref='delivery', lazy=True)

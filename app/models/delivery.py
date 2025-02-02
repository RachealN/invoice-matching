import uuid
from app.extensions import db

class Delivery(db.Model):
    __tablename__ = 'delivery'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    delivery_number = db.Column(db.String(255), nullable=False, unique=True)
    supplier_name = db.Column(db.String(255), nullable=True)
    delivery_date = db.Column(db.Date, nullable=False)  

    def to_dict(self):
        return {
            "Supplier": self.supplier_name,
            "delivery_number": self.delivery_number,
            "status": self.delivery_date
        }


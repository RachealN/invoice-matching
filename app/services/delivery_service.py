from app.repositories.delivery_repository import DeliveryRepository
from app.models.delivery import Delivery
from app.models.delivery_line_item import DeliveryLineItem
from app.extensions import db

class DeliveryService:

    @staticmethod
    def get_all_deliveries():
        deliveries = DeliveryRepository.get_all_deliveries()
        return [delivery.to_dict() for delivery in deliveries] if deliveries else []
    
    @staticmethod
    def create_delivery_line_items(delivery_numbers):
        for delivery_number, delivery_data in delivery_numbers.items():
            delivery = db.session.query(Delivery).filter_by(delivery_number=delivery_number).first()
            
            for idx, delivery_item in enumerate(delivery_data.get('line_items', [])):
                delivery_line_item = DeliveryLineItem(
                    delivery_id=delivery.id,
                    delivery_number=delivery.delivery_number,
                    title=delivery_item['title'],
                    unit=delivery_item['unit'],
                    amount=delivery_item['amount'],
                )
                db.session.add(delivery_line_item)
            db.session.commit()

    @staticmethod
    def create_or_verify_deliveries(delivery_numbers):
        for delivery_number, delivery_data in delivery_numbers.items():
            existing_delivery = db.session.query(Delivery).filter_by(delivery_number=delivery_number).first()
            if not existing_delivery:
                new_delivery = Delivery(
                    delivery_number=delivery_number,
                    supplier_name=delivery_data.get('supplier_name', None),
                    delivery_date="2025-01-01"  
                )
                db.session.add(new_delivery)
                db.session.commit()
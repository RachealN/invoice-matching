from app.models.delivery import Delivery

class DeliveryRepository:
    @staticmethod
    def get_all_deliveries():
        return Delivery.query.all()
    
    @staticmethod
    def get_all_delivery_numbers():
        deliveries = Delivery.query.all()
        return {delivery.delivery_number: delivery.id for delivery in deliveries}


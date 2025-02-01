from app.repositories.delivery_repository import DeliveryRepository

class DeliveryService:
    @staticmethod
    def get_all_deliveries():
        deliveries = DeliveryRepository.get_all_deliveries()
        return [delivery.to_dict() for delivery in deliveries] if deliveries else []
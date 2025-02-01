from app.models.delivery import DeliveryLineItem

class DeliveryRepository:
    @staticmethod
    def get_all_delivery_numbers():
        return {d.delivery_number: d.id for d in DeliveryLineItem.query.all()}

from app.models.delivery_line_item import DeliveryLineItem

class DeliveryRepository:
    @staticmethod
    def get_all_delivery_numbers():
        return {d.delivery_number: d.id for d in DeliveryLineItem.query.all()}

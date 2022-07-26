from project_properties.models import Order


def is_order_exists(order_title):
    return Order.objects.filter(title=order_title).exists()

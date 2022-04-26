from items import Items
from discounts import Discounts
from orders import Order, AppOrder
from notifications import Notifications, Restaurants
from utilities import PaymentMode


def main() -> None:
    """Whole lifecycle of an order"""

    # what needs to ordered , and from where --
    new_item = Items('Dosa', 5, 50)
    restaurant = Restaurants.Swadishtam
    applied_disc = Discounts(discount_coupon='NET05')

    # how the user will pay --
    PaymentMode.about()
    user_payment_mode = PaymentMode.net
    print(f"selected payment mode is -- {user_payment_mode.value}")

    # new order creation --
    new_order: Order = AppOrder(order_items=new_item, order_restaurant=restaurant, order_discounts=applied_disc)
    info = new_order.order_info()
    print(info)

    # order verification --
    new_order.verify_order()

    # order payment
    new_order.order_payment(user_payment_mode)

    # order notification to restaurant
    Notifications.notify_restaurant(new_order.order_restaurant)

    # order cancellation
    new_order.cancel_order()


if __name__ == "__main__":
    main()

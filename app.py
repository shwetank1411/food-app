from items import Items
from discounts import Discounts
from orders import Order,AppOrder
from notifications import Notifications
from utilities import PaymentMode
from notifications import Restaurants


def main() ->None :

    new_item =  Items('Dosa',5,50)
    restaurant = Restaurants.Swadishtam
    applied_disc = Discounts(discount_coupon='NET05')
    user_payment_mode = PaymentMode.net
    
    new_order :Order = AppOrder(order_items=new_item,order_restaurant=restaurant,order_discounts=applied_disc)
    
    info = new_order.order_info()
    print(info)
    new_order.verify_order()
    new_order.order_payment(user_payment_mode)
    Notifications.notify_restaurant(new_order.order_restaurant)
    new_order.cancel_order()
    
 if __name__ == "__main__":
 
     main()
from typing import Protocol
from dataclasses import dataclass

from items import Items
from discounts import Discounts
from payments import PaymentProcessor
from utilities import PaymentMode
from notifications import Restaurants

from exceptions import OrderExceptions

@dataclass
class Order(Protocol):

    order_items: Items
    order_restaurant: Restaurants
    order_discounts: Discounts
    order_payment_processor: PaymentProcessor
    payment_mode:PaymentMode

    def order_info(self) ->str:
        ...
    def verify_order(self) -> None:
        ...
    def order_payment(self , payment_mode :PaymentMode) -> None:
        ...
    def cancel_order(self) -> None:
        ...

class AppOrder:

    def __init__(self,order_items :Items,order_restaurant :Restaurants,order_discounts :Discounts) -> None:
        self.order_items = order_items
        self.order_discounts  = order_discounts
        self.order_payment_processor: PaymentProcessor = PaymentProcessor.DEFAULT_NONE_PROCESSOR
        self.order_restaurant = order_restaurant
        self.payment_mode = PaymentMode.non
        print('App Order Created')

    def order_info(self) ->str:
        return f"App Order placed for {self.order_restaurant.name} --\n"\
                + f"    *** ordered item = {self.order_items.item_name} ,ordered item quantity = {self.order_items.item_count} ,"\
                + f"priced at {self.order_items.item_price} per item ***"

    @property
    def _order_amount(self) ->int:
        return self.order_items.item_count * self.order_items.item_price

    @_order_amount.setter
    def _order_amount(self,amt) ->None:
        raise OrderExceptions("The Order Amount is derived and hence can not be set or changed explicitly.")

    def verify_order(self) -> None:
        print(f"Verifying app order for {self.order_items.item_name}  ...")
        print("App order verified")

    def order_payment(self, payment_mode :PaymentMode) ->None:
        self._set_payment_mode(payment_mode)
        print(f"Order Amount = {self._order_amount}")
        net_order_amount = self._calculate_net_order_amount()
        print("The payment through App is being processed....")
        self.order_payment_processor = PaymentProcessor(net_order_amount,payment_mode)
        self.order_payment_processor.process_payment()
        print("Thanks....Payment Completed Successfully on the App")

    def _set_payment_mode(self,payment_mode:PaymentMode) ->None:
        if not payment_mode:
            raise OrderExceptions(f"Payment Mode is needed!")
        self.payment_mode = payment_mode

    def _calculate_net_order_amount(self) ->float:
        if self.order_discounts.discount_coupon or self.order_discounts.flat_discount_amount > 0:
            order_discount :float = self._calculate_discount_amount()
        else:
            order_discount = 0
        net_order_amount = self._order_amount - order_discount
        if order_discount > 0 :
            print(f"Order Amount slashed to {net_order_amount}")
        return net_order_amount

    def _calculate_discount_amount(self) ->float:
        if self.order_discounts.discount_coupon :
            order_discount = self.order_discounts.apply_discount(amount =self._order_amount,payment_mode=self.payment_mode)
        elif self.order_discounts.flat_discount_amount > 0:
            order_discount = self.order_discounts.apply_discount(amount =self._order_amount)
        else:
            order_discount = 0
        return order_discount

    def cancel_order(self) -> None:
        print("*************ORDER CANCELLATION REQUESTED******************")
        self.order_payment_processor.reverse_payment()
        print("*************ORDER CANCELLED*******************************")
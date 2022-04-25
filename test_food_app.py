import unittest
from items import Items
from discounts import Discounts
from notifications import Restaurants
from orders import AppOrder
from utilities import Fees,Taxes,PaymentMode
from exceptions import ItemExceptions,DiscountsExceptions

class TestClassFactory:

    @staticmethod
    def create_test_instance(test_class,*class_test_parameters,**class_test_kw_parameters):
        return test_class(**class_test_kw_parameters) \
            if  test_class == Discounts \
            else test_class(*class_test_parameters)


class TestFoodApp(unittest.TestCase):

    def test_is_created_item_valid(self):
        """if the Items instance is created without raising ItemExceptions then the created item instance is valid"""
        test_class = Items
        test_item_name :str   = 'Dosa'
        test_item_count :int  =  5
        test_item_price :int  =  50
        try:
            test_item_instance = TestClassFactory.create_test_instance(test_class,test_item_name,test_item_count,test_item_price)
        except ItemExceptions:
            test_item_instance = None
        self.assertIsInstance(test_item_instance,test_class)

    def test_is_created_coupon_discount_valid(self):
        test_class = Discounts
        test_discount_coupon = 'CDT15'
        try:
            test_discount_instance = TestClassFactory.create_test_instance(test_class,discount_coupon=test_discount_coupon)
        except DiscountsExceptions:
            test_discount_instance = None
        self.assertIsInstance(test_discount_instance,test_class)

    def test_is_created_flat_discount_valid(self):
        test_class = Discounts
        test_flat_discount_amount = 100
        try:
            test_discount_instance = TestClassFactory.create_test_instance(test_class,flat_discount_amount=test_flat_discount_amount)
        except DiscountsExceptions:
            test_discount_instance = None
        self.assertIsInstance(test_discount_instance,test_class)

    def test_is_app_order_info_valid(self):
        test_class = AppOrder
        test_order_items = TestClassFactory.create_test_instance(Items,'Dosa',5,50)
        test_order_restaurant = Restaurants.Swadishtam
        test_order_discounts = TestClassFactory.create_test_instance(Discounts,flat_discount_amount=100)
        test_apporder_instance = TestClassFactory.create_test_instance(test_class,test_order_items,
                                                                       test_order_restaurant,test_order_discounts)
        test_info = test_apporder_instance.order_info()
        valid_info = f"App Order placed for {test_apporder_instance.order_restaurant.name} --\n"\
                + f"    *** ordered item = {test_apporder_instance.order_items.item_name} ," \
                + f"ordered item quantity = {test_apporder_instance.order_items.item_count} ,"\
                + f"priced at {test_apporder_instance.order_items.item_price} per item ***"
        self.assertEqual(test_info,valid_info)

    def test_is_app_order_amount_valid(self):
        test_class = AppOrder
        test_order_items = TestClassFactory.create_test_instance(Items, 'Dosa', 5, 50)
        test_order_restaurant = Restaurants.Swadishtam
        test_order_discounts = TestClassFactory.create_test_instance(Discounts, flat_discount_amount=100)
        test_apporder_instance = TestClassFactory.create_test_instance(test_class,test_order_items,
                                                                       test_order_restaurant,test_order_discounts)
        test_order_amount = test_apporder_instance._order_amount
        valid_order_amount = test_order_items.item_count * test_order_items.item_price
        self.assertEqual(test_order_amount,valid_order_amount)

    def test_is_app_order_amount_after_discount_valid(self):
        test_class = AppOrder
        test_order_items = TestClassFactory.create_test_instance(Items, 'Dosa', 5, 50)
        test_order_restaurant = Restaurants.Swadishtam
        test_order_discounts = TestClassFactory.create_test_instance(Discounts, flat_discount_amount=100)
        test_apporder_instance = TestClassFactory.create_test_instance(test_class,test_order_items,
                                                                       test_order_restaurant,test_order_discounts)
        test_net_order_amount = test_apporder_instance._order_amount - test_order_discounts.flat_discount_amount
        valid_order_amount = test_order_items.item_count * test_order_items.item_price
        valid_net_order_amount = valid_order_amount - test_order_discounts.flat_discount_amount
        self.assertEqual(test_net_order_amount,valid_net_order_amount)

    def test_is_delivery_fee_amount_valid(self):
        test_class = Fees
        test_base_amount = 100
        test_fees_instance = TestClassFactory.create_test_instance(test_class)
        test_delivery_fee_amount = test_fees_instance.get_delivery_flat_fee(test_base_amount)
        valid_delivery_fee_amount = 0
        self.assertEqual(test_delivery_fee_amount,valid_delivery_fee_amount)

    def test_is_calculated_total_tax_amount_valid(self):
        test_class = Taxes
        test_base_amount = 500.12
        test_taxes_instance = TestClassFactory.create_test_instance(test_class)
        test_tax_amount_tuple = test_taxes_instance.calculate_GST(test_base_amount)
        valid_CGST_tax_amount :float = round(test_base_amount * 0.09,2)
        valid_SGST_tax_amount :float = round(test_base_amount * 0.09,2)
        valid_total_tax_amount = valid_CGST_tax_amount + valid_SGST_tax_amount
        valid_tax_amount_tuple = (valid_CGST_tax_amount,valid_SGST_tax_amount,valid_total_tax_amount)
        self.assertTupleEqual(test_tax_amount_tuple,valid_tax_amount_tuple)

    def test_is_payment_mode_valid_for_discount_coupon(self):
        test_class = Discounts
        test_discount_coupon = 'CDT15'
        test_payment_mode = PaymentMode.cdt
        test_discount_instance = TestClassFactory.create_test_instance(test_class,discount_coupon=test_discount_coupon)
        self.assertTrue(test_payment_mode,test_discount_instance._is_valid_paymode_for_discount_coupon)

    def test_is_reversed_payment_amount_valid(self):
        test_class = AppOrder
        test_order_items = TestClassFactory.create_test_instance(Items, 'Dosa', 5, 50)
        test_order_restaurant = Restaurants.Swadishtam
        test_order_discounts = TestClassFactory.create_test_instance(Discounts, flat_discount_amount=100)
        test_payment_mode = PaymentMode.upi
        test_apporder_instance = TestClassFactory.create_test_instance(test_class,test_order_items,
                                                                       test_order_restaurant,test_order_discounts)
        test_apporder_instance.order_payment(test_payment_mode)
        test_reverse_payment_amount = test_apporder_instance.order_payment_processor.calculate_reverse_payment_amount()
        valid_reverse_payment_amount = test_apporder_instance.order_payment_processor._total_payment_amt
        self.assertEqual(test_reverse_payment_amount,valid_reverse_payment_amount)

if __name__ == "__main__":
    unittest.main()
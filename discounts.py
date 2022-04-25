from utilities import PaymentMode
from exceptions import DiscountsExceptions

class DiscountsMeta(type):

    def __call__(cls,*args,**kwargs):
        if args :
            raise DiscountsExceptions(f"Discounts class Usage --> Only keyword arguments needed")
        elif len(kwargs) > 1 :
            raise DiscountsExceptions("Discounts class Usage --> Discounts can be either Coupon --or-- Flat")
        elif len(kwargs) == 0 :
            raise DiscountsExceptions("Discounts class Usage --> Provide either Coupon code --or-- Flat Discount")
        return super().__call__(**kwargs)

class Discounts(metaclass=DiscountsMeta):

    APP10: float = 0.10
    UPI20: float = 0.20
    CDT15: float = 0.15
    DBT05: float = 0.05
    NET05: float = 0.05

    ALLOWED_PAYMODES :list = ['dbt','cdt','net','upi']

    @classmethod
    def  is_discount_code_valid(cls,discount_code) -> bool:
        if discount_code not in vars(cls):
            raise DiscountsExceptions(f"Invalid Discount Code -- {discount_code}")
        return True

    @classmethod
    def  is_flat_discount_amount_valid(cls,discount_amount) -> bool:
        if discount_amount  <= 0:
            raise DiscountsExceptions(f"Invalid flat discount amount -- {discount_amount}  -- should be greater than 0")
        return True

    def __init__(self,discount_coupon=None,flat_discount_amount=None):
        if discount_coupon and Discounts.is_discount_code_valid(discount_coupon):
            self.discount_coupon  = discount_coupon
            self.flat_discount_amount = None
        elif  flat_discount_amount is not None and Discounts.is_flat_discount_amount_valid(flat_discount_amount):
            self.flat_discount_amount  = flat_discount_amount
            self.discount_coupon = None

    def _is_valid_paymode_for_discount_coupon(self,payment_mode :PaymentMode) -> bool:
        is_valid_paymode_coupon :bool = True
        discount_coupon_paymode :str = self.discount_coupon[:3].lower()
        try:
            payment_mode_name = getattr(PaymentMode,payment_mode.name).name
        except AttributeError:
            raise DiscountsExceptions(f"Invalid Payment Mode - {payment_mode}")
        if discount_coupon_paymode in self.ALLOWED_PAYMODES\
                and discount_coupon_paymode != payment_mode_name :
            is_valid_paymode_coupon = False
        return  is_valid_paymode_coupon

    def _is_valid_flat_discount_amount(self,order_amount :float) -> bool:
        is_valid :bool = True
        if self.flat_discount_amount > order_amount:
            is_valid: bool = False
        return is_valid

    def apply_discount(self,amount:float,payment_mode:PaymentMode = None) ->float:
        discount :float = 0
        if self.discount_coupon :
            discount = self._apply_discount_coupon(amount,payment_mode)
        elif self.flat_discount_amount > 0:
            discount = self._apply_flat_discount(amount)
        return discount

    def _apply_discount_coupon(self,amount:float,payment_mode:PaymentMode) ->float:
        coupon_discount: float = 0
        if self._is_valid_paymode_for_discount_coupon(payment_mode):
            coupon_discount = self._get_discount_amount_for_coupon(amount)
            print(f"Whoaa..!! Applied {self.discount_coupon} to avail discount of {coupon_discount}")
        else:
            raise DiscountsExceptions(f"Discount Coupon {self.discount_coupon} is not valid for payment mode = {payment_mode.value}")
        return coupon_discount

    def _apply_flat_discount(self,amount:float ) ->float:
        flat_discount: float = 0
        if self._is_valid_flat_discount_amount(amount):
            flat_discount = self.flat_discount_amount
            print(f"WoW..!! Availed flat discount of {flat_discount}")
        else:
            raise DiscountsExceptions(f"Flat Discount NOT applied -- Invalid flat discount amount = {self.flat_discount_amount}")
        return flat_discount

    def _get_discount_amount_for_coupon(self,base_amount: float) -> float:
        discount_percentage = self._get_discount_percentage_for_valid_discount_code()
        return base_amount * discount_percentage

    def _get_discount_percentage_for_valid_discount_code(self) -> float:
        disc_per = getattr(self, self.discount_coupon)
        return disc_per
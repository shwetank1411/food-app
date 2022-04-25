class BusinessExceptions(Exception):
    """Base class for Business Exceptions"""

class OrderExceptions(BusinessExceptions):
    """Exceptions arising from class of Order Type"""

    def __init__(self,*args,**kwargs):
        super().__init__(*args)

class ItemExceptions(BusinessExceptions):
    """Exceptions arising from Items class"""

    def __init__(self,*args,**kwargs):
        super().__init__(*args)

class DiscountsExceptions(BusinessExceptions):
    """Exceptions arising from Discounts class"""

    def __init__(self,*args,**kwargs):
        super().__init__(*args)
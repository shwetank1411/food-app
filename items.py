from exceptions import ItemExceptions

class Items:

    def __init__(self,item_name,item_count,item_price):
        self.item_name = item_name
        self.item_count = item_count
        self.item_price = item_price
        print(f"Item Created --> {self.item_name}")

    @property
    def item_count(self):
        return self._item_count

    @item_count.setter
    def item_count(self,value):
        if not isinstance(value,int) or value <=0 :
            raise ItemExceptions(f"Invalid Item count -- {value} : should be a positive whole number")
        self._item_count = value

    @property
    def item_price(self):
        return self._item_price

    @item_price.setter
    def item_price(self, value):
        if not isinstance(value,int) or value <= 0:
            raise ItemExceptions(f"Invalid Item price -- {value} : should be a positive whole number")
        self._item_price = value
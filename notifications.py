from enum import Enum ,auto

class Restaurants(Enum):

    LaBellaPizza = auto()
    ChinChow = auto()
    Swadishtam = auto()
    BakeHouse = auto()
    ChaiWaala = auto()

class Notifications:

    @staticmethod
    def notify_restaurant(restaurant :Restaurants) -> None:
        print(f'App Order details sent to {restaurant.name}')
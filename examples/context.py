from dreampolitik.resource import ResourceCollection
from enum import Enum, auto, unique

@unique
class Resources(Enum):
    time = auto()
    money = auto()

@unique
class Actions(Enum):
    paying_rent = auto()
    paying_staff = auto()
    resting = auto()
    working = auto()

def money(amount):
    resDict = {Resources.money: amount}
    return ResourceCollection(resDict)

def time(amount):
    resDict = {Resources.time: amount}
    return ResourceCollection(resDict)

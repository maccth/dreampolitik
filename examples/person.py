from dreampolitik.element import Element
from examples.context import Resources, Actions, money, time

import logging

class Person(Element):

    def __init__(self, job, landlord, external=None):
        super(Person, self).__init__()
        self.job = job
        self.landlord = landlord
        self.external = external

    def on_tick(self):
        self.every(30, self.pay_rent)
        self.go_to_work()
        self.rest()

    def pay_rent(self):
        self.transfer(money(100), self.landlord, Actions.paying_rent)

    def go_to_work(self):
        self.transfer(time(8), self.job, Actions.working)

    def rest(self):
        self.transfer(time(12), self.external, Actions.resting)

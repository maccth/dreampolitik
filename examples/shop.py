from dreampolitik.element import Element
from examples.context import Actions, Resources, money
from collections import defaultdict

class Shop(Element):

    def __init__(self, external=None):
        super(Shop, self).__init__()
        self.staff_hours = defaultdict(lambda: 0.0)

    def on_tick(self):
        self.run_shop()
        self.every(7, self.pay_staff)

    def pre_on_tick(self, ingress):
        # Process working actions, keeping track of who worked
        if Actions.working in ingress:
            staff_transfers = ingress[Actions.working]
            for staff_member, res in staff_transfers.items():
                # For now, only deal with the expected Time resource
                # Don't check other resources
                hours = res[Resources.time]
                self.staff_hours[staff_member] += hours
            ingress.pop(Actions.working)
        # Process all other actions
        super(Shop, self).pre_on_tick(ingress)

    def run_shop(self):
        # Arbitrary, to keep the shop running for now with no actual customers
        # And they said there was no such thing as a free lunch...
        self._resources += money(100)

    def pay_staff(self):
        for staff_member in self.staff_hours:
            hours = self.staff_hours[staff_member]
            self.staff_hours[staff_member] = 0
            self.transfer(money(hours*2), staff_member, Actions.paying_staff)

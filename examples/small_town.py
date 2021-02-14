from examples.context import Resources, time
from examples.person import Person
from examples.shop import Shop
from examples.simulation import Simulation

import logging

class SmallTown(Simulation):

    def __init__(self):
        super(SmallTown, self).__init__()
        logging.getLogger().setLevel(logging.INFO)
        shop = Shop()
        # TODO: in future, Person/Shop should have register_work/staff memeber
        # functions instead of having to pass these things into the __init__
        person = Person(shop.get_id(), None)
        self.register_elements([person, shop])
        self.register_tick_packet(time(24))
        self.register_intra_tick_resources([Resources.time])


print("in small_town")
sim = SmallTown()
sim.run(1)

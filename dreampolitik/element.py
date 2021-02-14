import logging
import pprint
import textwrap
from collections import defaultdict

from .exception import InsufficientResourceError
from .resource import ResourceCollection


class Element(object):
    def __init__(self):
        self._id = id(self)
        self._tick_count = 0
        self._resources = ResourceCollection()
        self._intra_tick_resources = []
        self._init_elem_egress()

    def _init_elem_egress(self):
        # egress maps: to -> action -> from -> ResourceCollection
        # this makes it easier to convert egress to ingress
        frms_to_res = lambda : defaultdict(ResourceCollection)
        actions_to_frms = lambda : defaultdict(frms_to_res)
        to_to_actions = defaultdict(actions_to_frms)
        self._egress = to_to_actions

    def transfer(self, resources, to, action):
        if self._resources >= resources:
            self._resources -= resources
            self._egress[to][action][self.get_id()] += resources
        else:
            raise InsufficientResourceError(
                self._id, to, self._resources, resources, action)
            
    def pre_on_tick(self, ingress):
        # ingress maps: action -> from -> ResourceCollection
        # TODO: Move the tick_count increment to the class that wraps all
        #       elements at the simulation level
        self._tick_count += 1
        for action in ingress:
            for frm in ingress[action]:
                res = ingress[action][frm]
                self._resources += res
                msg_1 = f"[{type(self)}.{self._id}] <=={action}== [.{frm}]"
                msg_2 = textwrap.indent(pprint.pformat(res), '\t')
                msg = f" t = {self._tick_count} | " + msg_1 + '\n' + msg_2
                logging.info(msg)

    def post_on_tick(self):
        # if intra tick resources
        self._zero_intra_tick_resources()
        egress = self._egress
        self._init_elem_egress()
        return egress

    # For now, keeping this here since it makes it easier to parallelise
    # execution of the tick.
    # However, if the tick resource is sent with the tick, then that would be
    # controlled centrally or by some routing engine(s).
    # The following two things should be done in the same place
    #   1) the tick resource and it's amount are specified, and
    #   2) the tick resource is zeroed
    # and that place probably should not be here
    # One solution is to wrap Elements at the Simulation level
    def set_intra_tick_resources(self, resources):
        self._intra_tick_resources = resources

    def _zero_intra_tick_resources(self):
        for resource in self._intra_tick_resources:
            if resource in self._resources:
                self._resources.pop(resource)

    def get_id(self):
        return self._id

    def every(self, tick_period, fn):
        ''' Execute fn if the tick count is a multiple of tickPeriod '''
        if self._tick_count % tick_period == 0:
            fn()

    def on_cycle(self, on_ticks, tick_preiod, fn):
        tick = self._tick_count % tick_preiod
        execute = False
        if isinstance(on_ticks, int):
            execute = on_ticks == tick
        elif tick in on_ticks:
            execute = True
        if execute:
            fn()
        



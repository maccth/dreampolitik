from collections import defaultdict
from enum import Enum
import logging
import pprint
import textwrap

from .resource import ResourceCollection


class Simulation(object):

    def __init__(self):
        self._tick_count = 0

    def register_elements(self, elements):
        self._elements = elements

    def register_tick_packet(self, packet):
        self._tick_packet = packet

    def register_intra_tick_resources(self, resources):
        self._intra_tick_resources = resources
        for e in self._elements:
            e.set_intra_tick_resources(resources)

    def run(self, ticks):
        self._init_sim_ingress()
        self._init_sim_egress()
        for _ in range(ticks):
            self._tick_count += 1
            self._run_tick()

    def _run_tick(self):
        if None in self._ingress:
            sink_igress = self._ingress.pop(None)
            # sink_igress = textwrap.indent(pprint.pformat(sink_igress), '\t')
            # msg = f" t = {self._tick_count} | sink igress " + '\n' + sink_igress
            # logging.info(msg)
        for element in self._elements:
            # get ingress for given element
            if element.get_id() in self._ingress:
                ingress = self._ingress.pop(element.get_id())
            else:
                ingress = self._cons_element_ingress()
            # add tick packet
            ingress[FundamentalActions.tick][None] += self._tick_packet
            # execute tick
            element.pre_on_tick(ingress)
            element.on_tick()
            egress = element.post_on_tick()
            # save egress for next tick's ingress
            self._add_egress(egress)
        self._ingress = self._egress
        self._init_sim_egress()

    def _add_egress(self, egress):
        # TODO: rewrite this so the egress can be accumulated
        for to in egress:
            for action in egress[to]:
                for frm in egress[to][action]:
                    res = egress[to][action][frm]
                    self._egress[to][action][frm] += res

    def _cons_element_ingress(self):
        # element ingress maps: action -> from -> ResourceCollection
        frms_to_res = lambda : defaultdict(ResourceCollection)
        actions_to_frms = defaultdict(frms_to_res)
        return actions_to_frms

    def _init_sim_ingress(self):
        # element ingress maps:   action -> from -> ResourceCollection
        # sim ingress maps: to -> action -> from -> ResourceCollection
        elem_ingress = self._cons_element_ingress
        to_to_elem_ingress = defaultdict(elem_ingress)
        self._ingress = to_to_elem_ingress

    def _init_sim_egress(self):
        # element egress maps:   action -> from -> ResourceCollection
        # sim egress maps: to -> action -> from -> ResourceCollection
        elem_egress = self._cons_element_ingress
        to_to_elem_egress = defaultdict(elem_egress)
        self._egress = to_to_elem_egress

class FundamentalActions(Enum):
    tick = 'fundamental_tick'




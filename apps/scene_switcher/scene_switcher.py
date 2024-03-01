import hassapi as hass
import time
import json
from datetime import timedelta
from pprint import pprint
from datetime import datetime


class SceneSwitcher(hass.Hass):

    def initialize(self):

        self.log(f"{self.__class__.__name__} Starting")
        self.handlers = {}
        self.SwitchSensor = self.args["SwitchSensor"]
        self.SwitchCommands = self.args["SwitchCommands"]

        self.listen_state(self.switch_scene, self.SwitchSensor)

    def switch_scene(self, entity, attribute, old, new, kwargs):
        print(new,entity)
        if entity is not None:
            ent_to_switch = self.SwitchCommands.get(new)
            if ent_to_switch is not None:
                self.toggle(ent_to_switch)
                self.log(f"Toggling {ent_to_switch}")

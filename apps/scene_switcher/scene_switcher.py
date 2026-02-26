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
        print(self.SwitchCommands)
        print(self.SwitchCommands.get("1_hold"))
    def switch_scene(self, entity, attribute, old, new, kwargs):
        # print(new,entity)
        if entity is not None:
            commands = self.SwitchCommands.get(new)
            # print(commands)
            if commands is not None:
                # print(commands)
                for command,switch in commands.items():
                    if command == "Toggle":
                        for action in switch:
                            self.toggle(action)
                            self.log(f"Toggling {action}")
                    if command == "SwitchOn":
                        # print(switch)
                        for action in switch:
                            self.turn_on(action)
                            self.log(f"Switching on {action}")
                    if command == "SwitchOff":
                        for action in switch:
                            self.turn_off(action)
                            self.log(f"Switching off {action}")

            # if ent_to_switch is not None:
            #     self.toggle(ent_to_switch)

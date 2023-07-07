import hassapi as hass
import time
import json
from pprint import pprint
from datetime import datetime

class AutoLightOff(hass.Hass):

    def initialize(self):
        self.log(f"{self.__class__.__name__} Starting")
        self.handlers = {}
        self.state_all = self.get_state()
        self.listen_state(self.byrna, "switch")
        self.listen_state(self.byrna, "light")
        args = self.args
        print (self.args)

    def auto_byrna_off(self, args):
        self.log(f"runned in delay  ---{args['ent']}")
        if args['ent'] != "switch.alles":
            self.log("turning off---- ", args['ent'])
            self.turn_off(args['ent'])
            self.handlers.pop(args['ent'])

    def byrna(self, entity, attribute, old, new, kwargs):

        if not isinstance(self.get_state(entity, attribute="entity_id"), str):
            self.log(f"Returning {entity}")
            return

        try:
            automation_active = self.get_state('input_boolean.szalter')
            print (automation_active) 
            friendly_name_of_entity = self.get_state(
                entity, attribute="friendly_name")

            timerek_global_state = self.get_entity(
                'input_number.timerek').get_state()

            timerek_ent_state = [x for x, y in self.get_state().items() if
                                 y['attributes']['friendly_name'] == f'timerek_{friendly_name_of_entity}']

            timerek_state = self.get_state(timerek_ent_state[0]) if len(
                timerek_ent_state) == 1 else timerek_global_state

            off_time = int(timerek_state.split('.')[0]) * 60

        except Exception as e:
            self.log(f"An Exception occurred during turn of a lamp:"
                     f"{e}")

        if new == "on":
            if automation_active == "on":
                try:
                    handler = self.run_in(self.auto_byrna_off, off_time, ent=entity)
                    self.handlers.update({entity: handler})
                    self.log(f"Adding to auto off schedule light {friendly_name_of_entity} in {off_time} Minutes")
                except Exception as e:
                    self.log(f"An Exception occurred during turn of a lamp:"
                             f"{e}")
            else:
                self.log("Auto OFF is OFF!")

        if new == "off":
            if self.handlers.get(entity):
                try:
                    self.cancel_timer(self.handlers[entity])
                    self.handlers.pop(entity)
                    self.log(f"Manual light off occurred, removing {entity} from off schedule")
                except Exception as e:
                    self.log(e)
            self.log("Turned OFF", entity)

    def terminate(self):
        self.log("Terminating")





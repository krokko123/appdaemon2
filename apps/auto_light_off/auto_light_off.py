import hassapi as hass
import time
import json
from pprint import pprint
from datetime import datetime
from appdaemon.plugins.mqtt.mqttapi import Mqtt as mqtt
class AutoLightOff(hass.Hass):

    def initialize(self):
        self.log(f"{self.__class__.__name__} Starting")
        self.handlers = {}
        self.state_all = self.get_state()
        mqtt.mqtt_publish(self, topic="homeassistant/ktktkt",payload="KUUUUPAAA22222222")
        # self.listen_state(self.byrna, "switch")
        # self.listen_state(self.byrna, "light")
        self.NightModeValue = self.args["NightModeValue"]
        self.DayPeriodSensor = self.args["DayPeriodSensor"]
        self.Watched_devices = self.args["Watched_devices"]
        self.Excluded_night_devices = self.args["Excluded_night_devices"]
        self.AppDetails = self.args["AppDetails"]

        for ent in self.Watched_devices:
            self.listen_state(self.byrna, ent)
            self.log(f"Adding {ent} to watch.")

        args = self.args
        # print (self.args)
        states = self.get_state("switch")
        
        for ent in states.values():
            friendly_name_of_entity = ent.get("attributes").get("friendly_name")
#            friendly_name_of_entity = "ent"
            ent_id = ent['entity_id']#.replace(".","xx")
            ent_data = {"command_topic": f"{ent_id}",
                        "state_topic": f"{ent_id}/set",
                        "mode": "box",
                        "unique_id": f"kurwa_{ent_id}_idd",
                        "name": f"{friendly_name_of_entity}",
                        "friendly_name":"2137"
                        }

            post_data = {}
            post_data.update({"dev":self.AppDetails})
            post_data.update(ent_data)
            print (json.dumps(post_data,indent=4))
            tt = f"homeassistant/switch/{ent['entity_id']}/config".replace(".","")
            print (tt)
            mqtt.mqtt_publish(self, topic=tt, payload=json.dumps(post_data))

            ent_data = {"command_topic": f"{ent_id}",
                        "state_topic": f"{ent_id}/set",
                        "availability_topic": f"{ent_id}/av",
                        "unique_id": f"kurfrrwa_{ent_id}_idd",
                        "name": f"{friendly_name_of_entity}",
                        # "friendly_name": "2137"
                        }
            post_data = {}
            post_data.update({"dev":self.AppDetails})
            post_data.update(ent_data)
            print (json.dumps(post_data,indent=4))
            tt = f"homeassistant/number/kupa/{ent['entity_id']}/config".replace(".","xx")
            print (tt.format(typee="wefwwfew"))
            mqtt.mqtt_publish(self, topic=tt, payload=json.dumps(post_data))

            ent_data = {"command_topic": f"{ent_id}",
                        "state_topic": f"{ent_id}/set",
                        "availability_topic": f"{ent_id}/av",
                        "unique_id": f"kurfrrwa_{ent_id}_idd",
                        "name": f"{friendly_name_of_entity}",
                        # "friendly_name": "2137"
                        }
            post_data = {}
            post_data.update({"dev":self.AppDetails})
            post_data.update(ent_data)
            print (json.dumps(post_data,indent=4))
            tt = f"homeassistant/sensor/Eeee{ent['entity_id']}".replace(".","xx")
            print (tt.format(typee="wefwwfew"))
            mqtt.mqtt_publish(self, topic=f"{tt}/config", payload=json.dumps(post_data))

            ent_data = {"command_topic": f"{tt}/cmnd",
                        "state_topic": f"{tt}/set",
                        "availability_topic": f"{tt}/av",
                        "unique_id": f"kurfrrwa_{ent_id}_idd",
                        "name": f"{friendly_name_of_entity}",
                        # "friendly_name": "2137"
                        }
            post_data = {}
            post_data.update({"dev":self.AppDetails})
            post_data.update(ent_data)
            print (json.dumps(post_data,indent=4))
            tt = f"homeassistant/button/Eeee{ent['entity_id']}/config".replace(".","xx")
            print (tt.format(typee="wefwwfew"))
            mqtt.mqtt_publish(self, topic=tt, payload=json.dumps(post_data))

    def auto_byrna_off(self, args):
        self.log(f"runned in delay  ---{args['ent']}")
        if args['ent'] != "switch.alles":
            self.log("turning off---- ", args['ent'])
            self.turn_off(args['ent'])
            self.handlers.pop(args['ent'])

    def byrna(self, entity, attribute, old, new, kwargs):
        print(type(entity in self.Excluded_night_devices))
        print(self.Excluded_night_devices)
        print(self.get_state(self.DayPeriodSensor), self.NightModeValue, self.get_state(self.DayPeriodSensor) == self.NightModeValue)
        if (self.get_state(self.DayPeriodSensor) == self.NightModeValue) \
                and entity in self.Excluded_night_devices:
            self.log("Device is excluded from night auto off in this script!")
            return
        if not isinstance(self.get_state(entity, attribute="entity_id"), str):
            self.log(f"Returning {entity}")
            return

        try:
            automation_active = self.get_state('input_boolean.szalter')
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





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
        self.Buttons = {}
        self.Sensors = {}
        self.Numbers = {}
        self.Switches = {}
        for ent in self.Watched_devices:
            self.listen_state(self.byrna, ent)
            self.log(f"Adding {ent} to watch.")

        args = self.args
        # print (self.args)
        
        for ent in self.Watched_devices:
            states = self.get_entity(ent).get_state(attribute="all")
            friendly_name_of_entity = states.get("attributes").get("friendly_name")
#            friendly_name_of_entity = "ent"
            ent_id = states.get("entity_id")#.replace(".","xx")
            ent_data = {"command_topic": f"{ent_id}",
                        "state_topic": f"{ent_id}/set",
                        "mode": "box",
                        "unique_id": f"{ent_id}",
                        "name": f"{friendly_name_of_entity}",
                        "friendly_name":"2137"
                        }

            post_data = {}
            post_data.update({"dev":self.AppDetails})
            post_data.update(ent_data)
            print (json.dumps(post_data,indent=4))
            tt = f"homeassistant/switch/{ent_id}/config".replace(".","")
            self.Switches.update({ent_id:ent_data})
            print (tt)
            mqtt.mqtt_publish(self, topic=tt, payload=json.dumps(post_data))

            tt = f"homeassistant/number/kupa/{ent_id}/config".replace(".","xx")
            ent_data = {"command_topic": f"{tt}",
                        "state_topic": f"{tt}/set",
                        "availability_topic": f"{tt}/av",
                        "unique_id": f"{tt}",
                        "name": f"{friendly_name_of_entity}",
                        "mode":"box"
                        # "friendly_name": "2137"
                        }
            post_data = {}
            post_data.update({"dev":self.AppDetails})
            post_data.update(ent_data)
            print (json.dumps(post_data,indent=4))
            self.Numbers.update({ent_id:ent_data})
            print (tt.format(typee="wefwwfew"))
            mqtt.mqtt_publish(self, topic=tt, payload=json.dumps(post_data))
            mqtt.mqtt_publish(self, topic=ent_data.get("availability_topic"), payload="online")
            mqtt.mqtt_publish(self, topic=ent_data.get("state_topic"), payload=43)

            ent_data = {"command_topic": f"{ent_id}",
                        "state_topic": f"{ent_id}/set",
                        "availability_topic": f"{ent_id}/av",
                        "unique_id": f"dfvfdv{ent_id}",
                        "name":f"{friendly_name_of_entity}"
                        # "friendly_name": "2137"
                        }
            post_data = {}
            post_data.update({"dev":self.AppDetails})
            post_data.update(ent_data)
            print (json.dumps(post_data,indent=4))
            tt = f"homeassistant/sensor/fvfvf{ent_id}".replace(".","xx")
            self.Sensors.update({ent_id:ent_data})
            print (tt.format(typee="wefwwfew"))
            mqtt.mqtt_publish(self, topic=f"{tt}/config", payload=json.dumps(post_data))
            mqtt.mqtt_publish(self, topic=ent_data.get("availability_topic"), payload="online")

            ent_data = {"command_topic": f"{tt}/cmnd",
                        "state_topic": f"{tt}/set",
                        "availability_topic": f"{tt}/av",
                        "unique_id": f"{ent_id}",
                        "name": f"{friendly_name_of_entity}"
                        # "friendly_name": "2137"
                        }
            post_data = {}
            post_data.update({"dev":self.AppDetails})
            post_data.update(ent_data)
            print (json.dumps(post_data,indent=4))
            tt = f"homeassistant/button/{ent_id}/config".replace(".","xx")
            self.Buttons.update({ent_id: ent_data})
            print (tt.format(typee="wefwwfew"))
            mqtt.mqtt_publish(self, topic=tt, payload=json.dumps(post_data))
            mqtt.mqtt_publish(self, topic=ent_data.get("availability_topic"), payload="online")

            print(ent_data.get("availability_topic"))
        # for button in self.Buttons.values():
        #     print(button.get("availability_topic"))
        #     mqtt.mqtt_publish(self, topic=button.get("availability_topic"), payload="online")
        #
        # for number in self.Numbers.values():
        #
        #     mqtt.mqtt_publish(self, topic=number.get("availability_topic"), payload="online")
        # print(json.dumps(self.Sensors,indent=4))
        # print(json.dumps(self.Buttons,indent=4))
        # print(json.dumps(self.Numbers,indent=4))
        # print(json.dumps(self.Switches,indent=4))

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
                    mqtt.mqtt_publish(self,topic=self.Sensors.get(entity).get("availability_topic"),payload="online")
                    timer, interval, kwargs = self.info_timer(self.handlers.get(entity))
                    mqtt.mqtt_publish(self,self.Sensors.get(entity).get("state_topic"),payload=timer.strftime("%H:%M:%S"))
                    self.log(f"Adding to auto off schedule light {friendly_name_of_entity} in {off_time} Minutes")
                except Exception as e:
                    self.log(f"An Exception occurred during turn of a lamp:"
                             f"{e}")
            else:
                self.log("Auto OFF is OFF!")

        if new == "off":
            if self.handlers.get(entity):
                try:
                    self.log("kurwirjaeirui")
                    self.cancel_timer(self.handlers[entity])
                    self.handlers.pop(entity)
                    mqtt.mqtt_publish(self,self.Sensors.get(entity).get("state_topic"),payload="None")
                    self.log(f"Manual light off occurred, removing {entity} from off schedule")
                except Exception as e:
                    self.log(f"Exception occured: {e}")
            # self.log("Turned OFF", entity)

    def terminate(self):
        self.log("Terminating")





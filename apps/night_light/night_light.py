import hassapi as hass
import time
import json
import functools
from os.path import isfile, relpath, realpath, abspath, dirname
from pprint import pprint
from datetime import datetime


def byrna_operation_decorator(*f):
    def wrapper1(func, **kwargs):
        print(f"wrapper1 {func}  {kwargs} {f}")

        def wrapper2(*args, **kwargs):
            print(f"wrapper2 {args}  {kwargs} {f}")

            obj_vars = args[0]
            entity_name = vars(obj_vars)[f[0]][0]
            is_string = isinstance(entity_name,str)

            iterated_object = vars(obj_vars)[f[0]]
            print(iterated_object)
            for obj in iterated_object:
                try:
                    bulb_entity = obj if is_string else list(obj.keys())[0]
                    bulb_values = list(obj.values())[0] if not is_string else None
                    print(f"wrapper2 {bulb_entity}")
                    func(obj_vars, entity_name=bulb_entity, entity_values=bulb_values)

                except Exception as e:
                    obj_vars.log(f"Exception {e}", level ="ERROR")

        return wrapper2
    return wrapper1


class NightLight(hass.Hass):

    def initialize(self):
        state = self.get_state()
        self.log(f'{__class__.__name__} started')
        # self.Nightlights = self.args["NightLights"]
        self.state = self.get_state()
        self.NightBulbsOffTime = self.args["NightBulbsOffTime"]
        self.OverrideOffTime = self.args["OverrideOffTime"]
        self.DayPeriodSensor = self.args["DayPeriodSensor"]
        self.CheckNightTimePeriodTime = self.args["CheckNightTimePeriodTime"]
        self.NightModeValue = self.args["NightModeValue"]
        self.NightLightSwitches = self.args["NightLightSwitches"]
        self.NightLightBulbs = self.args["NightLightBulbs"]
        self.OffEventsFile = self.args["OffEventsFile"]
        self.PirSensor= self.args["PirSensor"]
        self.turn_off_ovveride()
        self.run_every(self.check_night_mode, "now", self.CheckNightTimePeriodTime)
        # self.create_helpers()
        self.listen_state(self.pir, self.PirSensor)

        for switch in self.NightLightSwitches:
            self.listen_state(self.switch_listener, switch)

    def create_helpers(self):
        for switch in self.NightLightSwitches:
            sw_name = switch.replace(".", "_")
            self.set_state(f"timer.{sw_name}",friendly_name=f"timer__{sw_name}",state="idle")
            self.set_state(f"input_boolean.{sw_name}",state="off", friendly_name=f"bolean_helper_{sw_name}")
        for bulb in self.NightLightSwitches:
            print(bulb)

    def pir(self, entity, attribute, old, new, kwargs):

        self.log("PIR accident !!!")
        override_state = self.get_state("input_boolean.pir_override")
        if (override_state == "on") | (self.NightModeValue != self.get_state(self.DayPeriodSensor)):
            self.log("PIR is overrided, returning")
            return
        self.log(f'{old}  {new}')
        if new == "on":
            # if self.get_state("timer.pir_override") == "active":
            #     self.turn_on("input_boolean.pir_override")
            #     return
            self.night_bulbs_on()
            self.run_in(self.night_bulbs_off, self.NightBulbsOffTime)

    def switch_listener(self, entity, attribute, old, new, kwargs):
        if self.NightModeValue != self.get_state(self.DayPeriodSensor):
            self.log("Switch Listener Now is not a night")
            return
        if new == "on":
            timer_state = self.get_state("timer.pir_override")

            if timer_state == "active":
                self.turn_on("input_boolean.pir_override")
                self.run_in(self.turn_off_ovveride, self.OverrideOffTime)
                self.log(f"Overridding pir for {self.OverrideOffTime} seconds")
        if new == "off":
            self.get_entity("timer.pir_override").call_service("start")

    def check_night_mode(self, bleble):

        override_state = self.get_state("input_boolean.pir_override")
        if override_state == "on":
            self.log("PIR is overrided, returning")
            return

        if self.NightModeValue != self.get_state(self.DayPeriodSensor):
            self.log(f"{bleble}We do not Have A Nnight ! returning")
            self.stop_night_mode()
            return

        self.log(f"A NIGHT !!! {self.NightModeValue} {self.DayPeriodSensor}")
        self.night_switches_on()

    @byrna_operation_decorator("NightLightBulbs")
    def night_bulbs_off(self, *args,  **kwargs):
        entity_name = kwargs["entity_name"]
        entity_values = kwargs["entity_values"]
        self.turn_off(entity_name)
        self.log(f"turning off the bulb {entity_name}")

    @byrna_operation_decorator("NightLightBulbs")
    def night_bulbs_on(self, *args,  **kwargs):
        entity_name = kwargs["entity_name"]
        entity_values = kwargs["entity_values"]
        self.turn_on(entity_name,
                     brightness=entity_values['brightness'],
                     rgb_color=entity_values['rgb_color'])
        self.log(f"turning off the bulb {entity_name}")

    @byrna_operation_decorator("NightLightSwitches")
    def night_switches_on(self, *args, **kwargs):
        entity_name = kwargs["entity_name"]
        ent_state = self.get_state(entity_name)
        if ent_state == "on":
            self.night_bulbs_off()
            self.log("Night Switch is on... Turning off the bulbs")
        if ent_state == "off":
            self.turn_on(entity_name)
            self.log("Night Switch is off... Turning on them")
            self.run_in(self.night_bulbs_off, 30)
                    # print(f"{args}   {kwargs}")

    @byrna_operation_decorator("NightLightSwitches")
    def night_switches_off(self, *args, **kwargs):
        entity_name = kwargs["entity_name"]
        self.turn_off(entity_name)
        self.log("Night Switch off")

    def turn_off_ovveride(self,*args, **kwargs):
        self.turn_off("input_boolean.pir_override")
        self.log("Turning off override", level="ERROR")

    def stop_night_mode(self):
        dir_name = dirname(__file__)
        filename = f"{dir_name}/{self.OffEventsFile}"
        today_date = datetime.now().strftime("%Y-%m-%d")

        if isfile(filename):
            with open(filename,'r') as read_file:
                json_data_read = json.loads(read_file.read())
        else:
            json_data_read = []

        if today_date in json_data_read:
            self.log("Night mode stopped already today.... returning.")
            return

        self.log("stopping night mode")
        self.night_switches_off
        data_to_dump = today_date
        json_data_read.append(data_to_dump)
        json_data_write = json.dumps(json_data_read,indent=4)

        with open(filename, "w") as write_file:
            write_file.write(json_data_write)
            write_file.close()

    def terminate(self):
        self.log("Terminating")
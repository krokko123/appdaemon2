import hassapi as hass
import time
import json
from pprint import pprint
from datetime import datetime
#
# Hello World App
#
# Args:
#


class HelloWorld(hass.Hass):
    def initialize(self):
        #state = self.get_state('input_select.ththth')
        #print(state)
        self.listen_event(self.mode_event, "*")
        #self.turned_on = {}
        self.handlers = {}
        self.friendly_names = dict()
        self.listen_state(self.byrna, "switch")
        self.listen_state(self.byrna, "light")
        self.listen_state(self.pir, "binary_sensor")
        self.listen_state(self.pir, "input_boolean")
        self.listen_state(self.pir, "input_number")
        # print(json.dumps(self.get_state()))
#        self.listen_state(state_callback)
        self.log("Hello from AppDaemon")
        self.log("You are now ready to run Apps!")
        self.log("czesc kurwa")
        # print  (json.dumps(self.get_entity('sensor.time_of_day').get_state(attribute="entity_id")))
        #print(self.get_state("switch.wlacznik_sypialnia_right"))
        #print(self.get_state("switch.wlacznik_sypialnia_left"))
        state_all = self.get_state()
        #


        print([x for x,y in state_all.items() if y['attributes']['friendly_name'] =='Pushy' ][0])
        for ent,attributes in state_all.items():
            friendly_name = attributes.get('attributes').get('friendly_name')
            self.friendly_names.update({ent:friendly_name})
#        self.toggle("switch.wlacznik_sypialnia_right")
#        self.toggle("switch.wlacznik_sypialnia_left")
#         print(json.dumps(self.sta,indent=4))
#         print(list(self.friendly_names
#                    .keys())
#                    [list(self
#                    .friendly_names
#                    .values())
#                    .index('Łazienka')])
#         # time.sleep(1)
#         print(self.get_state("switch.wlacznik_sypialnia_right"))
#         print(self.get_state("switch.wlacznik_sypialnia_left"))
        self.run_every(self.every_c, "now", 5)
#        print(self.get_state("light"))


#        for i in self.get_state("switch"):
#            self.toggle(i)
#            print(i)

        
    def every_c(self, args):
        self.log("run_every")
        self.fire_event("MODE_CHANGE", dupa="kupia", kurwa="mac")
        print(self.handlers)
#        for entity in self.handlers.values():
#            print (self.info_timer(entity))

    def run_in_c(self,args):
        self.log(f"runned in delay  ---{args['ent']}")
        print(args)
        if args['ent'] != "switch.alles":
            self.log("turning off---- ",  args['ent'])
            self.turn_off(args['ent'])
            self.handlers.pop(args['ent'])
#            duration = datetime.now() - self.turned_on.get(args['ent']) 
#            print (duration.total_seconds())
#            if 10  > duration.total_seconds() > 9:
#                print("HAMPF")
#            else:
#                print("NIE HAMPF")

    def byrna(self, entity, attribute, old, new, kwargs):
        self.log(entity, attribute, old, new, kwargs)
#        print (json.dumps(self.turned_on,indent=4, default=json_serial))
        friendly_name =self.get_state(entity,attribute=('friendly_name'))

        if new == "on":
            automation_active = self.get_state('input_boolean.szalter')
            friendly_name_of_entity = self.get_state(entity,attribute="friendly_name")
            timerek_global_state  = self.get_entity('input_number.timerek').get_state()
            timerek_ent_state =[x for x,y in self.get_state().items() if y['attributes']['friendly_name'] == f'timerek_{friendly_name_of_entity}']
            timerek_state = self.get_state(timerek_ent_state[0]) if len(timerek_ent_state) == 1 else timerek_global_state
            friendly_name_v = list(self.friendly_names.values())
            print ("KUUUUPAAAA")
            off_time = int(timerek_state.split('.')[0]) * 60
#            print(self.get_state(entity,attribute=('friendly_name')))
            #self.turned_on.update({entity:datetime.now()})

            if automation_active == "on":
                handler = self.run_in(self.run_in_c,off_time,ent=entity)
                self.handlers.update({entity:handler})
            else:
                self.log("Auto OFF is OFF!")
#

#        lazienka_state = self.get_state("light.obk12c40761")
#        self.log("lazienka_light_state", lazienka_state)
#        self.log("lazienka_state", entity, old, new)
#        if entity == "switch.wlacznik_duzy_left":
#            if lazienka_state == "off":
#                self.turn_on("switch.wlacznik_duzy_left")
        if new == "off":
            if self.handlers.get(entity):
                try:
                    self.cancel_timer(self.handlers[entity])
                    self.handlers.pop(entity)
                except Exception as e:
                    self.log(e)
            self.log("Turned OFF", entity)

    def pir(self, entity, attribute, old, new, kwargs):
        self.log(str(entity),"\n", 
                str(attribute),"\n", 
                str(old),"\n", 
                str(new),"\n")
        print(self.get_entity('input_boolean.szalter').get_state())
        print(self.get_entity('input_number.timerek').get_state())
#        if new == "on":
#            self.toggle("switch.wlacznik_sypialnia_left")
#        if new == "off":
#            self.toggle("switch.wlacznik_sypialnia_right")

    def mode_event(self, event_name, data, kwargs):
        print( event_name)#, data, kwargs)
            

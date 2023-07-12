import hassapi as hass
import time
import json
from pprint import pprint
from datetime import datetime

class DayPeriod(hass.Hass):

    def initialize(self):
        self.log(f"{self.__class__.__name__} Starting")
        self.handlers = {}
        self.DayPeriods = self.args["DayPeriods"]
        self.run_every(self.day_period ,"now", 1)
        args = self.args
        print (self.DayPeriods)

    def day_period(self,e):
        print(datetime.now())
        print (self.DayPeriods)




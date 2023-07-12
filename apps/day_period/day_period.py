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

        args = self.args
        print (self.DayPeriods)


        self.log("Terminating")





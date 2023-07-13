import hassapi as hass
import time
import json
from datetime import timedelta
from pprint import pprint
from datetime import datetime


class DayPeriod(hass.Hass):

    def initialize(self):
        self.log(f"{self.__class__.__name__} Starting")
        self.handlers = {}
        self.DayPeriods = self.args["DayPeriods"]
        self.DayPeriodSensor = self.args["DayPeriodSensor"]
        self.run_every(self.day_period, "now", 60)
        args = self.args
        self.day_period()


    def init_dayperiods(self,now):
        self.DateTimes = [{"dayperiod": d,
                           "start": now.replace(hour=int(e['start'].split(":")[0]),
                                                           minute=int(e['start'].split(":")[1]),
                                                           second=0,
                                                           microsecond=0),
                           "end": now.replace(hour=int(e['end'].split(":")[0]),
                                                         minute=int(e['end'].split(":")[1]),
                                                         second=0,
                                                         microsecond=0)
                           } for d, e in self.DayPeriods.items()]

    def day_period(self, e=None):



        now = datetime.now()
        self.init_dayperiods(now)

        # print(now)
        for period in self.DateTimes:
            if (period['end'] - period['start']) < timedelta(days=0):
                pass
                if now > period['start']:
                    period['end'] += timedelta(days=1)
                else:
                    period['start'] -= timedelta(days=1)
            # print (period)

            if (period['start'] < now < period['end']):
                self.log(f"Setting dayperiod sensor {self.DayPeriodSensor} to {period['dayperiod']}")
                self.set_value(self.DayPeriodSensor,period['dayperiod'])
                # print(period['dayperiod'], now)
            # else:
            #     print (f"{period['start']} {now}    {period['end']}")

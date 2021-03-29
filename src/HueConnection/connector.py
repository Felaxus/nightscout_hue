import logging
import re
from datetime import datetime, timedelta, time
from typing import Optional

import pytz
import requests
import ujson
from dateutil.parser import parse
from twisted.internet import task, reactor

from .errors import *

requests.models.json = ujson

log = logging.getLogger(__name__)

ip_regex = re.compile(
    r'^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$', re.IGNORECASE)


class HueConnector:

    def __init__(self, *args, **kwargs):
        # Defining phillips IP
        phillips_ip = kwargs.get("phillips_ip") if ip_regex.fullmatch(kwargs.get("phillips_ip")) else None
        self.phillips_username = kwargs.get("phillips_user")
        if phillips_ip is None:
            raise InvalidData("Invalid IP")
        phillips_ip = phillips_ip + "/api/" if not phillips_ip.endswith("/") else phillips_ip + "api/"
        self.phillips_ip = phillips_ip + self.phillips_username + "/"

        # Defines other variables
        self.nightscout_url = kwargs.get("n_url")
        self.light_id = kwargs.get("light_id")
        self.high_color = kwargs.get("high_color")
        self.color_in_range = kwargs.get("color_in_range")
        self.low_color = kwargs.get("low_color")
        self.start_time = kwargs.get("start_time")
        self.end_time = kwargs.get("end_time")
        self.timezone_difference = kwargs.get("timezone")
        self.difference_color = kwargs.get("delay_color")
        self.nightscout_time_limit = kwargs.get("nightscout_difference")
        self.token = kwargs.pop("token", None)
        self.local_mode = bool(self.token)

        # Checks the types of variables
        try:
            self.high_glucose = int(kwargs.get("high_glucose"))
            self.brightness = int(kwargs.get("brightness"))
            self.refresh_rate = int(kwargs.get("refresh_rate"))
            self.low_glucose = int(kwargs.get("low_glucose"))

        except TypeError:
            raise InvalidData("Invalid data has been given")
        else:
            self.colors = {
                "RED": {
                    "hue": 10,
                    "sat": 240,
                    "bri": self.brightness,
                    "on": True},
                "ORANGE": {
                    "hue": 4500,
                    "sat": 250,
                    "bri": self.brightness,
                    "on": True},
                "GREEN": {
                    "hue": 27000,
                    "sat": 250,
                    "bri": self.brightness,
                    "on": True},
                "BLUE": {
                    "hue": 45000,
                    "sat": 250,
                    "bri": self.brightness,
                    "on": True},
                "PURPLE": {
                    "hue": 50000,
                    "sat": 250,
                    "bri": self.brightness,
                    "on": True}
            }

    def main(self):
        if not self.delayed:
            print(
                f"Nighstout delay with real life is too big. Changing colour to {self.get_color(self.glucose_level, True)}")
            self.change_color()
            return

        if not self.in_time_range:
            log.info("Time not in range")
            print("Not in range, turning off lights. Good night")
            # Turn off lights
            return

        print(
            f"Glucose {self.glucose_level} ({self.actual_glucose}) changing color to {self.get_color(self.glucose_level, True)}")
        self.change_color()

    def get_color(self, glucose_level, name: Optional[bool] = None):
        if glucose_level.upper().strip() == "HIGH":
            return ujson.dumps(self.colors[self.high_color]) if not name else self.high_color
        elif glucose_level.upper().strip() == "RANGE":
            return ujson.dumps(self.colors[self.color_in_range]) if not name else self.color_in_range
        elif glucose_level.upper().strip() == "DELAY":
            return ujson.dumps(self.colors[self.difference_color]) if not name else self.difference_color
        elif glucose_level.upper().strip() == "LOW":
            return ujson.dumps(self.colors[self.low_color]) if not name else self.low_color
        raise InternalIssue("Wrong glucose level idk")

    def change_color(self):
        for i in self.light_id.split(','):
            requests.put(f'http://{self.phillips_ip}lights/{i}/state', data=self.get_color(self.glucose_level))

    @property
    def nightscout_json(self):
        return requests.get(
            f"{self.nightscout_url + '/' if not self.nightscout_url.endswith('/') else self.nightscout_url}api/v1/entries.json",
            data={"count": 1},
        ).json()

    @property
    def time_checker(self):
        return TimeParser(self.nightscout_json[0]['dateString'], self.timezone_difference)

    @property
    def real_timezone(self):
        return self.time_checker.get_real_timezone()

    @property
    def delayed(self):
        return not self.time_checker.nightscout_in_range(self.real_timezone, int(self.nightscout_time_limit))

    @property
    def in_time_range(self):
        return self.time_checker.in_range(self.start_time, self.end_time, self.real_timezone)

    @property
    def glucose_level(self):
        glucose = self.nightscout_json[0]['sgv']
        if not self.delayed:
            return "DELAY"
        if glucose < self.low_glucose:
            return "LOW"
        if glucose > self.high_glucose:
            return "HIGH"
        return "RANGE"

    @property
    def actual_glucose(self):
        return self.nightscout_json[0]['sgv']

    def run(self):
        task.LoopingCall(self.main).start(self.refresh_rate)
        reactor.run()


class TimeParser:

    def __init__(self, nightscout_time, timezone_difference):
        nightscout_time = parse(nightscout_time)
        self.nightscout_time = timedelta(hours=nightscout_time.hour, minutes=nightscout_time.minute,
                                         seconds=nightscout_time.minute)

        self.timezone_difference = timezone_difference

    def nightscout_in_range(self, now: timedelta, difference: int) -> bool:
        diff = time(minute=difference)
        x = (now - self.nightscout_time)
        return x.seconds // 60 < diff.second // 60

    def get_real_timezone(self) -> timedelta:
        now = datetime.now(pytz.timezone("GMT"))
        gmt_now = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
        if self.timezone_difference == "0":
            return gmt_now
        difference = timedelta(hours=int(self.timezone_difference[1:]))

        if self.timezone_difference.startswith("+"):
            return gmt_now + difference
        return gmt_now - difference

    def in_range(self, start_time: str, end_time: str, now: timedelta) -> bool:
        start_time, end_time = [[int(x) for x in start_time.split(":")], [int(x) for x in end_time.split(":")]]

        start_time = timedelta(
            hours=int(start_time[0]), minutes=start_time[1] if start_time else 0
        )

        end_time = timedelta(
            hours=int(end_time[0]), minutes=end_time[1] if end_time else 0
        )

        return start_time < now < end_time

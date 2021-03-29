import logging
import re
from datetime import datetime, timedelta, time

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
        self.nightscout_url = kwargs.get("n_url")
        self.phillips_ip = ip_regex.fullmatch(kwargs.get("phillips_ip"))
        self.phillips_username = kwargs.get("phillips_user")
        self.light_id = kwargs.get("light_id")
        self.high_color = kwargs.get("high_color")
        self.color_in_range = kwargs.get("color_in_range")
        self.low_color = kwargs.get("low_color")
        self.start_time = kwargs.get("start_time")
        self.end_time = kwargs.get("end_time")
        self.timezone_difference = kwargs.get("timezone")
        self.nightscout_time_limit = kwargs.get("nightscout_difference")
        self.token = kwargs.pop("token", None)
        self.local_mode = bool(self.token)

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
                    "bri": self.brightness},
                "ORANGE": {
                    "hue": 4500,
                    "sat": 250,
                    "bri": self.brightness},
                "GREEN": {
                    "hue": 27000,
                    "sat": 250,
                    "bri": self.brightness},
                "BLUE": {
                    "hue": 45000,
                    "sat": 250,
                    "bri": self.brightness},
                "PURPLE": {
                    "hue": 50000,
                    "sat": 250,
                    "bri": self.brightness}
            }

    def main(self):
        if not self.time_checker.nightscout_in_range(self.real_timezone, int(self.nightscout_time_limit)):
            print("Time diff too big")
            return

        if not self.time_checker.in_range(self.start_time, self.end_time, self.real_timezone):
            log.info("Time not in range")
            print("Not in range, turning off lights. Good night")
            # Turn off lights
            return

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

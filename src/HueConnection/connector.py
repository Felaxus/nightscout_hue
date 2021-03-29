import logging
import re

import requests
import ujson
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
            self.low_glucose_value = int(kwargs.get("low_glucose"))

        except TypeError:
            raise InvalidData("Invalid data has been given")

    def main(self):
        print("Do something")

    def run(self):
        task.LoopingCall(self.main).start(self.refresh_rate)
        reactor.run()


class TimeParser:

    def __init__(self, nightscout_url: str, timezone_difference: str):
        self.glucose_json = requests.get(
            f"{nightscout_url + '/' if not nightscout_url.endswith('/') else nightscout_url}api/v1/entries.json",
            data={"count": 1}).json()


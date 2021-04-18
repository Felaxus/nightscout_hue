from os import environ as env

from durations import Duration

import HueConnection

conn = HueConnection.HueConnector(
    n_url=env.get("NIGHTSCOUT_URL"),
    phillips_ip=env.get("PHILLIPS_IP"),
    phillips_user=env.get("PHILLIPS_USERNAME"),
    light_id=env.get("LIGHT_ID"),
    refresh_rate=env.get("REFRESH_RATE"),
    brightness=env.get("BRIGHTNESS_LEVEL"),
    high_glucose=env.get("HIGH_GLUCOSE_VALUE"),
    high_color=env.get("HIGH_COLOR"),
    low_glucose=env.get("LOW_GLUCOSE_VALUE"),
    color_in_range=env.get("RANGE_COLOR"),
    low_color=env.get("LOW_COLOR"),
    start_time=env.get("START_TIME"),
    end_time=env.get("END_TIME"),
    timezone=env.get("TIMEZONE_DIFFERENCE"),
    nightscout_difference=Duration(
        env.get("NIGHTSCOUT_REALTIME_DIFFERENCE")
    ).to_minutes(),
    token=env.get("TOKEN"),
    delay_color=env.get("DELAY_COLOR"),
)

if __name__ == "__main__":
    conn.run()

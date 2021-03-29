from os import environ as env

import HueConnection


conn = HueConnection.HueConnector(
    n_url=env.get("NIGHTSCOUT_URL"),
    phillips_ip=env.get("PHILLIPS_IP"),
    phillips_user=env.get("PHILLIPS_USERNAME"),
    light_id=env.get("LIGHT_ID"),
    high_color=env.get("HIGH_COLOR"),
    color_in_range=env.get("RANGE_COLOR"),
    low_color=env.get("LOW_COLOR"),
    start_time=env.get("START_TIME"),
    end_time=env.get("END_TIME"),
    timezone=env.get("TIMEZONE_DIFFERENCE"),
    nightscout_difference=env.get("NIGHTSCOUT_TIME_LIMIT"),
    token=env.get("TOKEN")
)


if __name__ == '__main__':
    conn.run()

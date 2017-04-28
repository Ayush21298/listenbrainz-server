#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
from influxdb import InfluxDBClient
import config

if __name__ == "__main__":
    try:
        i = InfluxDBClient(host=config.INFLUX_HOST, port=config.INFLUX_PORT, database=config.INFLUX_DB_NAME)
        i.create_database(config.INFLUX_DB_NAME)
    except Exception as e:
        print("Creating influx DB failed: ", e)

    try:
# TODO use the actual 7 day query here
#        i.create_retention_policy("one_week", "1w", 1, "listenbrainz")
        i.create_retention_policy("one_week", "1h", 1, "listenbrainz")
    except Exception as e:
        print("Creating retention policy failed: ", e)

#!/usr/bin/python3

import time
import json
import subprocess
from subprocess import PIPE

from influxdb import InfluxDBClient

# InfluxDB Settings
DB_ADDRESS = ''
DB_PORT = 8086
DB_USER = ''
DB_PASSWORD = ''
DB_DATABASE = ''

influxdb_client = InfluxDBClient(
    DB_ADDRESS, DB_PORT, DB_USER, DB_PASSWORD, None)


def init_db():
    databases = influxdb_client.get_list_database()

    if len(list(filter(lambda x: x['name'] == DB_DATABASE, databases))) == 0:
        influxdb_client.create_database(
            DB_DATABASE)  # Create if does not exist.
    else:
        influxdb_client.switch_database(DB_DATABASE)  # Switch to if does exist.


def format_for_influx(cliout):
    data = json.loads(cliout)
    # There is additional data in the speedtest-cli output but it is likely not necessary to store.
    influx_data = [
        {
            'measurement': 'ping',
            'time': data['timestamp'],
            'fields': {
                'jitter': data['ping']['jitter'],
                'latency': data['ping']['latency']
            }
        },
        {
            'measurement': 'download',
            'time': data['timestamp'],
            'fields': {
                # Byte to Megabit
                'bandwidth': data['download']['bandwidth'] / 125000,
                'bytes': data['download']['bytes'],
                'elapsed': data['download']['elapsed']
            }
        },
        {
            'measurement': 'upload',
            'time': data['timestamp'],
            'fields': {
                # Byte to Megabit
                'bandwidth': data['upload']['bandwidth'] / 125000,
                'bytes': data['upload']['bytes'],
                'elapsed': data['upload']['elapsed']
            }
        },
        {
            'measurement': 'packetLoss',
            'time': data['timestamp'],
            'fields': {
                'packetLoss': float(data.get('packetLoss', 0.0))
            }
        },
        {
            'measurement': 'server',
            'time': data['timestamp'],
            'fields': {
                'name': data['server']['name'],
                'location': data['server']['location'],
                'host': data['server']['host']
            }
        },
        {
            'measurement': 'identification',
            'time': data['timestamp'],
            'fields': {
                'id': data['result']['id']
            }
        }
     ]

    return influx_data


def main():
    init_db()  # Setup the database if it does not already exist.
    speedtest = subprocess.run(
        ["speedtest", "--accept-license", "--accept-gdpr", "-f", "json"], stdout=PIPE, stderr=PIPE)

    if speedtest.returncode == 0:  # Speedtest was successful.
        data = format_for_influx(speedtest.stdout)
        print("Speedtest Successful:")
        if influxdb_client.write_points(data) == True:
             print("Data written to DB successfully")
    else:  # Speedtest failed.
        print("Speedtest Failed:")
        print(speedtest.stderr)
        print(speedtest.stdout)


if __name__ == '__main__':
    print('Speedtest CLI Data Logger to InfluxDB')
    main()
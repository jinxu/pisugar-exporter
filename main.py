import os
import time
from prometheus_client import start_http_server, Gauge,Info

from pisugar import *

battery = Gauge("pisugar_battery", "Battery level in percent")
temperature = Gauge("pisugar_temperature", "Battery temperature")
voltage = Gauge("pisugar_voltage", "Battery voltage in volts")
    
conn, event_conn = connect_tcp('127.0.0.1')
piSugar = PiSugarServer(conn, event_conn)

def get_metrics():
    b = piSugar.get_battery_level()
    v = piSugar.get_battery_voltage()
    t = piSugar.get_temperature()
    
    battery.set(b)
    temperature.set(t)
    voltage.set(v)
    
if __name__ == '__main__':
    start_http_server(9978)
    while True:
        try:
            get_metrics()
        except:
            pass
        time.sleep(1)

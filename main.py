import os
import time
from prometheus_client import start_http_server, Gauge,Info,Enum
import psutil
from pisugar import *
import time


def get_system_uptime():
    boot_time_timestamp = psutil.boot_time()
    current_time_timestamp = time.time()
    uptime_seconds = current_time_timestamp - boot_time_timestamp
    return uptime_seconds


battery = Gauge("pisugar_battery", "Battery level in percent")
temperature = Gauge("pisugar_temperature", "Battery temperature")
voltage = Gauge("pisugar_voltage", "Battery voltage in volts")
cpu = Gauge("cpu","CPU Usag %")
uptime  = Gauge("uptime","System Uptime")
memory = Gauge("memory","Memory usage %")
diskFree = Gauge("disk_free","Disk Free Space")
byteSend = Gauge("byte_send","Bytes send")

conn, event_conn = connect_tcp('127.0.0.1')
piSugar = PiSugarServer(conn, event_conn)

def get_metrics():
    b = piSugar.get_battery_level()
    v = piSugar.get_battery_voltage()
    t = piSugar.get_temperature()
    
    battery.set(b)
    temperature.set(t)
    voltage.set(v)

    cpuUsage = psutil.cpu_percent(interval=1)
    cpu.set(cpuUsage)

    uptime.set(get_system_uptime())
    memory.set(psutil.virtual_memory().percent)
    partition_usage = psutil.disk_usage('/')
    diskFree.set(partition_usage.free / (1024.0 ** 3))
    byteSend.set(psutil.net_io_counters().bytes_sent/get_system_uptime())

if __name__ == '__main__':
    start_http_server(9978)
    while True:
        try:
            get_metrics()
        except:
            pass
        time.sleep(1)

#!/bin/python
import time
import socket
from subprocess import Popen
import sys

time.sleep(30)
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.42.0.1', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '10.42.0.1'
    finally:
        s.close()
    return IP

def main(ip):
    cmd = 'DISPLAY=:0 chromium-browser --no-user-gesture-required --noerrdialogs --kiosk http://%s:8000' % ip
    p = Popen(cmd, shell=True)
    p.wait()

if __name__ == "__main__":
    ip = get_ip()
    main(ip)

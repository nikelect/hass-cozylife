""" Controls a Smart Switch trough command line.
"""
import argparse
from custom_components.cozylife.tcp_client import tcp_client

parser = argparse.ArgumentParser()
# Command Example: py send_command.py --ip 192.168.1.199 --state 0
parser.add_argument("--ip", help="device ip")
parser.add_argument("--state", type=int, help="device state")
args = parser.parse_args()

a = tcp_client(args.ip, timeout=0.4)
a._initSocket()

if a._connect:
    # Tested with MINI Smart Switch - Apple Homekit Smart 
    status = a.control({'1': args.state})
    if status:
        print("Control Command Sent.")
    else:
        print("Fail sending the Control Command!")
else:
    print("Error: Not Connected!")

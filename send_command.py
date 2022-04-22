""" Controls a Smart Switch trough command line.
"""
import argparse
from custom_components.cozylife.tcp_client import tcp_client

parser = argparse.ArgumentParser()
parser.add_argument("--ip", help="device ip")
group = parser.add_mutually_exclusive_group()
group.add_argument("--state", type=int, help="device state")
group.add_argument("--toggle", action='store_true', help="toggle the relay state")
args = parser.parse_args()

# Command Examples
# py send_command.py --ip 192.168.1.199 --state 0
# py send_command.py --ip 192.168.1.199 --state 1
# py send_command.py --ip 192.168.1.199 --toggle

a = tcp_client(args.ip, timeout=0.4)
a._initSocket()

if a._connect:
    # Tested with MINI Smart Switch - Apple Homekit Smart
    if args.toggle:
        status = a.control({'2': 1})
    else: # --state
        status = a.control({'1': args.state})
   
    if status != True:
        print("Fail sending the Control Command!")
else:
    print("Error: Not Connected!")

# Print return state.
print(a.query())
# State Examples:
# {'1': 0}
# {'1': 1}
# {'2': 1}
# {'1': 0, '2': 1}
# {'1': 1, '2': 0}

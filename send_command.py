""" Controls/Read a Smart Switch trough command line.

    Command Examples:
    send_command.py --ip 192.168.1.199 --state 0
    send_command.py --ip 192.168.1.199 --state 1
    send_command.py --ip 192.168.1.199 --toggle
    send_command.py get_state --ip 192.168.1.199

"""
import argparse
import sys

from custom_components.cozylife.tcp_client import tcp_client

def control(device, options):
    """ Controls a Relay state.
    
    Parameters
    ----------
    device : tcp_client
        TCP device.
    options : argparse
        Command line options.

    """
    if device._connect:
        # Tested with MINI Smart Switch - Apple Homekit Smart
        if options.toggle:
            status = device.control({'2': 1})
        else: # --state
            status = device.control({'1': options.state})
   
        if status != True:
            print("Fail sending the Control Command!")
    else:
        print("Error: Not Connected!")

    # Print return state.
    print(device.query())
    
def get_state(device, options):
    """ Read a Relay state.
    
    Parameters
    ----------
    device : tcp_client
        TCP device.
    options : argparse
        Command line options.

    """
    # Print return state.
    print(device.query())
    # State Examples:
    # {'1': 0}
    # {'1': 1}
    # {'2': 1}
    # {'1': 0, '2': 1}
    # {'1': 1, '2': 0}

def main(arguments):   
    optparse = argparse.ArgumentParser(
    description='CozyLife command line interface'
    )    

    # sub-command parser
    subparsers = optparse.add_subparsers(
    title="Relay Control/Read",
    description="To Control the relays or Read the relay state.",
    dest="command",
    metavar="<control>, <get_state>"
    )

    subparsers.required = True

    control_parser = subparsers.add_parser('control', help='control the Relay State 0 or 1.')
    control_parser.add_argument("--ip", required=True, help="device ip")
    control_parser.set_defaults(command=control)
    group = control_parser.add_mutually_exclusive_group()
    group.add_argument("--state", type=int, help="device state")
    group.add_argument("--toggle", action='store_true', help="toggle the relay state.")

    get_state_parser = subparsers.add_parser('get_state', help='gets the realy state 0 or 1.')
    get_state_parser.add_argument("--ip", required=True, help="device ip")
    get_state_parser.set_defaults(command=get_state)

    options = optparse.parse_args(arguments)

    device = tcp_client(options.ip, timeout=0.4)
    device._initSocket()

    # Call corresponding function
    options.command(device, options)

# Execute main function
if __name__ == "__main__":
    main(sys.argv[1:])

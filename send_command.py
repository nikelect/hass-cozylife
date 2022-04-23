""" Controls/Read a Smart Switch trough command line.

    Command Examples:
    send_command.py control --ip 192.168.1.199 --function set_gang --gang-code 0 # All Gangs OFF
    send_command.py control --ip 192.168.1.199 --function set_gang --gang-code 1 # Gang1 ON
    send_command.py control --ip 192.168.1.199 --function set_gang --gang-code 5 # Gang1 ON + Gang3 ON
    send_command.py control --ip 192.168.1.199 --function toggle --gang-code (2, 4 or 6) (Gang1, Gang2, Gang3)
    send_command.py get_state --ip 192.168.1.199

"""
import argparse
import sys

from custom_components.cozylife.tcp_client import tcp_client

def control(device, function, gang_code):
    """ Controls a Relay state.
    
    Parameters
    ----------
    device : tcp_client
        TCP device.
    function : string
        "toggle" - toggle the relay.
        "set_gang" - Turn ON or OFF the gangs sending a code.
        ""
    gang_code : int
        0 - All Gangs OFF
        1 - Gang1 ON
        2 - Gang2
        3 - Gang1 ON + Gang2 ON
        4 - Gang3 ON
        5 - Gang1 ON + Gang3 ON
        6 - Gang2 ON + Gang3 ON
        7 - All Gangs OFF
    """
    if device._connect:
        # Tested with MINI Smart Switch - Apple Homekit Smart
        if "toggle" == function:
            status = device.control({gang_code: 1})
        elif "set_gang" == function:
            status = device.control({'1': gang_code})
        else:
            print("Unrecognized function!")
   
        if status != True:
            print("Fail sending the Control Command!")
    else:
        print("Error: Not Connected!")

    # Print return state json message.
    print(device.query())
    
def get_state(device):
    """ Read a Relay state.
    
    Parameters
    ----------
    device : tcp_client
        TCP device.

    """
    # Print return state json message.
    print(device.query())
    # State Examples:
    # {'1': 0}
    # {'1': 1}
    # {'2': 1}
    # {'1': 0, '2': 1}
    # {'1': 1, '2': 0}

def call_method(device, options):
    """ Call the method defined in the command line.
    
    Parameters
    ----------
    device : tcp_client
        TCP device.
    options : argparse
        Command line options.

    """
    if options.command.__name__ == "control":
        control(device, options.function, options.gang_code)
    elif options.command.__name__ == "get_state":
        get_state(device)

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

    control_parser = subparsers.add_parser('control', help='control a relay State "on", "off "or "toggle".')
    control_parser.add_argument("--ip", required=True, help="device ip")
    control_parser.set_defaults(command=control)
    control_parser.add_argument("--gang-code", type=int, help="gang code")
    control_parser.add_argument("--function", type=str, help="'on', 'off' or 'toggle'")

    get_state_parser = subparsers.add_parser('get_state', help='gets the relay/s state 0 or 1.')
    get_state_parser.add_argument("--ip", required=True, help="device ip")
    get_state_parser.set_defaults(command=get_state)

    options = optparse.parse_args(arguments)

    device = tcp_client(options.ip, timeout=0.4)
    device._initSocket()

    # Call corresponding function
    call_method(device, options)

# Execute main function
if __name__ == "__main__":
    main(sys.argv[1:])

import base64
from argparse import ArgumentParser

from colorama import init, Fore
from progressbar import progressbar

import wsHandler as w

# Colours initialization
init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET

ERROR_LIST = ["invalid", "could not", "can't", "cannot", "error", "incorrect, 'Connection Timed Out'"]
KEYWORDS = ["wsfuzz"]


# Retrieves command line arguments entered
def args():
    parser = ArgumentParser()
    subparser = parser.add_subparsers(title='Attack', dest='attack', help='Type of attack to carry out', required=True)

    attack_args = [
        ('xss', 'ws://dvws.local:8080/reflected-xss', 'payloads/xss.txt'),
        ('sqli', 'ws://dvws.local:8080/authenticate-user-blind', 'payloads/sqli.txt'),
        ('cmdi', 'ws://dvws.local:8080/command-execution', 'payloads/cmdi.txt'),
        ('lfi', 'ws://dvws.local:8080/file-inclusion', 'payloads/lfi.txt')
    ]

    # Set default values for different attacks; users can supply their own parameters
    for attack, default_target, default_payload in attack_args:
        attack_parser = subparser.add_parser(attack)
        attack_parser.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default=default_target)
        attack_parser.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default="*")
        attack_parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default=default_payload)
        attack_parser.add_argument('-e', '--encode', nargs='?', type=str, choices=('none', 'base64', 'hex', 'url'), help='Encoding scheme to use, default=none ', default='none')

    return parser.parse_args()


# Return encoded messages based on the selected scheme
def encoding(encoding_scheme, msg):
    if encoding_scheme == 'base64':
        return base64.b64encode(msg.encode('utf-8')).decode('utf-8')
    elif encoding_scheme == 'hex':
        return msg.encode('utf-8').hex()
    elif encoding_scheme == 'url':
        return urllib.parse.quote_plus(msg)
    # More methods will be supported in the future
    return msg


# Encode and send payloads to server
def test_payloads(payload_list, exampleRequest, target, encode, attack_name):
    for payload in progressbar((payload_list), redirect_stdout=True):
        line = payload.strip('\n')
        newRequest = exampleRequest.replace('*', encoding(encode,line))
        response = w.InteractWithWsSite(target, newRequest)
        global PAYLOAD 
        PAYLOAD = line
        if check_response(response):
            print(f"{GREEN}[+]{RESET} {attack_name} successful!")
            print(f"{GREEN}[+]{RESET} Payload: %s" % line)
            print(f"{GREEN}[+]{RESET} Response: %s\n" % response)
        else:
            print(f"{RED}[-]{RESET} {attack_name} failed!")
            print(f"{RED}[-]{RESET} Payload: %s\n" % line)


# Different checks to test if response is a valid/successful attack
def check_response(response):
    if not response:
        return False
    if response == ' ':
        return False
    if PAYLOAD in response:
        return True
    if any([x in response.casefold() for x in ERROR_LIST]):
        return False
    if any([x in response.casefold() for x in KEYWORDS]):
        return True
    return True

# Start attack
def execute_attack(target, payload, example_request, encode, attack_name):
    print(f"{GREEN}[+]{RESET} {attack_name} selected! Commencing {attack_name} attack...")
    print(f"{GREEN}[+]{RESET} {encode} encoding scheme detected!")
    with open(payload, 'r',encoding="utf-8") as payload_file:
        payload_list = payload_file.readlines()
    test_payloads(payload_list, example_request, target, encode, attack_name)
    
# usage (full)
# python wsfuzz.py {attack_name} -t {target_url} -r {payload_example_string} -p {payload_list} -e {encoding_method}
# python wsfuzz.py sqli -t ws://dvws.local:8080/authenticate-user -r '{"auth_user":"*","auth_pass":""}' -p payloads/custom_sqli.txt -e base64
# python wsfuzz.py cmdi -t ws://dvws.local:8080/command-execution -r "127.0.0.1*" -p payloads/cmdi2.txt -e normal
# python wsfuzz.py lfi -t ws://dvws.local:8080/file-inclusion -r "*" -p payloads/lfi.txt -e normal    
# python wsfuzz.py xss -t ws://dvws.local:8080/reflected-xss -r "*" -p payloads/cmdi2.txt -e normal

# usage (partial)
# python wsfuzz.py xss -t ws://dvws.local:8080/file-inclusion -r "*" 

def main():
    arg = args()

    if not arg.target.startswith(("ws://", "wss://")):
        print(f"{RED}[-]{RESET} Please enter a valid WebSocket URL")
        exit(0)
        
    attacks = {
        'xss': 'XSS',
        'lfi': 'LFI',
        'sqli': 'SQLi',
        'cmdi': 'command injection'
    }
    
    attack_name = attacks.get(arg.attack)
    if attack_name:
        execute_attack(arg.target, arg.payload, arg.request, arg.encode, attack_name)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"{RED}[-]{RESET} User initiated termination, exiting...")
    except ConnectionRefusedError:
        print(f"{RED}[-]{RESET} Error connecting to target websocket, exiting...")
        exit(0)

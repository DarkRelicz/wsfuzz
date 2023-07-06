from argparse import ArgumentParser
import wsHandler as w
import base64

from time import sleep
from colorama import init, Fore
from progressbar import progressbar

# coloura initialization
init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET



# retrieves command line arguments entered
def args():
    parser = ArgumentParser()

    subparser = parser.add_subparsers(title='Attack', dest='attack', help='Type of attack to carry out', required=True)
    xss = subparser.add_parser('xss')
    sqli = subparser.add_parser('sqli')
    cmdi = subparser.add_parser('cmdi')
    lfi = subparser.add_parser('lfi')

    xss.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/reflected-xss')
    xss.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default="*")
    xss.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/xss.txt')
    xss.add_argument('-e', '--encode', nargs='?', type=str, choices=('normal', 'base64'), help='Encoding scheme to use, select normal for no encoding', default='normal')

    sqli.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/authenticate-user-blind')
    sqli.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default='*')
    sqli.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/sqli.txt')
    sqli.add_argument('-e', '--encode', nargs='?', type=str, choices=('normal', 'base64'), help='Encoding scheme to use, select normal for no encoding', default='normal')

    cmdi.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/command-execution')
    cmdi.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default="*")
    cmdi.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/cmdi.txt')
    cmdi.add_argument('-e', '--encode', nargs='?', type=str, choices=('normal', 'base64'), help='Encoding scheme to use, select normal for no encoding', default='normal')

    lfi.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/file-inclusion')
    lfi.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default="*")
    lfi.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/lfi.txt')
    lfi.add_argument('-e', '--encode', nargs='?', type=str, choices=('normal', 'base64'), help='Encoding scheme to use, select normal for no encoding', default='normal')

    return parser.parse_args()



# return encoded messages based on the selected scheme
def encoding(encoding_scheme, msg):
    if encoding_scheme == 'base64':
        return base64.b64encode(msg.encode('utf-8')).decode('utf-8')
    return msg

# encode and send payloads to server
def test_payloads(payload_list, exampleRequest, target, encode):
    for payload in progressbar((payload_list), redirect_stdout=True):
        line = payload.strip('\n')
        newRequest = exampleRequest.replace('*', encoding(encode, line))
        print("request: %s\n" % newRequest)
        response = w.InteractWithWsSite(target, newRequest)
        print("response: %s\n" % response)
        if response != ' ':
            print(f"{GREEN}[+]{RESET} Command injection successful!")
            print(f"{GREEN}[+]{RESET} Command output: {response}")
            print(f"{GREEN}[+]{RESET} Command: {line}")
        else:
            print(f"{RED}[-]{RESET} Command injection failed!")
            print(f"{RED}[-]{RESET} Command: {line}")
        print("response: %s\n" % response)
        sleep(0.001)

def execute_attack(target, payload, example_request, encode, attack_name):
    print(f"{GREEN}[+]{RESET} {attack_name} selected! Commencing {attack_name} attack...")
    print(f"{GREEN}[+]{RESET} {encode} encoding scheme detected!")
    with open(payload, 'r') as payload_file:
        payload_list = payload_file.readlines()
    test_payloads(payload_list, example_request, target, encode)
    
# usage
# python wsfuzz.py sqli -r '{"auth_user":"*","auth_pass":""}' -p payloads/custom_sqli.txt -e base64
# python wsfuzz.py cmdi -t ws://dvws.local:8080/command-execution -r "127.0.0.1*" -p payloads/cmdi2.txt -e normal    

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
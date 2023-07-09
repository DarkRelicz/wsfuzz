import base64
from argparse import ArgumentParser

from colorama import init, Fore
from progressbar import progressbar

import wsHandler as w

# coloura initialization
init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET

ERROR_LIST = ["invalid", "could not", "can't", "cannot", "error", "incorrect, 'Connection Timed Out'"]
KEYWORDS = ["wsfuzz"]


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
    elif encoding_scheme == 'normal':
        return msg


# encode and send payloads to server
def test_payloads(payload_list, exampleRequest, target, encode, attack_name):
    for payload in progressbar((payload_list), redirect_stdout=True):
        line = payload.strip('\n')
        newRequest = exampleRequest.replace('*', encoding(encode,line))
        response = w.InteractWithWsSite(target, newRequest)
        global PAYLOAD 
        PAYLOAD = line
        # print(response)
        if check_response(response):
            print(f"{GREEN}[+]{RESET} {attack_name} successful!")
            print(f"{GREEN}[+]{RESET} Payload: %s" % line)
            print(f"{GREEN}[+]{RESET} Response: %s\n" % response)
        else:
            print(f"{RED}[-]{RESET} {attack_name} failed!")
            print(f"{RED}[-]{RESET} Payload: %s\n" % line)
            
def check_response(response):
    if response == '':
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

# # conduct cross site scripting attack
# def xss(target, payload, exampleRequest, encode):
#     print(f"{GREEN}[+]{RESET} xss selected! Commencing XSS attack...")
#     print(f"{GREEN}[+]{RESET} {encode} encoding scheme detected!")
#     with open(payload, 'r') as payload_file:
#         payloads = payload_file.readlines()
#     for line in payloads:
#         line = line.replace('\n', '')
#         newRequest = exampleRequest.replace('*', line)
#         response = w.InteractWithWsSite(target, newRequest)
#         print("response: %s\n" % response)
    


# # conduct local file inclusion attack
# def lfi(target, payload, exampleRequest, encode):
#     print(f"{GREEN}[+]{RESET} lfi selected! Commencing LFI attack...")
#     print(f"{GREEN}[+]{RESET} {encode} encoding scheme detected!")
#     with open (payload, 'r') as payload_file:
#         payloads = payload_file.readlines()
#     for line in payloads:
#         line = line.replace('\n', '')
#         newRequest = exampleRequest.replace('*', line)
#         response = w.InteractWithWsSite(target, newRequest)
#         if (response != '' and response != ' ') or any([x in response.casefold() for x in ERROR_LIST]):
#             print(f"{GREEN}[+]{RESET} Local file inclusion successful!")
#             print(f"{GREEN}[+]{RESET} Payload: %s" % line)
#             print(f"{GREEN}[+]{RESET} Response: %s\n" % response)
#         else:
#             print(f"{RED}[-]{RESET} Local file inclusion failed!")
#             print(f"{RED}[-]{RESET} Payload: %s\n" % line)



# # conduct sql injection attack
# def sqli(target, payload, exampleRequest, encode):
    
#     print(f"{GREEN}[+]{RESET} sqli selected! Commencing SQLi attack...")
#     print(f"{GREEN}[+]{RESET} {encode} encoding scheme detected!")
#     with open (payload, 'r') as payload_file:
#         payloads = payload_file.readlines()
#     for line in payloads:
#         line = line.replace('\n', '')
#         newRequest = exampleRequest.replace('*', encoding(encode, line))
#         print("request: %s\n" % newRequest)
#         response = w.InteractWithWsSite(target, newRequest)
#         print("response: %s\n" % response)
#         if response != ' ':
#         # chk_match = [x for x in error_list if x in response.casefold()]
#         if any([x in response.casefold() for x in ERROR_LIST]) or response == ' ':
#             print(f"{RED}[-]{RESET} SQL injection failed!")
#             print(f"{RED}[-]{RESET} Payload: %s\n" % line)
#         else:
#             print(f"{GREEN}[+]{RESET} SQL injection successful!")
#             print(f"{GREEN}[+]{RESET} Payload: %s" % line)
#             print(f"{GREEN}[+]{RESET} Response: %s\n" % response)
# # usage
# # python wsfuzz.py sqli -r '{"auth_user":"*","auth_pass":""}' -p payloads/custom_sqli.txt -e base64    


# # conduct command injection attack
# def cmdi(target, payload, exampleRequest, encode):
#     print(f"{GREEN}[+]{RESET} cmdi selected! Commencing command injection attack...")
#     print(f"{GREEN}[+]{RESET} {encode} encoding scheme detected!")
#     with open (payload, 'r') as payload_file:
#         payloads = payload_file.readlines()
#     for line in payloads:
#         line = line.replace('\n', '')
#         newRequest = exampleRequest.replace('*', line)
#         response = w.InteractWithWsSite(target, newRequest)
#         if 'wsfuzz' in response:
#             print(f"{GREEN}[+]{RESET} Command injection successful!")
#             print(f"{GREEN}[+]{RESET} Command output: {response}")
#             print(f"{GREEN}[+]{RESET} Command: {line}")
#         else:
#             print(f"{RED}[-]{RESET} Command injection failed!")
#             print(f"{RED}[-]{RESET} Command: {line}")
#         print("response: %s\n" % response)
#         sleep(0.001)

def execute_attack(target, payload, example_request, encode, attack_name):
    print(f"{GREEN}[+]{RESET} {attack_name} selected! Commencing {attack_name} attack...")
    print(f"{GREEN}[+]{RESET} {encode} encoding scheme detected!")
    with open(payload, 'r',encoding="utf-8") as payload_file:
        payload_list = payload_file.readlines()
    test_payloads(payload_list, example_request, target, encode, attack_name)
    
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
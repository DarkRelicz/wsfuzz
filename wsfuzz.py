from argparse import ArgumentParser
import wsHandler as w
import sys


def args():
    parser = ArgumentParser()
    
    # Uncomment this
    # parser.add_argument('-t', '--target', nargs='?', type=str, required=True, help='Target Websocket URL')
    # parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi, lfi'], required=True, help='Type of attack to carry out')
    # parser.add_argument('-r', '--request', nargs='?', type=str, required=True, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}")
    # parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use')
    
    # Testing Purpose (sqli)
    # parser.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/authenticate-user')
    # parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi, lfi'], help='Type of attack to carry out', default='sqli')
    # parser.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default="{'auth_user'':'*','auth_pass':'*'}")
    # parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/sqli.txt')
    # return parser.parse_args()

    # # Testing Purpose (xss)
    # parser.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/reflected-xss')
    # parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi, lfi'], help='Type of attack to carry out', default='xss')
    # parser.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default="{'*'}")
    # parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/xss.txt')
    # return parser.parse_args()

    # # Testing Purpose (cli)
    # parser.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/command-execution')
    # parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi, lfi'], help='Type of attack to carry out', default='cmdi')
    # parser.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default="{'*'}")
    # parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/cmdi.txt')
    # return parser.parse_args()

    # Testing Purpose (lfi)
    parser.add_argument('-t', '--target', nargs='?', type=str, help='Target Websocket URL', default='ws://dvws.local:8080/file-inclusion')
    parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi, lfi'], help='Type of attack to carry out', default='lfi')
    parser.add_argument('-r', '--request', nargs='?', type=str, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}", default="{'*'}")
    parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use', default='payloads/lfi.txt')
    return parser.parse_args()





def xss(target, payload, exampleRequest):
    with open (payload, 'r') as payload_file:
        payloads = payload_file.readlines()
    for line in payloads:
        line = line.replace('\n', '')
        newRequest = exampleRequest.replace('*', line)
        w.InteractWithWsSite(target, newRequest)
    print('xss')
    
def lfi(target, payload, exampleRequest):
    with open (payload, 'r') as payload_file:
        payloads = payload_file.readlines()
    for line in payloads:
        line = line.replace('\n', '')
        newRequest = exampleRequest.replace('*', line)
        w.InteractWithWsSite(target, newRequest)
    print('lfi')

def sqli(target, payload, exampleRequest):
    with open (payload, 'r') as payload_file:
        payloads = payload_file.readlines()
    for line in payloads:
        line = line.replace('\n', '')
        newRequest = exampleRequest.replace('*', line)
        w.InteractWithWsSite(target, newRequest)
    print('sqli')
    
def cmdi(target, payload, exampleRequest):
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
        print("Please enter a valid websocket url")
        exit(0)

    if arg.attack == 'xss':
        if arg.payload:
            payload = arg.payload
        else:
            payload = "dir_to_default_xss_payload"
        xss(arg.target, payload, arg.request)

    if arg.attack == 'lfi':
        if arg.payload:
            payload = arg.payload
        else:
            payload = "dir_to_default_lfi_payload"
        lfi(arg.target, payload, arg.request)

    if arg.attack == 'sqli':
        if arg.payload:
            payload = arg.payload
        else:
            payload = "dir_to_default_sqli_payload"
        sqli(arg.target, payload, arg.request)

    if arg.attack == 'cmdi':
        if arg.payload:
            payload = arg.payload
        else:
            payload = "dir_to_default_cmi_payload"
        cmdi(arg.target, payload, arg.request)


if __name__ == '__main__':
    main()

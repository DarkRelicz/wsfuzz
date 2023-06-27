from argparse import ArgumentParser
import wsHandler as w

def args():
    parser = ArgumentParser()
    parser.add_argument('-t', '--target', nargs='?', type=str, required=True, help='Target Websocket URL')
    parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi, lfi'], required=True, help='Type of attack to carry out')
    parser.add_argument('-r', '--request', nargs='?', type=str, required=True, help="Format of an example request, e.g. {'auth_user'':'*','auth_pass':'*'}")
    parser.add_argument('-p', '--payload', nargs='?', type=str, help='Payload file to use')
    return parser.parse_args()


def xss(target, payload, exampleRequest):
    print('xss')

def lfi(target, payload, exampleRequest):
    print('lfi')

def sqli(target, payload, exampleRequest):
    print('sqli')

def cmdi(target, payload, exampleRequest):
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
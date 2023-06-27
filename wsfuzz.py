from argparse import ArgumentParser

def args():
    parser = ArgumentParser()

    parser.add_argument('-t', '--target', nargs='?', type=str, required=True, help='Target Websocket URL')
    parser.add_argument('-a', '--attack', choices=['xss', 'sqli', 'cmdi'], required=True, help='Type of attack to carry out')
    parser.add_argument('-p', '--payload', nargs='?', type=str, required=True, help='Payload file to use')

    return parser.parse_args()


def xss(target, payload, exampleRequest):
    print('xss')

def lfi(target, payload, exampleRequest):
    print('lfi')

def sqli(target, payload):
    print('sqli')

def cmdi(target, payload):
    print('cmd injection')


# ws helper function
def ws_handler(url, payload):
    return True


def main():
    arg = args()

    print(arg.target)
    print(arg.payload)
    if arg.attack == 'xss':
        if arg.payload :
            payload = arg.payload
        else:
            payload = "/var/xss"
        xss(payload)
    if arg.attack == 'lfi':
        payload = "/var/lfi"
        lfi(payload)
    if arg.attack == 'cmdi':
        payload = "/var/cmdi"
        cmdi(payload)



if __name__ == '__main__':
    main()
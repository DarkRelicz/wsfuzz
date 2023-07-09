from pyfiglet import Figlet

def init_banner():
    custom_fig = Figlet(font='slant')
    
    print(custom_fig.renderText('wsfuzz'))
    print('-----A WebSocket Fuzzing Tool-----\n\n\n')

    return None
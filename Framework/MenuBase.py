
from colorama import Fore, Back, Style, init

class MenuBase:
    def __init__(self):
        init(convert=True)

    '''
    pip install colorama
    Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    Style: DIM, NORMAL, BRIGHT, RESET_ALL
    print(Fore.RED + 'some red text')
    print(Back.GREEN + 'and with a green background')
    print(Style.DIM + 'and in dim text')
    print(Style.RESET_ALL)
    print('back to normal now')
    '''

    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    '''
    BORDER = Fore.CYAN
    MSG = '\033[94m'
    TITLE = '\033[92m'
    SETTING = Fore.MAGENTA + Style.BRIGHT
    STEPS = Fore.CYAN + Style.BRIGHT
    CODE = Fore.GREEN + Style.DIM
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CMD = Back.GREEN + Fore.RED

    def prompt(self, msg = None):
        if msg != None:
            print(msg)
        print('> ', end = '')

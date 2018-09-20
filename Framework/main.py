import os
import platform
import argparse

from Session import *

if __name__ == "__main__":
    
    #os.system("powershell.exe $ENV:PATH += \';C:/Program Files/Wireshark\'")
    #os.system("powershell.exe $ENV:PATH += \';C:/Program Files (x86)/Nmap\'")

    try:
        parser = argparse.ArgumentParser(description='Ready Go')
        parser.add_argument('-s','--session', help='Load a specific session', required = False)
        parser.add_argument('-n','--new', help='Create a new session with specified name', required = False)
        parser.add_argument('-i','--ip', help='IP of target', required = False)
        args = parser.parse_args()

        if args.session:
            session.start(args.session)
        elif args.new:
            session.start(args.new, True, args.ip)
        else:
            session.start()
            #session.start('debug12345')

        session.screen.optionsShow()

        while True:
            session.screen.userinput()

    except KeyboardInterrupt as e:
        session.endProgram()

# TODOS:
'''
2. implement Tcpdump
7. Proxychains
8. RAT
10. msfvenom 
Parat - Undetectable Python Payload
install dbqwaudit
install john-omp
learn crunch
wordlists:
    AD/Windows network passwords
    web passwords
    http directories
    users
    compile, and remove duplicates
    create top choice list
    take total list and chop it into ~4 to pass to all kali servers

parsers:
Gobuster

================== ATTACKING =================
FTP:
1. check for annonyous login
2. check for blank root/admin login
3. bruteforce it using: ...

HTTP:
1. dird
bruteforce using: gobuster, ...
wfuzz (https://www.youtube.com/watch?v=CUbWpteTfio)
check for sql injection


Images found:
exiftool to analyize the image/s

SSH:
bruteforce using: hydra



'''

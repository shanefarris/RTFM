
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
                          12 : 'Ming C Compiler',
                          13 : 'Hyperion',
                          14 : 'Ettercap',
                          15 : 'Imagemagick',
                          16 : 'FTP Client',
                          17 : 'tkinter',
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
        elif index == 12:
            self.installMing()
        elif index == 13:
            self.installHyperion()
        elif index == 14:
            self.installEttercap()
        elif index == 15:
            self.installImagemagick()
        elif index == 16:
            self.installFtp()
        elif index == 17:
            self.installTkinter()
        elif index == 29:
            self.installAll()

    def installMinimum(self):
        os.system('pip install colorama')
        os.system('python -m pip install -U pip')
        os.system('pip install python-libnmap')

        return

    def installStandard(self):
        os.system('pip install colorama')

        if platform.system() == 'Windows':
            os.system('python -m pip install -U pip')
            #os.system('pip install scapy')
            os.system('pip install python-libnmap')
            print('Trying to download PentestBox: https://pentestbox.org')
            os.system('Invoke-WebRequest -OutFile ./PentestBox.exe https://sourceforge.net/projects/pentestbox')
        else:
            os.system('echo \"deb http://http.kali.org/kali kali-rolling main contrib non-free\" >> /etc/apt/sources.list')
            os.system('apt-get -y update && apt-get upgrade')
            os.system('pip install -U pip')
            os.system('pip install pynput')
            os.system('apt -y update && apt -y install exploitdb')
            os.system('apt -y install libxml2-utils')
            os.system('searchsploit -u')
            os.system('apt-get -y install python3-libnmap')
            os.system('apt -y install libxml2-utils')
            os.system('apt-get -y install python-setuptools python-pip')
            os.system('gunzip /usr/share/wordlists/rockyou.txt.gz')
            os.system('apt-get -y install nbtscan-unixwiz')
            os.system('apt-get -y install pluma')
            os.system('apt-get -y install apt2')
            os.system('apt-get -y install casefile')
            os.system('apt install gnome-screenshot')
            os.system('../Scripts/playbook_install.sh')
            os.system('apt -y --reinstall install open-vm-tools-desktop fuse')
            os.system('mkdir /mnt/hgfs')
            os.system('mkdir /mnt/hgfs/Shared')
            os.system('vmhgfs-fuse -o allow_other -o auto_unmount .host:/Shared /mnt/hgfs/Shared')
            os.system('apt-get install gcc-multilib g++-multilib')
            
            # Missing Nmap scripts
            # db2-discover
            os.system('cp ../Scripts/broadcast-hid-discoveryd.nse /usr/share/nmap/scripts')
            os.system('cp ../Scripts/db2-das-info.nse /usr/share/nmap/scripts')
            os.system('cp ../Scripts/broadcast-jenkins-discover.nse /usr/share/nmap/scripts; nmap --script-updatedb')
            
    def installAll(self):
        self.installStandard()
            
            # Install scapy from source
            #os.system('mkdir tmp')
            #os.system('wget --trust-server-names https://github.com/secdev/scapy/archive/master.zip ./tmp')
            #os.system('unzip ./tmp/scapy-master')
            #os.system('cd master')
            #os.system('python3 ./tmp/scapy-master/setup.py install')

            # If libnmap doesn't install, try this
            
            #git clone https://github.com/savon-noir/python-libnmap.git
            #cd python-libnmap
            #python setup.py install
            
        #os.system('pip install python-nmap')
        
        self.installNikto()
        self.installNmap()
        self.installNessus()
        self.installPyshark()
        self.installHttrack()
        self.installOpenVAS()
        self.installMing()
        self.installHyperion()
        self.installEttercap()
        self.installImagemagick()
        self.installTkinter()

    def installNikto(self):
        print('** Installing Nikto **')

        # https://nmap.org/dist/nmap-7.70-setup.exe
        if platform.system() == 'Windows':
            print('DOWNLOAD: https://projects.giacomodrago.com/nikto-win/nikto-2.1.5-win.7z')
        else:
            os.system('git clone https://github.com/sullo/nikto ~')

    def installNmap(self):
        print('** Installing Nmap/libs **')
        os.system('pip install python-nmap')

        # https://nmap.org/dist/nmap-7.70-setup.exe
        if platform.system() == 'Windows':
            print('DOWNLOAD: https://nmap.org/dist/nmap-7.70-setup.exe')
        else:
            os.system('https://nmap.org/dist/nmap-7.70.tar.bz2')
            os.system('bzip2 -cd nmap-7.70.tar.bz2 | tar xvf -')
            os.system('cd nmap-7.70')
            os.system('./configure')
            os.system('make')
            os.system('su root')
            os.system('make install')

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
        os.system('pip3 install pyshark')
        
    def installSmbexec(self):
        print('Installing SMBexec')
        os.system('git clone https://github.com/brav0hax/smbexec.git ~/')
        os.system('~/smbexec/install.sh')
        os.system('~/smbexec/install.sh')
        print('If this has failed then try \'../Scripts/playbook_install.sh\'')
        
    def installVeil(self):
        print('NOT DONE')
        
    def installDiscoverScripts(self):
        print('Installing Discover Scripts')
        os.system('git clone https://github.com/leebaird/discover.git /opt/tools/discover')
        os.system('/opt/tools/discover/setup.sh')
        return

    def installHttrack(self):
        print('Installing Httrack (web scraper)')
        os.system('apt-get -y install httrack')

    def installOpenVAS(self):
        print('Installing OpenVAS')
        os.system('apt-get -y install openvas')
        
    def installMing(self):
    	print('Installing Ming C Compiler')
    	os.system('apt-get -y install mingw-w64')
    	
    def installHyperion(self):
    	print('Installing Hyperion for encryption')
    	os.system('wget https://github.com/nullsecuritynet/tools/raw/master/binary/hyperion/release/Hyperion-1.2.zip ~/')
    	os.system('unzip ~/Hyperion-1.2.zip')
    	
    def installEttercap(self):
        print('Setting permissions for Ettercap')
        os.system('sed -i -e \'s/ec_uid = 65534/ec_uid = 0/g\' /etc/ettercap/etter.conf')
        os.system('sed -i -e \'s/ec_gid = 65534/ec_uid = 0/g\' /etc/ettercap/etter.conf')
        
    def installImagemagick(self):
        os.system('apt-get install -y imagemagick')
        
    def installFtp(self):
        os.system('apt-get install ftp')

    def installTkinter(self):
        os.system('apt-get install python python3-tk; pip3 install pygubu')
        
if __name__ == "__main__":
    try:
        setup = Setup()

        parser = argparse.ArgumentParser(description='Ready Go')
        parser.add_argument('-m','--minimum', help='Only install the minimum required libraries to run this program', required = False)
        args = parser.parse_args()

        if args.minimum:
            setup.installMinimum()
        else:
            setup.installAll()

    except Exception as e:
        print(e)

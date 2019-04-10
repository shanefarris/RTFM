
import os
import platform
import logging
import subprocess
from subprocess import Popen, PIPE
from threading import Thread
from colorama import Fore, Back, Style, init

from Session import *
from MenuBase import *
from ToolManager import *
from Parsers import ParserNmap, ParserPrivesc

class Enumeration(MenuBase):

    def __init__(self):
        init()
        self.targetOS = 'Agnostic'
        self._tsharks = []
        self._tcpdumps = []

        self._scans = { -1 : 'Nmap:',
                       1 : 'LOUD Aggressive Nmap scan (TCP)', 
                       2 : 'LOUD Aggressive Nmap scan (UDP)',
                       3 : 'LOUD Standard Nmap scan (TCP)',
                       4 : 'LOUD Standard Nmap scan (UDP)',
                       5 : 'Quiet Syn Nmap scan (TCP)',
                       6 : 'Ping Scan (for subnets)',
                       7 : 'OS Fingerprinting Nmap scan',
                       8 : 'Quick/Simple scan',
                       10 : 'Super Stealth Scan',
                       18 : 'Parse all Nmap files',
                       -2 : '',
                       -3 : 'Nikto:',
                       20 : 'Config Options',
                       21 : 'Standard Scan',
                       22 : 'Use Proxy (Setup proxy manually)',
                       -4 : '',
                       -5 : 'TShark:',
                       30 : 'All Traffic',
                       31 : 'HTTP Only',
                       32 : 'DNS Analysis',
                       -6 : '',
                       -7 : 'Other Tools:',
                       40 : 'DnsRecon (Need name not IP)',
                       41 : 'Whatweb',
                       42 : 'Dird',
                       43 : 'Wpscan',
                       44 : 'Nessus Scanner',
                       45 : 'Nexpose Scanner',
                       46 : 'OpenVAS Scanner',
                       -8 : '',
                       -9 : 'tcpdump:',
                       60 : 'All Traffic',
                       61 : 'HTTP Only',
                       62 : 'DNS Analysis' }

        self._internals = { 1 : 'Standard Local Scan/Enumeration', 2 : 'Lynis (Linux/Unix only)', 3 : 'unix-privesc-check (Linux/Unix Only)' }

    def getScanDictionary(self):
        return self._scans

    def getInternalDictionary(self):
        return self._internals

    def run(self, index):
        if index.isdigit():
            num = int(index)
            if num <= 19:
                self.runNmap(num)
            elif num < 30 and num > 19:
                self.runNikto(num)
            elif num < 40 and num > 29:
                self.runTshark(num)
            elif num < 50 and num > 39:
                self.runOther(num)
            elif num < 70 and num > 59:
                self.runTcpdump(num)
        else:
            self.prompt('Try again')

        self.prompt()

    def runNikto(self, index):
        target = session.getRemoteHost()
        dir = session.getIntelDir()

        cmd = 'NO COMMAND CREATED'

        if index == 20:
            print('Config for proxies, and other options: /etc/nikto/config.txt')
            print('# Proxy settings -- still must be enabled by -useproxy\nPROXYHOST=85.28.28.209\nPROXYPORT=8080')

        elif index == 21:
            cmd = 'nikto -Display V -host ' + target + ' -Format HTM -output ' + dir + '/nikto.html'
            
        elif index == 22:
            cmd = 'nikto -useproxy -Display V -host ' + target + ' -Format HTM -output ' + dir + '/nikto.html'

        if cmd != 'NO COMMAND CREATED':
            session.runThreadedCmd(cmd, cmd)

    def runNmap(self, index):
        if index == 18:
            parser = ParserNmap()
            import glob
            for file in glob.glob(session.getIntelDir() + '/nmap_*'):
                print(self.TITLE + 'Parsing: ' + file + self.ENDC)
                parser.parseFile(file)
            return

        if index == 1:
            session.toolManager.runByName('NmapLoudTcp', ToolCategory.Enumeration, threaded = True)
        elif index == 2:
            session.toolManager.runByName('NmapLoudUdp', ToolCategory.Enumeration, threaded = True)
        elif index == 3:
            session.toolManager.runByName('NmapStandardTcp', ToolCategory.Enumeration, threaded = True)
        elif index == 4:
            session.toolManager.runByName('NmapStandardUdp', ToolCategory.Enumeration, threaded = True)
        elif index == 5:
            session.toolManager.runByName('NmapSneaky', ToolCategory.Enumeration, threaded = True)
        elif index == 6:
            session.toolManager.runByName('NmapPing', ToolCategory.Enumeration, threaded = True)
        elif index == 7:
            session.toolManager.runByName('NmapVersion', ToolCategory.Enumeration, threaded = True)
        elif index == 8:
            session.toolManager.runByName('NmapQuick', ToolCategory.Enumeration, threaded = True)
        elif index == 10:
            session.toolManager.runByName('NmapStealth', ToolCategory.Enumeration)

    def runTshark(self, index):
        target = session.getRemoteHost()
        dir = session.getIntelDir()

        # List and select which interface
        if platform.system() == 'Windows':
            os.chdir('C:/Program Files/Wireshark')
            t = Thread(target=os.system, args=('tshark -D',))
            t.start()
        else:
            os.system('tshark -D')

        print('Enter listening interface: ')
        interface = input()

        # Create tshark command
        cmd = 'tshark -i ' + interface
        dir = session.CWD + '/' + dir

        filter = ' -Q'
        file = ''

        if index == 30:
            file = dir + '/tshark_all.pcap '
        elif index == 31:
            file = dir + '/tshark_http.pcap '
            filter = filter + ' -Y http.request '
        elif index == 32:
            file = dir + '/tshark_http.pcap '
            filter = filter + ' -f "src port 53" -n -T fields -e dns.qry.name -e dns.resp.addr '

        # Combine all options and log it
        cmd = cmd + ' ' + filter + ' -w ' + file 
        session.runThreadedCmd(cmd, cmd)
            
        import time
        time.sleep(3)
        os.chdir(session.CWD)

        print('Scanning in the background')

    def runOther(self, index):
        target = session.getRemoteHost()
        dir = session.getIntelDir()

        if index == 40:
            session.runCmdSimple('dnsrecon ' + session.getRemoteHost(), 'Enumerating with dnsrecon')
        elif index == 41:
            outfile = dir + '/whatweb_subnet.txt'
            if '/' in session.getRemoteHost():
                cmd = 'whatweb -v --no-errors ' + session.getRemoteHost() + ' | tee ' + outfile
            else:
                cmd = 'whatweb -v -a 3 ' + session.getRemoteHost() + ' | tee ' + outfile
            session.runCmdSimple(cmd, 'Using whatweb for vulnerability scanning', outfile)
        elif index == 42:
            session.runThreadedCmd('dirb http://' + session.getRemoteHost() + ' -w -S | tee ' + dir + '/dirb.txt', 'Dirb')
        elif index == 43:
            session.runThreadedCmd('wpscan' + session.getRemoteHost() + ' | tee ' + dir + '/wpscan.txt', 'Wpscan')
        elif index == 44:
            session.runCmdSimple('/etc/init.d/nessusd start')
            session.runCmdSimple('firefox https://localhost:8834', 'Starting Nessus scanner')
        elif index == 45:
            session.runCmdSimple('service nexposeconsole start')
            session.runCmdSimple('firefox https://localhost:3780', 'Starting Nexpose scanner')
        elif index == 46:
            session.runCmdSimple('openvas-start')
            session.runCmdSimple('firefox https://localhost:9392', 'Starting OpenVAS scanner')

    def runTcpdump(self, index):
        target = session.getRemoteHost()
        dir = session.getIntelDir()
        cmd = 'tcpdump -i eth0 '
        file = ''
        filter = ''
        title = ''

        if index == 60:
            file = dir + '/tcpdump_all.pcap '
            title = 'tcpdump All'
        elif index == 61:
            file = dir + '/tcpdump_http.pcap '
            filter = filter + ' -Y http.request '
            title = 'tcpdump HTTP'
        elif index == 62:
            file = dir + '/tcpdump_http.pcap '
            filter = filter + ' -f "src port 53" -n -T fields -e dns.qry.name -e dns.resp.addr '
            title = 'tcpdump DNS'

        cmd += ' -w ' + file + ' ' + filter
        session.runThreadedCmd(cmd, cmd)

        return

    def runLynis(self):
        index = session.toolManager.findToolIndex('Lynis (LOCAL)', toolCategory = 2)
        if index > 0:
            session.toolManager.run(index, toolCategory = 2)
        else:
            self.prompt('Unable to find tool')
        return

    def runPrivesc(self):
        os.system('chmod +x ../Scripts/unix-privesc-check.sh')
        session.runCmdSimple('../Scripts/unix-privesc-check.sh standard > ' + session.getIntelDir() + '/unix-privesc-check.out')
        
        if ParserPrivesc.parseFile(session.getIntelDir() + '/unix-privesc-check.out') == False:
            print('Error parsing output.')
        else:
            print('Output parsed and saved to session')

        self.prompt('Check: unix-privesc-check.out')
        return

    def localStandardScan(self):
        dir = session.getIntelDir()

        if platform.system() == 'Windows':
            import os.path
            if not os.path.isfile("accesschk.exe"):
                print('https://docs.microsoft.com/en-us/sysinternals/downloads/accesschk')
                print('accesschk.exe from SysInternals must be in same folder as this script... Exiting.')
                return

            import sys
            import csv
            import codecs
            import argparse

            dir = dir + '/'
            raw = dir + "IU93xy0Px.csv"
            path_list = []
            basic = dir + "basic_info.txt"
            network = dir + "network_info.txt"
            firewall = dir + "firewall_info.txt"
            tasks = dir + "task_service_info.txt"
            driver = dir + "driver_info.txt"
            service = dir + "service_info.txt"
            service_tmp1 = dir + "service_tmp1.txt"
            service_tmp2 = dir + "service_tmp2.txt"
            patches = dir + "patch_info.txt"
            fast_priv = dir + "fast_priv.txt"
            wmic_chk = dir + "wmic_check.txt"
            check = dir + "dki98kxAI.bat"

            # Basic enum
            print('Runnng Windows Basic System Information Enumeration.')
            self.file_header(basic)
            self.section_heading("Basic System Enumeration", basic)
  
            self.part_heading("System Info", basic)
            self.sys_call('systeminfo | findstr /B /C:"OS Name" /C:"OS Version"', basic)
            self.sys_call("echo --------------------------------------------------------------------", basic)
  
            self.part_heading("Hostname", basic)
            self.sys_call('hostname', basic)
            self.sys_call("echo --------------------------------------------------------------------", basic)  
  
            self.part_heading("Current User", basic)
            self.sys_call('echo %username%', basic)
            self.sys_call("echo --------------------------------------------------------------------", basic)
  
            self.part_heading("Path", basic)
            self.sys_call('echo %path%', basic)
            self.sys_call("echo --------------------------------------------------------------------", basic)
  
            self.part_heading("Users", basic)
            self.sys_call('net users', basic)
  
            self.part_heading("Administrators", basic)
            self.sys_call('net localgroup Administrators', basic)
  
            self.part_heading("RDP Users", basic)
            self.sys_call('net localgroup "Remote Desktop Users"', basic)
            self.sys_call("echo --------------------------------------------------------------------", basic)

            # Network enum
            print('Running Local Network Enumeration.')
            self.file_header(network)
            self.section_heading("Network Information", network)
  
            self.sys_call('ipconfig /all', network)
            self.sys_call("echo --------------------------------------------------------------------", network)
  
            self.part_heading("Routes", network)
            self.sys_call('route print', network)
            self.sys_call("echo --------------------------------------------------------------------", network)
  
            self.part_heading("Local Network", network)
            self.sys_call('arp -A', network)
            self.sys_call("echo --------------------------------------------------------------------", network)

            self.sys_call('netstat -ano', network)
            self.sys_call("echo --------------------------------------------------------------------", network)

            # Firewall enum
            print('Running Windows Firewall Enumeration.')
            self.file_header(firewall)
            self.section_heading("Firewall Enumeration", firewall)
  
            self.sys_call('netsh firewall show state', firewall)
            self.sys_call("echo --------------------------------------------------------------------", firewall)
  
            self.part_heading("Firewall Config", firewall)
            self.sys_call('netsh firewall show config', firewall)
            self.sys_call("echo --------------------------------------------------------------------", firewall)

            # Schedule enum
            print('Running Windows Tasks and Scheduled Process Enumeration.')
            self.file_header(tasks)
            self.section_heading("Running Tasks and Services", tasks)
  
            self.part_heading("Tasks", tasks)
            self.sys_call('schtasks /query /fo LIST /v', tasks)
            self.sys_call("echo --------------------------------------------------------------------", tasks)
  
            self.part_heading("Running Process", tasks)
            self.sys_call('tasklist /SVC', tasks)
            self.sys_call("echo --------------------------------------------------------------------", tasks)

            # Service enum
            print('Windows Service Enumeration.')
            self.file_header(service)
            self.section_heading("Service Executable Rights Enumeration", service)
            self.sys_call('echo SERVICE_CHANGE_CONFIG == Can reconfigure the service binary', service)
            self.sys_call('echo WRITE_DAC == Can reconfigure permissions to SERVICE_CHANGE_CONFIG', service)
            self.sys_call('echo WRITE_OWNER == Can become owner, reonfigure permissions', service)
            self.sys_call('echo GENERIC_WRITE == Inherits SERVICE_CHANGE_CONFIG', service)
            self.sys_call('echo GENERIC_ALL == Inherits SERVICE_CHANGE_CONFIG', service)
            self.sys_call("echo --------------------------------------------------------------------", service)
            self.sys_call("echo.", service) # blank line
            self.part_heading("Services", service)
            self.sys_call('sc queryex type= service state= all | findstr /B /C:"SERVICE_NAME"', service_tmp1)
            lines = [line.rstrip('\n') for line in open(service_tmp1)]
  
            for line in lines:
                name = line.split(' ')[1]
                name = name.strip()
                command = 'sc qc ' + name + ' | findstr /C:"BINARY_PATH_NAME"'
                self.sys_call_new(command, service_tmp2)
                path_lines = [path_line.rstrip('\n') for path_line in open(service_tmp2)]
                for path_line in path_lines:
                    try:
                        path_line = path_line.strip()
                        path = path_line.split(':')[1] + ':' + path_line.split(':')[2] 
                        path = path.strip()
                        path = path.split(' -')[0]
                        path = path.split(' /')[0]
                        path = path.strip()
                        path = self.quote_string(path)
                    except:
                        continue

            self.sys_call('sc qc ' + name, service)
            self.sys_call("echo.", service) # blank line
            self.sys_call('accesschk.exe -ucqv "' + name + '" /accepteula', service)
            self.sys_call("echo.", service) # blank line
            self.sys_call('accesschk.exe -q ' + path + ' /accepteula', service)
            self.sys_call("echo --------------------------------------------------------------------", service)

            os.remove(service_tmp1)
            os.remove(service_tmp2)
            self.sys_call("echo --------------------------------------------------------------------", service)

            # Driver enum
            print('Running Windows Driver Enumeration.')
            self.file_header(driver)
            self.section_heading("Driver Enumeration", driver)
  
            self.sys_call('DRIVERQUERY', driver)
            self.sys_call("echo --------------------------------------------------------------------", driver)

            # Patch'es enum
            print('Running Windows Patch Enumeration.')
            cal = subprocess.call('wmic qfe get Caption,Description,HotFixID,InstalledOn /format:table > ' + patches, shell=True)

            # Privilege escalation
            print('Running Fast Privilege Escalation Enumeration.')
            self.file_header(fast_priv)

            out = open(check, 'w')
            out.write('wmic service get name,displayname,pathname,startmode |findstr /i "Auto" |findstr /i /v "C:\\Windows\\\\" |findstr /i /v """\n')
            out.write('reg query HKCU\\SOFTWARE\\Policies\\Microsoft\\Windows\\Installer /v AlwaysInstallElevated\n')
            out.write('reg query HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Installer /v AlwaysInstallElevated\n')
            out.close()
    
            self.section_heading("Unquoted Service Paths and Always Installed Elevated", fast_priv)
            self.sys_call(check, fast_priv)
            self.sys_call("echo --------------------------------------------------------------------", fast_priv)
            os.remove(check)

            self.section_heading("Unattended Install Check", fast_priv)
            self.sys_call('reg query HKLM\\System\\Setup!UnattendFile', fast_priv)
            file_list = ['unattend.xml', 'sysprep.xml', 'sysprep.inf', 'autounattend.xml']
            path_list = ['c:\\', 'c:\\Windows\\Panther\\', 'c:\\Windows\\Panther\\Unattend\\', 'c:\\Windows\\System32\\', 'c:\\Windows\\System32\\sysprep\\']
            for file in file_list:
                for path in path_list:
                    if os.path.isfile(path + file):
                        self.sys_call('echo Possible Unattended Install File: ', fast_priv)
                        self.sys_call('echo ' + path + file, fast_priv)

            self.sys_call("echo.", fast_priv) # blank line

            self.section_heading("Quck Accesschk Look - Won't Work >= Win XP SP2", fast_priv)
            self.sys_call('accesschk.exe -uwcqv "Authenticated Users" * /accepteula', fast_priv)
            self.sys_call("echo.", fast_priv) # blank line

            # WMIC enum
            print('Running WMIC Check')
            self.file_header(wmic_chk)
            servicelist = "wmic service get name,pathname /format:csv > " + raw
            cal = subprocess.call(servicelist, shell=True)

            if os.path.isfile(raw) == False:
                print('Something went wrong with service enumeration.')
                return
  
            self.section_heading("Service Executable Rights Enumeration", wmic_chk)
            self.sys_call('echo SERVICE_CHANGE_CONFIG == Can reconfigure the service binary', wmic_chk)
            self.sys_call('echo WRITE_DAC == Can reconfigure permissions to SERVICE_CHANGE_CONFIG', wmic_chk)
            self.sys_call('echo WRITE_OWNER == Can become owner, reonfigure permissions', wmic_chk)
            self.sys_call('echo GENERIC_WRITE == Inherits SERVICE_CHANGE_CONFIG', wmic_chk)
            self.sys_call('echo GENERIC_ALL == Inherits SERVICE_CHANGE_CONFIG', wmic_chk)
            self.sys_call("echo --------------------------------------------------------------------", wmic_chk)
            self.sys_call("echo.", wmic_chk) # blank line
  
            f = codecs.open(raw,"rb","utf-16")
            csvreader = csv.reader(f,delimiter=',')
            csvreader.__next__()
            csvreader.__next__()
  
            for row in csvreader:
                if len(row) < 2:
                    continue
                service_name = row[1]
                raw_path = row[2]
                raw_path = raw_path.split(' -')[0]
                raw_path = raw_path.split('/')[0]
                service_path = raw_path.strip()
                if service_path == "":
                    continue
                if service_path in path_list:
                    continue
  
                path_list.append(service_path)
  
                self.sys_call('sc qc ' + service_name, wmic_chk)
                self.sys_call("echo.", wmic_chk) # blank line
                self.sys_call('accesschk.exe -ucqv "' + service_name + '" /accepteula', wmic_chk)
                self.sys_call("echo.", wmic_chk) # blank line
                self.sys_call('accesschk.exe -q "' + service_path + '" /accepteula', wmic_chk)
                self.sys_call("echo --------------------------------------------------------------------", wmic_chk)
  
            f.close()
            os.remove(raw)

        else:
            # Title / formatting
            bigline = "================================================================================================="
            smlline = "-------------------------------------------------------------------------------------------------"

            print(bigline)
            print('LINUX PRIVILEGE ESCALATION CHECKER')
            print(bigline)
            print()

            # Basic system info
            print('[*] GETTING BASIC SYSTEM INFO...\n')
            results = []
            sysInfo = {"OS":{"cmd":"cat /etc/issue","msg":"Operating System","results" : results}, 
	               "KERNEL":{"cmd":"cat /proc/version","msg":"Kernel","results" : results}, 
	               "HOSTNAME":{"cmd":"hostname", "msg":"Hostname", "results" : results} }

            sysInfo = self.execCmd(sysInfo, 'Getting basic system information')
            print(sysInfo)
            self.printResults(sysInfo, dir)

            # Networking Info
            print('[*] GETTING NETWORKING INFO...\n')

            netInfo = {"NETINFO":{"cmd":"/sbin/ifconfig -a", "msg":"Interfaces", "results":results},
	               "ROUTE":{"cmd":"route", "msg":"Route", "results":results},
	               "NETSTAT":{"cmd":"netstat -antup | grep -v 'TIME_WAIT'", "msg":"Netstat", "results":results} }

            netInfo = self.execCmd(netInfo, 'Getting networking information')
            self.printResults(netInfo, dir)

            # File System Info
            print('[*] GETTING FILESYSTEM INFO...\n')

            driveInfo = {"MOUNT":{"cmd":"mount","msg":"Mount results", "results":results},
	                 "FSTAB":{"cmd":"cat /etc/fstab 2>/dev/null", "msg":"fstab entries", "results":results} }

            driveInfo = self.execCmd(driveInfo, 'Getting filesystem information')
            self.printResults(driveInfo, dir)

            # Scheduled Cron Jobs
            cronInfo = {"CRON":{"cmd":"ls -la /etc/cron* 2>/dev/null", "msg":"Scheduled cron jobs", "results":results},
	                "CRONW": {"cmd":"ls -aRl /etc/cron* 2>/dev/null | awk '$1 ~ /w.$/' 2>/dev/null", "msg":"Writable cron dirs", "results":results} }

            cronInfo = self.execCmd(cronInfo, 'Gathering information on Cron jobs')
            self.printResults(cronInfo, dir)

            # User Info
            print('\n[*] ENUMERATING USER AND ENVIRONMENTAL INFO...\n')

            userInfo = {"WHOAMI":{"cmd":"whoami", "msg":"Current User", "results":results},
	                "ID":{"cmd":"id","msg":"Current User ID", "results":results},
	                "ALLUSERS":{"cmd":"cat /etc/passwd", "msg":"All users", "results":results},
	                "SUPUSERS":{"cmd":"grep -v -E '^#' /etc/passwd | awk -F: '$3 == 0{print $1}'", "msg":"Super Users Found:", "results":results},
	                "HISTORY":{"cmd":"ls -la ~/.*_history; ls -la /root/.*_history 2>/dev/null", "msg":"Root and current user history (depends on privs)", "results":results},
	                "ENV":{"cmd":"env 2>/dev/null | grep -v 'LS_COLORS'", "msg":"Environment", "results":results},
	                "SUDOERS":{"cmd":"cat /etc/sudoers 2>/dev/null | grep -v '#' 2>/dev/null", "msg":"Sudoers (privileged)", "results":results},
	                "LOGGEDIN":{"cmd":"w 2>/dev/null", "msg":"Logged in User Activity", "results":results} }

            userInfo = self.execCmd(userInfo, 'Enumerating user and evniroment information.')
            self.printResults(userInfo, dir)

            try:
                if "root" in userInfo["ID"]["results"][0]:
                    print('[!] ARE YOU SURE YOU\'RE NOT ROOT ALREADY?\n')
            except:
                pass

            # File/Directory Privs
            print('[*] ENUMERATING FILE AND DIRECTORY PERMISSIONS/CONTENTS...\n')

            fdPerms = {"WWDIRSROOT":{"cmd":"find / \( -wholename '/home/homedir*' -prune \) -o \( -type d -perm -0002 \) -exec ls -ld '{}' ';' 2>/dev/null | grep root", "msg":"World Writeable Directories for User/Group 'Root'", "results":results},
	               "WWDIRS":{"cmd":"find / \( -wholename '/home/homedir*' -prune \) -o \( -type d -perm -0002 \) -exec ls -ld '{}' ';' 2>/dev/null | grep -v root", "msg":"World Writeable Directories for Users other than Root", "results":results},
	               "WWFILES":{"cmd":"find / \( -wholename '/home/homedir/*' -prune -o -wholename '/proc/*' -prune \) -o \( -type f -perm -0002 \) -exec ls -l '{}' ';' 2>/dev/null", "msg":"World Writable Files", "results":results},
	               "SUID":{"cmd":"find / \( -perm -2000 -o -perm -4000 \) -exec ls -ld {} \; 2>/dev/null", "msg":"SUID/SGID Files and Directories", "results":results},
	               "ROOTHOME":{"cmd":"ls -ahlR /root 2>/dev/null", "msg":"Checking if root's home folder is accessible", "results":results} }

            fdPerms = self.execCmd(fdPerms, 'Enumerating file and directory permissions/content') 
            self.printResults(fdPerms, dir)

            pwdFiles = {"LOGPWDS":{"cmd":"find /var/log -name '*.log' 2>/dev/null | xargs -l10 egrep 'pwd|password' 2>/dev/null", "msg":"Logs containing keyword 'password'", "results":results},
	                "CONFPWDS":{"cmd":"find /etc -name '*.c*' 2>/dev/null | xargs -l10 egrep 'pwd|password' 2>/dev/null", "msg":"Config files containing keyword 'password'", "results":results},
	                "SHADOW":{"cmd":"cat /etc/shadow 2>/dev/null", "msg":"Shadow File (Privileged)", "results":results} }

            pwdFiles = self.execCmd(pwdFiles, 'Gathering logs')
            self.printResults(pwdFiles, dir)

            # Processes and Applications
            print('[*] ENUMERATING PROCESSES AND APPLICATIONS...\n')

            if "debian" in sysInfo["KERNEL"]["results"][0] or "ubuntu" in sysInfo["KERNEL"]["results"][0]:
                getPkgs = "dpkg -l | awk '{$1=$4=\"\"; print $0}'" # debian
            else:
                getPkgs = "rpm -qa | sort -u" # RH/other

            getAppProc = {"PROCS":{"cmd":"ps aux | awk '{print $1,$2,$9,$10,$11}'", "msg":"Current processes", "results":results},
                          "PKGS":{"cmd":getPkgs, "msg":"Installed Packages", "results":results} }

            getAppProc = self.execCmd(getAppProc, 'Enumerating processes and programs')
            self.printResults(getAppProc, dir) # comment to reduce output

            otherApps = { "SUDO":{"cmd":"sudo -V | grep version 2>/dev/null", "msg":"Sudo Version (Check out http://www.exploit-db.com/search/?action=search&filter_page=1&filter_description=sudo)", "results":results},
	                  "APACHE":{"cmd":"apache2 -v; apache2ctl -M; httpd -v; apachectl -l 2>/dev/null", "msg":"Apache Version and Modules", "results":results},
	                  "APACHECONF":{"cmd":"cat /etc/apache2/apache2.conf 2>/dev/null", "msg":"Apache Config File", "results":results} }

            otherApps = self.execCmd(otherApps, 'Listing sudo permissions')
            self.printResults(otherApps, dir)

            print('[*] IDENTIFYING PROCESSES AND PACKAGES RUNNING AS ROOT OR OTHER SUPERUSER...\n')

            # find the package information for the processes currently running
            # under root or another super user
            procs = getAppProc["PROCS"]["results"]
            pkgs = getAppProc["PKGS"]["results"]
            supusers = userInfo["SUPUSERS"]["results"]
            procdict = {} # dictionary to hold the processes running as super users
  
            for proc in procs: # loop through each process
                relatedpkgs = [] # list to hold the packages related to a process
                try:
                    for user in supusers: # loop through the known super users
                        if (user != "") and (user in proc): # if the process is being run by a super user
                            procname = proc.split(" ")[4] # grab the process name
                        if "/" in procname:
                            splitname = procname.split("/")
                            procname = splitname[len(splitname) - 1]
                            for pkg in pkgs: # loop through the packages
                                if not len(procname) < 3: # name too short to get reliable package results
                                    if procname in pkg:
                                        if procname in procdict: 
                                            relatedpkgs = procdict[proc] # if already in the dict, grab its pkg list
                                        if pkg not in relatedpkgs:
                                            relatedpkgs.append(pkg) # add pkg to the list
                                procdict[proc] = relatedpkgs # add any found related packages to the process dictionary entry
                except:
                    pass

            for key in procdict:
                print("    " + key) # print the process name
                try:
                    if not procdict[key][0] == "": # only print the rest if related packages were found
                        print("        Possible Related Packages: ")
                        for entry in procdict[key]: 
                            print("            " + entry) # print each related package
                except:
                    pass

            for key in procdict:
                print("    " + key) # print the process name
                try:
                    if not procdict[key][0] == "": # only print the rest if related packages were found
                        print("        Possible Related Packages: ") 
                        for entry in procdict[key]: 
                            print("            " + entry) # print each related package
                except:
                    pass

            # EXPLOIT ENUMERATION

            # First discover the avaialable tools
            print()
            print("[*] ENUMERATING INSTALLED LANGUAGES/TOOLS FOR SPLOIT BUILDING...\n")

            devTools = {"TOOLS":{"cmd":"which awk perl python ruby gcc cc vi vim nmap find netcat nc wget tftp ftp 2>/dev/null", "msg":"Installed Tools", "results":results}}
            devTools = self.execCmd(devTools, 'Enumerating installed tools')
            self.printResults(devTools, dir)

            print("[+] Related Shell Escape Sequences...\n")
            escapeCmd = {"vi":[":!bash", ":set shell=/bin/bash:shell"], "awk":["awk 'BEGIN {system(\"/bin/bash\")}'"], "perl":["perl -e 'exec \"/bin/bash\";'"], "find":["find / -exec /usr/bin/awk 'BEGIN {system(\"/bin/bash\")}' \\;"], "nmap":["--interactive"]}
            for cmd in escapeCmd:
                for result in devTools["TOOLS"]["results"]:
                    if cmd in result:
                        for item in escapeCmd[cmd]:
                            print("    " + cmd + "-->\t" + item)
            print()
            print("[*] FINDING RELEVENT PRIVILEGE ESCALATION EXPLOITS...\n")

            # Now check for relevant exploits (note: this list should be
            # updated over time; source: Exploit-DB)
            # sploit format = sploit name : {minversion, maxversion,
            # exploitdb#, language, {keywords for applicability}} -- current
            # keywords are 'kernel', 'proc', 'pkg' (unused), and 'os'
            sploits = { "2.2.x-2.4.x ptrace kmod local exploit":{"minver":"2.2", "maxver":"2.4.99", "exploitdb":"3", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "< 2.4.20 Module Loader Local Root Exploit":{"minver":"0", "maxver":"2.4.20", "exploitdb":"12", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.4.22 "'do_brk()'" local Root Exploit (PoC)":{"minver":"2.4.22", "maxver":"2.4.22", "exploitdb":"129", "lang":"asm", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "<= 2.4.22 (do_brk) Local Root Exploit (working)":{"minver":"0", "maxver":"2.4.22", "exploitdb":"131", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.4.x mremap() bound checking Root Exploit":{"minver":"2.4", "maxver":"2.4.99", "exploitdb":"145", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "<= 2.4.29-rc2 uselib() Privilege Elevation":{"minver":"0", "maxver":"2.4.29", "exploitdb":"744", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.4 uselib() Privilege Elevation Exploit":{"minver":"2.4", "maxver":"2.4", "exploitdb":"778", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.4.x / 2.6.x uselib() Local Privilege Escalation Exploit":{"minver":"2.4", "maxver":"2.6.99", "exploitdb":"895", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.4/2.6 bluez Local Root Privilege Escalation Exploit (update)":{"minver":"2.4", "maxver":"2.6.99", "exploitdb":"926", "lang":"c", "keywords":{"loc":["proc","pkg"], "val":"bluez"}},
		            "<= 2.6.11 (CPL 0) Local Root Exploit (k-rad3.c)":{"minver":"0", "maxver":"2.6.11", "exploitdb":"1397", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "MySQL 4.x/5.0 User-Defined Function Local Privilege Escalation Exploit":{"minver":"0", "maxver":"99", "exploitdb":"1518", "lang":"c", "keywords":{"loc":["proc","pkg"], "val":"mysql"}},
		            "2.6.13 <= 2.6.17.4 sys_prctl() Local Root Exploit":{"minver":"2.6.13", "maxver":"2.6.17.4", "exploitdb":"2004", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.6.13 <= 2.6.17.4 sys_prctl() Local Root Exploit (2)":{"minver":"2.6.13", "maxver":"2.6.17.4", "exploitdb":"2005", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.6.13 <= 2.6.17.4 sys_prctl() Local Root Exploit (3)":{"minver":"2.6.13", "maxver":"2.6.17.4", "exploitdb":"2006", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.6.13 <= 2.6.17.4 sys_prctl() Local Root Exploit (4)":{"minver":"2.6.13", "maxver":"2.6.17.4", "exploitdb":"2011", "lang":"sh", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "<= 2.6.17.4 (proc) Local Root Exploit":{"minver":"0", "maxver":"2.6.17.4", "exploitdb":"2013", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.6.13 <= 2.6.17.4 prctl() Local Root Exploit (logrotate)":{"minver":"2.6.13", "maxver":"2.6.17.4", "exploitdb":"2031", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "Ubuntu/Debian Apache 1.3.33/1.3.34 (CGI TTY) Local Root Exploit":{"minver":"4.10", "maxver":"7.04", "exploitdb":"3384", "lang":"c", "keywords":{"loc":["os"], "val":"debian"}},
		            "Linux/Kernel 2.4/2.6 x86-64 System Call Emulation Exploit":{"minver":"2.4", "maxver":"2.6", "exploitdb":"4460", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "< 2.6.11.5 BLUETOOTH Stack Local Root Exploit":{"minver":"0", "maxver":"2.6.11.5", "exploitdb":"4756", "lang":"c", "keywords":{"loc":["proc","pkg"], "val":"bluetooth"}},
		            "2.6.17 - 2.6.24.1 vmsplice Local Root Exploit":{"minver":"2.6.17", "maxver":"2.6.24.1", "exploitdb":"5092", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.6.23 - 2.6.24 vmsplice Local Root Exploit":{"minver":"2.6.23", "maxver":"2.6.24", "exploitdb":"5093", "lang":"c", "keywords":{"loc":["os"], "val":"debian"}},
		            "Debian OpenSSL Predictable PRNG Bruteforce SSH Exploit":{"minver":"0", "maxver":"99", "exploitdb":"5720", "lang":"python", "keywords":{"loc":["os"], "val":"debian"}},
		            "Linux Kernel < 2.6.22 ftruncate()/open() Local Exploit":{"minver":"0", "maxver":"2.6.22", "exploitdb":"6851", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "< 2.6.29 exit_notify() Local Privilege Escalation Exploit":{"minver":"0", "maxver":"2.6.29", "exploitdb":"8369", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.6 UDEV Local Privilege Escalation Exploit":{"minver":"2.6", "maxver":"2.6.99", "exploitdb":"8478", "lang":"c", "keywords":{"loc":["proc","pkg"], "val":"udev"}},
		            "2.6 UDEV < 141 Local Privilege Escalation Exploit":{"minver":"2.6", "maxver":"2.6.99", "exploitdb":"8572", "lang":"c", "keywords":{"loc":["proc","pkg"], "val":"udev"}},
		            "2.6.x ptrace_attach Local Privilege Escalation Exploit":{"minver":"2.6", "maxver":"2.6.99", "exploitdb":"8673", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.6.29 ptrace_attach() Local Root Race Condition Exploit":{"minver":"2.6.29", "maxver":"2.6.29", "exploitdb":"8678", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "Linux Kernel <=2.6.28.3 set_selection() UTF-8 Off By One Local Exploit":{"minver":"0", "maxver":"2.6.28.3", "exploitdb":"9083", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "Test Kernel Local Root Exploit 0day":{"minver":"2.6.18", "maxver":"2.6.30", "exploitdb":"9191", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "PulseAudio (setuid) Priv. Escalation Exploit (ubu/9.04)(slack/12.2.0)":{"minver":"2.6.9", "maxver":"2.6.30", "exploitdb":"9208", "lang":"c", "keywords":{"loc":["pkg"], "val":"pulse"}},
		            "2.x sock_sendpage() Local Ring0 Root Exploit":{"minver":"2", "maxver":"2.99", "exploitdb":"9435", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.x sock_sendpage() Local Root Exploit 2":{"minver":"2", "maxver":"2.99", "exploitdb":"9436", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.4/2.6 sock_sendpage() ring0 Root Exploit (simple ver)":{"minver":"2.4", "maxver":"2.6.99", "exploitdb":"9479", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.6 < 2.6.19 (32bit) ip_append_data() ring0 Root Exploit":{"minver":"2.6", "maxver":"2.6.19", "exploitdb":"9542", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.4/2.6 sock_sendpage() Local Root Exploit (ppc)":{"minver":"2.4", "maxver":"2.6.99", "exploitdb":"9545", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "< 2.6.19 udp_sendmsg Local Root Exploit (x86/x64)":{"minver":"0", "maxver":"2.6.19", "exploitdb":"9574", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "< 2.6.19 udp_sendmsg Local Root Exploit":{"minver":"0", "maxver":"2.6.19", "exploitdb":"9575", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.4/2.6 sock_sendpage() Local Root Exploit [2]":{"minver":"2.4", "maxver":"2.6.99", "exploitdb":"9598", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.4/2.6 sock_sendpage() Local Root Exploit [3]":{"minver":"2.4", "maxver":"2.6.99", "exploitdb":"9641", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.4.1-2.4.37 and 2.6.1-2.6.32-rc5 Pipe.c Privelege Escalation":{"minver":"2.4.1", "maxver":"2.6.32", "exploitdb":"9844", "lang":"python", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "'pipe.c' Local Privilege Escalation Vulnerability":{"minver":"2.4.1", "maxver":"2.6.32", "exploitdb":"10018", "lang":"sh", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.6.18-20 2009 Local Root Exploit":{"minver":"2.6.18", "maxver":"2.6.20", "exploitdb":"10613", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "Apache Spamassassin Milter Plugin Remote Root Command Execution":{"minver":"0", "maxver":"99", "exploitdb":"11662", "lang":"sh", "keywords":{"loc":["proc"], "val":"spamass-milter"}},
		            "<= 2.6.34-rc3 ReiserFS xattr Privilege Escalation":{"minver":"0", "maxver":"2.6.34", "exploitdb":"12130", "lang":"python", "keywords":{"loc":["mnt"], "val":"reiser"}},
		            "Ubuntu PAM MOTD local root":{"minver":"7", "maxver":"10.04", "exploitdb":"14339", "lang":"sh", "keywords":{"loc":["os"], "val":"ubuntu"}},
		            "< 2.6.36-rc1 CAN BCM Privilege Escalation Exploit":{"minver":"0", "maxver":"2.6.36", "exploitdb":"14814", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "Kernel ia32syscall Emulation Privilege Escalation":{"minver":"0", "maxver":"99", "exploitdb":"15023", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "Linux RDS Protocol Local Privilege Escalation":{"minver":"0", "maxver":"2.6.36", "exploitdb":"15285", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "<= 2.6.37 Local Privilege Escalation":{"minver":"0", "maxver":"2.6.37", "exploitdb":"15704", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "< 2.6.37-rc2 ACPI custom_method Privilege Escalation":{"minver":"0", "maxver":"2.6.37", "exploitdb":"15774", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "CAP_SYS_ADMIN to root Exploit":{"minver":"0", "maxver":"99", "exploitdb":"15916", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "CAP_SYS_ADMIN to Root Exploit 2 (32 and 64-bit)":{"minver":"0", "maxver":"99", "exploitdb":"15944", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "< 2.6.36.2 Econet Privilege Escalation Exploit":{"minver":"0", "maxver":"2.6.36.2", "exploitdb":"17787", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "Sendpage Local Privilege Escalation":{"minver":"0", "maxver":"99", "exploitdb":"19933", "lang":"ruby", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.4.18/19 Privileged File Descriptor Resource Exhaustion Vulnerability":{"minver":"2.4.18", "maxver":"2.4.19", "exploitdb":"21598", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.2.x/2.4.x Privileged Process Hijacking Vulnerability (1)":{"minver":"2.2", "maxver":"2.4.99", "exploitdb":"22362", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "2.2.x/2.4.x Privileged Process Hijacking Vulnerability (2)":{"minver":"2.2", "maxver":"2.4.99", "exploitdb":"22363", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "Samba 2.2.8 Share Local Privilege Elevation Vulnerability":{"minver":"2.2.8", "maxver":"2.2.8", "exploitdb":"23674", "lang":"c", "keywords":{"loc":["proc","pkg"], "val":"samba"}},
		            "open-time Capability file_ns_capable() - Privilege Escalation Vulnerability":{"minver":"0", "maxver":"99", "exploitdb":"25307", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},
		            "open-time Capability file_ns_capable() Privilege Escalation":{"minver":"0", "maxver":"99", "exploitdb":"25450", "lang":"c", "keywords":{"loc":["kernel"], "val":"kernel"}},}

            # variable declaration
            os = sysInfo["OS"]["results"][0]
            version = sysInfo["KERNEL"]["results"][0].split(" ")[2].split("-")[0]
            langs = devTools["TOOLS"]["results"]
            procs = getAppProc["PROCS"]["results"]
            kernel = str(sysInfo["KERNEL"]["results"][0])
            mount = driveInfo["MOUNT"]["results"]
            #pkgs = getAppProc["PKGS"]["results"] # currently not using
            #packages for sploit appicability but my in future

            # lists to hold ranked, applicable sploits
            # note: this is a best-effort, basic ranking designed to help in
            # prioritizing priv escalation exploit checks
            # all applicable exploits should be checked and this function could
            # probably use some improvement
            avgprob = []
            highprob = []

            for sploit in sploits:
                lang = 0 # use to rank applicability of sploits
                keyword = sploits[sploit]["keywords"]["val"]
                sploitout = sploit + " || " + "http://www.exploit-db.com/exploits/" + sploits[sploit]["exploitdb"] + " || " + "Language=" + sploits[sploit]["lang"]
                # first check for kernell applicability
                if (version >= sploits[sploit]["minver"]) and (version <= sploits[sploit]["maxver"]):
	                # next check language applicability
                    if (sploits[sploit]["lang"] == "c") and (("gcc" in str(langs)) or ("cc" in str(langs))):
                        lang = 1 # language found, increase applicability score
                    elif sploits[sploit]["lang"] == "sh": 
                        lang = 1 # language found, increase applicability score
                    elif (sploits[sploit]["lang"] in str(langs)):
                        lang = 1 # language found, increase applicability score
                    
                    if lang == 0:
                        sploitout = sploitout + "**" # added mark if language not detected on system

                # next check keyword matches to determine if some sploits have
                # a higher probability of success
                for loc in sploits[sploit]["keywords"]["loc"]:
                    if loc == "proc":
                        for proc in procs:
                            if keyword in proc:
                                highprob.append(sploitout) # if sploit is associated with a running process consider it a higher
                                                           # probability/applicability
                                break
                        break
                    elif loc == "os":
                        if (keyword in os) or (keyword in kernel):
                            highprob.append(sploitout) # if sploit is specifically applicable to this OS consider it a higher
                                                       # probability/applicability
                            break  
                    elif loc == "mnt":
                        if keyword in mount:
                            highprob.append(sploitout) # if sploit is specifically applicable to a mounted file system consider it a
                                                       # higher
                                                                                                             # probability/applicability
                            break
                    else:
                        avgprob.append(sploitout) # otherwise, consider average probability/applicability based only on kernel
                                                  # version

            print("    Note: Exploits relying on a compile/scripting language not detected on this system are marked with a '**' but should still be tested!")
            print

            print("    The following exploits are ranked higher in probability of success because this script detected a related running process, OS, or mounted file system")
            for exploit in highprob:
                print("    - " + exploit)
            print

            print("    The following exploits are applicable to this kernel version and should be investigated as well")
            for exploit in avgprob:
                print("    - " + exploit)

            print()	
            print(bigline)


        print('Done')

    def execCmd(self, cmdDict, comments = ''):
        for item in cmdDict:
            cmd = cmdDict[item]["cmd"]
            session.addReportCmd(cmd, comments)

            out, error = subprocess.Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True).communicate()
            results = out.decode("utf-8").split('\n')
            cmdDict[item]["results"] = results
        return cmdDict

    def printResults(self, cmdDict, dir):
        f = None
        try:
            f = open(dir + "/privcheckout.txt", "a")
            for item in cmdDict:
                msg = cmdDict[item]["msg"]
                print('[+] ' + msg)
                f.write('[+] ' + msg + '\n')

                results = cmdDict[item]["results"]
                for result in results:
                    if len(result.strip()) > 0:
                        print('    ' + result.strip())
                        f.write('    ' + result.strip() + '\n')
            print('')
            f.write('\n')
        except:
            pass
        finally:
            f.close()

        return

    def quote_string(self, input):
        if input[0] != '"':
            input = '"' + input
        length = len(input)
        if input[length - 1] != '"':
            input = input + '"'
        return input

    def part_heading(self, title, file):
        self.sys_call("echo " + title + ":", file)

    def section_heading(self, title, file):
        border = '+' * (len(title) + 4)
        self.sys_call("echo " + border, file)
        self.sys_call("echo + " + title + " +", file)
        self.sys_call("echo " + border, file)
        self.sys_call("echo.", file)

    def file_header(self, file):
        cal = subprocess.call("echo Windows Local Enumeration > " + file, shell=True)
        self.sys_call("echo =====================================", file)
        self.sys_call("echo.", file)

    def sys_call_new(self, arg, file):
        cal = subprocess.call(arg + ' > ' + file, shell=True)
        session.addReportCmd(arg)

    def sys_call(self, arg, file):
        cal = subprocess.call(arg + ' >> ' + file, shell=True)
        if arg == 'echo --------------------------------------------------------------------' or \
            arg == 'echo.' or \
            arg == 'echo =====================================' or \
            arg.startswith('echo +'):
            pass
        else:
            session.addReportCmd(arg)


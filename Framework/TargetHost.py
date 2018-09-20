
import Session

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

        return ret

    def getIp(self):
        return self._Ip

    def setIp(self, ip):
        self._Ip = ip

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

    def getServiceByPort(self, port):
        try:
            for service in self._services:
                if str(service.getPort()) == str(port):
                    return service
        except Exception as e:
            print(e)

        return None;

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
            print('** OS: ' + self._Os + ' **', file = f)
            print('** IP: ' + self._Ip + ' **', file = f)

            print('## Services', file = f)
            print('| Service Name | Version | Status | Protocol | Port |', file = f)
            print('| - | - | - | - | - |', file = f)

            for s in self._services:
                print('| ' + s._name + ' | ' + s._version + ' | ' + s._status + ' | ' + s._protocol + ' | ' + s._port + ' |', file = f)
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
                if service.getName().lower().find('apache') != -1 or \
                    service.getName().lower().find('iis') != -1 or \
                    service.getName().lower().find('http') != -1:
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasMysql(self):
        try:
            for service in self._services:
                if service.getName().lower().find('mysql') != -1:
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasSmd(self):
        try:
            for service in self._services:
                if service.getName().lower().find('netbios') != -1:
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasAcarsd(self):
        # ACARS decoder
        try:
            for service in self._services:
                if service.getPort() == '2202':
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasAfp(self):
        # Apple Filing Protocol
        try:
            for service in self._services:
                if service.getPort() == '548':
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasAjp(self):
        # Apache JServ Protocol 
        try:
            for service in self._services:
                if service.getPort() == '8009':
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasAllseeingeye(self):
        # Allseeingeye game service
        try:
            for service in self._services:
                if 'allseeingeye' in service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasAmqp(self):
        # advanced message queuing protocol
        try:
            for service in self._services:
                if 'amqp' in service.getName() or service.getPort() == '5672':
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasCassandra(self):
        # Cassandra database
        try:
            for service in self._services:
                if 'cassandra' in service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasCics(self):
        # CICS for IBM mainframes
        try:
            for service in self._services:
                if 'tn3270' in service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasClamAv(self):
        # Clam AV server
        try:
            for service in self._services:
                if 'clam' == service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasCoap(self):
        # COAP endpoint
        try:
            for service in self._services:
                if 'coap' == service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasCvs(self):
        # CVS server
        try:
            for service in self._services:
                if 'cvspserver' == service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasDb2(self):
        # IBM DB2 server
        try:
            for service in self._services:
                if 'ibm-db2' == service.getName() or service.getPort() == '523':
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasDeluge(self):
        try:
            for service in self._services:
                if 'deluge' == service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasDistccd(self):
        # distccd
        try:
            for service in self._services:
                if 'distccd' == service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasLotusNotesUser(self):
        # IBM Lotus Domino user
        try:
            for service in self._services:
                if 'lotusnotes' == service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasLotusNotesUser(self):
        # IBM Lotus Domino console
        try:
            for service in self._services:
                if '2050' == service.getPort():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasIphoto(self):
        # IPhoto (dpap)
        try:
            for service in self._services:
                if 'iphoto' == service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasDrda(self):
        # DRDA protocol
        try:
            for service in self._services:
                if 'drda' == service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasEtherNetIp(self):
        # EtherNet/IP
        try:
            for service in self._services:
                if '44818' == service.getPort():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFinger(self):
        # Finger
        try:
            for service in self._services:
                if 'finger' == service.getPort():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFume(self):
        # Fume HTTP server
        try:
            for service in self._services:
                if 'fume' in service.getName() or '35871' == service.getPort():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFox(self):
        # Niagara Fox
        try:
            for service in self._services:
                if 'niagara' in service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFreelancer(self):
        # Freelancer game server
        try:
            for service in self._services:
                if 'freelancer' in service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFtp(self):
        try:
            for service in self._services:
                if '21' == service.getPort():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFtps(self):
        try:
            for service in self._services:
                if '990' == service.getPort():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasHddTemp(self):
        try:
            for service in self._services:
                if 'hddtemp' == service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasFtps(self):
        try:
            for service in self._services:
                if '990' == service.getPort():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    def hasVlcStream(self):
        # VLC streaming service
        try:
            for service in self._services:
                if 'vlcstreamer' in service.getName():
                    return service.getPort()
        except Exception as e:
            print(e)

        return '-1'

    #endregion

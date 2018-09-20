
import os.path
import logging
from libnmap.parser import NmapParser

import Utility
from Session import *
import TargetHost
import Tool

class ParserBase:
    def __init__(self):
        return

    def parseFile(self, fileName):
        pass

    def parseToolOutput(self, tool):
        pass
        
    def getToolName(self):
        return self._name

class ParserManager():
    def __init__(self):
        self._parsers = []
        self._parsers.append(ParserDirb())
        self._parsers.append(ParserNmap())
        self._parsers.append(ParserPrivesc())
        self._parsers.append(ParserGobuster())
        self._parsers.append(ParserSearchSploit())
        self._parsers.append(ParserSearchSploitNmap())
        return
        
    def parseOutput(self, parserName, filename):
        for parser in self._parsers:
            if parserName == parser._name:
                parser.parseFile(filename)
                
    def parseTool(self, tool):
        filename = tool.getOutputFileName()
        self.parseOutput(tool._parserName, filename)
        
class ParserDirb(ParserBase):
    def __init__(self):
        self._name = 'dirb'
        return super().__init__()

    def parseFile(self, fileName):
        try:
            if os.path.exists(fileName) == False:
                return False

            directoryFound = '==> DIRECTORY: '
            fileFound = '+ '
            statusCode = '(CODE:2'

            with open(fileName, 'r') as outputFile:
                for line in outputFile:
                    if directoryFound in line:
                        session.targetHost.addHttpDirectory(line.replace(directoryFound, ''))
                    elif fileFound in line and statusCode in line:
                        line = line.replace(fileFound, '')
                        arry = line.split(' ')
                        if len(arry) > 0:
                            session.targetHost.addHttpFile(arry[0])

        except Exception as e:
            logging.exception(e)
            return False

        return True

    def parseToolOutput(self, tool):
        try:
            fileName = tool.getOutputFileName()
            self.parseFile(fileName)
        except Exception as e:
            logging.exception(e)
            return False

        return True

class ParserNmap(ParserBase):
    def __init__(self):
        self._name = 'nmap'
        return super().__init__()

    def parseFile(self, fileName):
        try:
            if os.path.exists(fileName) == False:
                return False

            nmap_report = NmapParser.parse_fromfile(fileName)
            tartgetHost = None
    
            for host in nmap_report.hosts:
                print(host.address)
                session.targetHost.setIp(host.address)

                for s in host.services:
                    print("Service: {0}/{1}\t{2}\t{3}".format(s.port, s.protocol, s.state, s.service))

                    version = ''
                    product = s.service
                    for cpe in s.cpelist:
                        print("CPE: {0}".format(cpe.get_product()))
                        version = cpe.get_version()
                        
                        if len(cpe.get_product()) > 0:
                            product = product + ', ' + cpe.get_product()

                    session.targetHost.addService(s.port, s.protocol, s.state, product, version)

                if host.os_fingerprinted:
                    print("OS Fingerprints")
                    for osm in host.os.osmatches:
                        print("Found Match:{0} ({1}%)".format(osm.name, osm.accuracy))

                        for cpe in osm.get_cpe():
                            print("\t    CPE: {0}".format(cpe))

            session.save()
            session.runCmdSimple('xsltproc ' + fileName + ' -o ' + session.getReportDir() + '/' + fileName.replace('.xml') + '.html');

        except Exception as e:
            logging.exception(e)

        return False

    def parseToolOutput(self, tool):
        try:
            fileName = tool.getOutputFileName()
            self.parseFile(fileName)
        except Exception as e:
            logging.exception(e)
            return False

        return True

class ParserPrivesc(ParserBase):
    def __init__(self):
        self._name = 'unix-privesc-check'
        return super().__init__()

    def parseFile(self, fileName):
        try:
            if os.path.exists(fileName) == False:
                return False

            with open(fileName, 'r') as outputFile:
                warningCount = 0
                for line in outputFile:
                    if 'WARNING' in line:
                        warningCount += 1
                        if warningCount > 1:
                            session.targetHost.addNotes(line)

            session.save()

        except Exception as e:
            logging.exception(e)

        return False

    def parseToolOutput(self, tool):
        return self.parseFile(session.getIntelDir() + '/unix-privesc-check.out')

class ParserGobuster(ParserBase):
    def __init__(self):
        self._name = 'Gobuster'
        return super().__init__()

    def parseFile(self, fileName):
        try:
            if os.path.exists(fileName) == False:
                return False

            with open(fileName, 'r') as outputFile:
                for line in outputFile:
                    if 'http://' in line or 'https://' in line:
                        dirStr = line.split('(Status')
                        if dirStr != None:
                            session.targetHost.addHttpDir(dirStr[0])

            session.save()

        except Exception as e:
            logging.exception(e)

        return False

    def parseToolOutput(self, tool):
        try:
            fileName = tool.getOutputFileName()
            self.parseFile(fileName)
        except Exception as e:
            logging.exception(e)
            return False

        return True

class ParserSearchSploit(ParserBase):
    def __init__(self):
        self._name = 'SearchSploit'
        return super().__init__()

    def parseFile(self, fileName):
        import json
        import platform
        import shutil

        data = None
        with open(fileName) as f:
            data = json.load(f)

        exploitCount = 0
        service = data['SEARCH']
        for obj in data['RESULTS_EXPLOIT']:
            name = obj['Title']
            id = obj['EDB-ID']
            date = obj['Date']
            type = obj['Type']
            platform = obj['Platform']
            file = obj['Path']
            
            # Don't save DOS attacks
            if type != 'dos':
                session.attackManager.addAttack(Attack.Attack(name, file, '', service, id, date, type, platform))
                        
            if not os.path.exists(session.getExploitDir() + '/PossibleAttempts'):
                os.makedirs(session.getExploitDir()+ '/PossibleAttempts')
                        
            if not os.path.exists(session.getExploitDir() + '/PossibleAttempts/' + service):
                os.makedirs(session.getExploitDir() + '/PossibleAttempts/' + service)
                            
            shutil.copy(file, session.getExploitDir() + '/PossibleAttempts/' + service + '/' + os.path.basename(file))
            exploitCount += 1
                        
        print('Possible exploits found and saved: ' + str(exploitCount))

        return True

    def parseToolOutput(self, tool):
        try:
            fileName = tool.getOutputFileName()
            self.parseFile(fileName)
        except Exception as e:
            logging.exception(e)
            return False

        return True
        
class ParserSearchSploitNmap(ParserBase):
    def __init__(self):
        self._name = 'SearchSploitNmap'
        return super().__init__()

    def parseFile(self, fileName):
        import json
        import platform
        import shutil

        infile = open(fileName,'r').readlines()
        formattedFile = fileName + '_formatted.txt'

        # Possibly windows and linux parses the json differently, because I'm getting errors
        if platform.system() == 'Windows':
            with open(formattedFile,'w') as outfile:
                for index,line in enumerate(infile):
                    if index == 0 or index == 1:
                        continue
                    elif index == 2:
                        outfile.write('[')
                    elif line == '}\n':
                        line = '},\n'
                        outfile.write(line)
                    else:
                        outfile.write(line)

                outfile.write(']')
        else:
            # Find how many objects there are
            count = 0
            with open(formattedFile,'w') as outfile:
                for index,line in enumerate(infile):
                    if line == '}\n':
                        count += 1

            with open(formattedFile,'w') as outfile:
                for index,line in enumerate(infile):
                    if index == 0 or index == 1:
                        continue
                    elif index == 2:
                        outfile.write('[')
                    elif line == '}\n' and count > 1:
                        line = '},\n'
                        count -= 1
                        outfile.write(line)
                    elif line == '}\n' and count <= 1:
                        line = '}\n'
                        count -= 1
                        outfile.write(line)
                    else:
                        outfile.write(line)

                outfile.write(']')

        data = None
        with open(formattedFile) as f:
            data = json.load(f)

        exploitCount = 0
        for obj in data:
        
            if len(obj['RESULTS_EXPLOIT']) > 0:
                service = obj['SEARCH']
                for result in obj['RESULTS_EXPLOIT']:
                    name = result['Title']
                    id = result['EDB-ID']
                    date = result['Date']
                    type = result['Type']
                    platform = result['Platform']
                    file = result['Path']

                    # Don't save DOS attacks
                    if type != 'dos':
                        session.attackManager.addAttack(Attack.Attack(name, file, '', service, id, date, type, platform))
                        
                        if not os.path.exists(session.getExploitDir() + '/PossibleAttempts'):
                            os.makedirs(session.getExploitDir()+ '/PossibleAttempts')
                        
                        if not os.path.exists(session.getExploitDir() + '/PossibleAttempts/' + service):
                            os.makedirs(session.getExploitDir() + '/PossibleAttempts/' + service)
                            
                        shutil.copy(file, session.getExploitDir() + '/PossibleAttempts/' + service + '/' + os.path.basename(file))
                        exploitCount += 1
                        
        print('Possible exploits found and saved: ' + str(exploitCount))

        return True

    def parseToolOutput(self, tool):
        try:
            fileName = tool.getOutputFileName()
            self.parseFile(fileName)
        except Exception as e:
            logging.exception(e)
            return False

        return True


import uuid
import os
import platform
import logging
import json
from datetime import date
from threading import Thread

import TargetHost
import Attack
import ToolManager
import Checklist
from MenuBase import MenuBase

class Session():
    def __init__(self, name = None):
        pass

    def start(self, name = None, isNew = False, ip = None):
        if platform.system() == 'Windows':
            os.sys.path.append('c:/python/lib/site-packages')
        else:
            pass
            #os.sys.path.append('/usr/lib/python3/dist-packages')
            #os.sys.path.append('/usr/local/lib/python2.7/dist-packages')
            #os.sys.path.append('/usr/lib/python3.6/dist-packages')
            #os.sys.path.append('/usr/lib/python3.7/dist-packages')
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        import Screen
        import Setup
        import Enumeration
        import Exploit
        import Maintain
        import Parsers

        self.DEV_MODE = True
        self.CWD = os.getcwd()
        self.attackManager = Attack.AttackManager()
        self.targetHost = TargetHost.TargetHost()
        self.parserManager = Parsers.ParserManager()
        self.checklistManager = Checklist.ChecklistManager()

        self._rhost = '127.0.0.1'
        self._rport = 'ALL'
        self._targetOS = 'Agnostic'
        self._sessionId = ''
        self._threads = '50'
        self._wordlist = '/usr/share/wordlists/rockyou.txt'
        self._httpWordlist = '/usr/share/wordlists/rockyou.txt'
        self._dbWordlist = '/usr/share/wordlists/rockyou.txt'
        self._userlist = '/usr/share/wordlists/rockyou.txt'

        if name == None or len(name) < 5 or isNew == True:
            # New session
            if isNew == True:
                self._id = name
                self._sessionId = name
                
                if ip != None:
                    self._rhost = ip
            else:
                self._id = str(uuid.uuid4())[:5]
                self._sessionId = str(date.today()) + '-' + self._id
        else:
            # Saved session
            self._id = name[5:]
            self._sessionId = name

            self.load(self._sessionId)  

        # Create session directories
        self._workingDir = './' + self._sessionId
        if not os.path.exists(self._workingDir):
            os.makedirs(self._workingDir)

        self._exploitDir = self._workingDir + '/exploits'
        if not os.path.exists(self._exploitDir):
            os.makedirs(self._exploitDir)

        self._lootDir = self._workingDir + '/loot'
        if not os.path.exists(self._lootDir):
            os.makedirs(self._lootDir)

        self._intelDir = self._workingDir + '/intel'
        if not os.path.exists(self._intelDir):
            os.makedirs(self._intelDir)

        self._reportDir = self._workingDir + '/report'
        if not os.path.exists(self._reportDir):
            os.makedirs(self._reportDir)

        # Set standard report/markdown files
        #self._reportOutput = self._reportDir + '/output.md'
        #self._reportResult = self._reportDir + '/result.md'

        # Logging
        logging.basicConfig(format='%(asctime)s %(message)s', filemode = 'a', datefmt='%m/%d/%Y %I:%M:%S %p', filename=self._workingDir + '/session.log', level=logging.INFO)  
        self.save()

        self.screen = Screen.Screen()
        self.setup = Setup.Setup()
        self.enumeration = Enumeration.Enumeration()
        self.exploit = Exploit.Exploit()
        self.maintain = Maintain.Maintain()
        self.toolManager = ToolManager.ToolManager()
        self.PROCS = []
        self.USE_SDKS = False
     
    # region Getters and Setters

    def getLootFiles(self):
        return os.listdir(self._lootDir)
        
    def getIntelFiles(self):
        return os.listdir(self._intelDir)
        
    def getExploitFiles(self):
        return os.listdir(self._exploitDir)

    def getId(self):
        return self._id

    def getSessionId(self):
        return self._sessionId

    def getWorkingDir(self):
        return self._workingDir

    def getExploitDir(self):
        return self._exploitDir

    def getLootDir(self):
        return self._lootDir

    def getIntelDir(self):
        return self._intelDir

    def getReportDir(self):
        return self._reportDir

    def getRemoteHost(self):
        return self._rhost

    def setRemoteHost(self, rhost):
        self._rhost = rhost
        self.save()

    def getRemotePort(self):
        return self._rport

    def setRemotePort(self, rport):
        self._rport = rport
        self.save()

    def getTargetOs(self):
        return self._targetOS

    def setTargetOs(self, targetOs):
        self._targetOS = targetOs
        self.save()

    def getThreads(self):
        return self._threads

    def setThreads(self, threads):
        self._threads = threads
        self.save()

    def getWordlist(self):
        return self._wordlist

    def setWordlist(self, wordlist):
        self._wordlist = wordlist
        self.save()

    def getHttpWordlist(self):
        return self._httpWordlist

    def setHttpWordlist(self, wordlist):
        self._httpWordlist = wordlist
        self.save()

    def getDbWordlist(self):
        return self._dbWordlist

    def setDbWordlist(self, wordlist):
        self._dbWordlist = wordlist
        self.save()

    def getUserlist(self):
        return self._userlist

    def setUserlist(self, userlist):
        self._userlist = userlist
        self.save()

    # endregion

    def save(self):
        import json

        # Session
        session = {}  
        session['SESSION'] = []  
        session['SESSION'].append({  
                'rhost' : self._rhost,
                'rport' : self._rport,
                'target_os' : self._targetOS,
                'session_id' : self._sessionId,
                'threads' : self._threads,
                'wordlist' : self._wordlist,
                'http_wordlist' : self._httpWordlist,
                'db_wordlist' : self._dbWordlist,
                'userlist' : self._userlist
        })

        # Services
        session['SERVICES'] = []
        for service in self.targetHost.getServices():
            session['SERVICES'].append({
                    'name' :  str(service.getName()),
                    'port' :  str(service.getPort()),
                    'protocol' :  str(service.getProtocol()),
                    'status' :  str(service.getStatus()),
                    'version' :  str(service.getVersion())
                })

        # Possible attacks
        session['ATTACKS'] = []
        for attack in self.attackManager.getAttacks():
            session['ATTACKS'].append({
                    'id' : attack.getId(),
                    'name' : attack.getName(),
                    'file' : attack.getFile(),
                    'desc' : attack.getDesc(),
                    'service' : attack.getService(),
                    'date' : attack.getDate(),
                    'type' : attack.getType(),
                    'platform' : attack.getPlatform()
                    })

        # HTTP directories found
        session['HTTP_DIR'] = []
        for dir in self.targetHost.getHttpDirectories():
            session['HTTP_DIR'].append({ 'dir' : dir })

        # HTTP files found
        session['HTTP_FILE'] = []
        for file in self.targetHost.getHttpFiles():
            session['HTTP_FILE'].append({ 'file' : file })

        # Notes
        session['NOTES'] = []
        for note in self.targetHost.getNotes():
            session['NOTES'].append({ 'note' : note })

        # Checklists
        session['CHECKLISTS'] = []
        for category in self.checklistManager.getChecklists():
            checklistCat = {}
            checklistCat[category._CategoryName] = []
            for i, item in category._items.items():
                checklistCat[category._CategoryName].append({
                    'id' : str(i),
                    'result' : item._result,
                    'notes' : item._notes
                    })
            session['CHECKLISTS'].append({ category._CategoryName : checklistCat[category._CategoryName] })

        self.targetHost.generateReport()
        self.checklistManager.generateReport()

        with open(self._workingDir + '/session.json', 'w') as outfile:  
            json.dump(session, outfile, indent = 4)

        return

    def load(self, sessionId):
        data = None
        with open(sessionId + '/session.json', encoding="utf8") as f:
            data = json.load(f)

        for session in data['SESSION']:
            self._targetOS = session['target_os']
            self._rhost = session['rhost']
            self._rport = session['rport']
            self._threads = session['threads']
            self._wordlist = session['wordlist']
            self._httpWordlist = session['http_wordlist']
            self._dbWordlist = session['db_wordlist']
            self._userlist = session['userlist']
            
        for service in data['SERVICES']:
            self.targetHost.addService(service['port'], service['protocol'], service['status'], service['name'], service['version'])

        for attack in data['ATTACKS']:
            attack = Attack.Attack(attack['name'], attack['file'], attack['desc'], attack['service'], attack['id'], attack['date'], attack['type'], attack['platform'])
            self.attackManager.addAttack(attack)

        for dir in data['HTTP_DIR']:
            self.targetHost.addHttpDirectory(dir['dir'])

        for file in data['HTTP_FILE']:
            self.targetHost.addHttpFile(file['file'])

        for note in data['NOTES']:
            self.targetHost.addNotes(note['note'])

        
        for checklist in data['CHECKLISTS']:
            for name, category in checklist.items():
                for item in category:
                    self.checklistManager.setValue(name, item['id'], item['result'], item['notes'])

        self._id = sessionId[-5:]
        self._workingDir = './' + self._sessionId

        return

    def addReportCmd(self, cmd, comments = '', outputFile = ''):
        import time
        import datetime
        import random

        timestamp = time.time()
        reportDate = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        with open(self._reportDir + '/cmd.md','a') as report:
            report.write('')                    # Blank line
            if len(comments) > 0:               # Check for comments
                report.write(comments)
                report.write('')

            report.write('> ' + cmd)            # Write command

            if len(outputFile) > 0:             # Check for output file and put in footnotes
                num = random.randint(1000,9999)
                report.write('Output file is created [^' + num + ']')
                report.write('[^' + num + '] ' + outputFile)

            report.write('')
        return

    def endProgram(self):
        try:
            from subprocess import Popen
    
            try:
                self.save()
            except Exception as e:
                logging.exception(e)

            for p in self.PROCS:
                try:
                    print('Terminating PID: ' + str(p.pid))
                    p.terminate()
                    #Popen("TASKKILL /F /PID {pid} /T".format(pid=p.pid))
                except:
                    continue

            #for t in session.THREADS:
            #    t.stop()
        except:
            pass

        quit()

    def runCmdSimple(self, cmd, comments = '', outputFile = '', quiet = False):
        import os
        print(MenuBase.CMD + cmd + MenuBase.ENDC)
        if quiet == True:
            os.system(cmd + ' &> /dev/null') # Not windows compatible
        else:
            os.system(cmd)
        
        self.addReportCmd(cmd, comments, outputFile)

    def runCmd(self, cmd, title, appList = None, onComplete = None, arg = None, quiet = False, comments = ''):
        import subprocess

        useShell = True
        if platform.system() == 'Windows':
            useShell = False
    
        print(MenuBase.CMD + cmd + MenuBase.ENDC)

        proc = None
        if quiet == True:
            with open(os.devnull, 'w') as FNULL:
                proc = subprocess.Popen(cmd, stdout=FNULL, shell=useShell)
        else:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=useShell)
            
        self.PROCS.append(proc)
        self.addReportCmd(cmd, comments)

        if appList != None:
            appList.append(proc)

        while proc.poll() == None:
            pass

        print(MenuBase.MSG + title + ': is completed' + MenuBase.ENDC + '\n> ', end = '')

        if onComplete != None:
            if arg is None:
                onComplete()
            else: 
                onComplete(arg)

    def runThreadedCmd(self, cmd, title, appList = None, onComplete = None, arg = None):
        t = Thread(target=self.runCmd, args=(cmd, title, appList, onComplete, arg)) 
        t.start()

global session
session = Session()


import os
import platform

from Session import *
import TargetHost
import Attack
from Parsers import ParserSearchSploit
from Tools import *

# searchsploit -j --nmap FILE | tee OUT.JSON

class Templates:
    def __init__(self):
        pass

    def runStandard(self):
        print('Running standard attack')

        # Get our nmap result files
        nmapFiles = []
        for fn in os.listdir(session.getIntelDir()):
            if 'nmap_' in fn:
                print('Nmap file found: ' + fn)
                nmapFiles.append(fn)

        # Run  searchsploit
        if platform.system() == 'Windows':
            print('Windows not ready')
        else:
            for fn in nmapFiles:
                outFile = session.getExploitDir() + '/searchsploit_' + fn + '.json'
                exclude = ' --exclude="windows" '
                if session.getTargetOs() == 'Windows':
                    exclude = ' --exclude="linux" '
                    
                cmd = 'searchsploit -j --nmap ' + session.getIntelDir() + '/' + fn + exclude + ' | tee ' + outFile
                session.runCmdSimple(cmd, 'Searching searchsploit for know vulnerabilities', outFile)
                parser = ParserSearchSploitNmap()
                parser.parseFile(outFile)
        
        # Find services and attack them
        if session.targetHost.hasHttp() != '-1':
            self.runHttp()

        if session.targetHost.hasAcarsd() != '-1':
            session.toolManager.runByName('NmapAcars', Tool.ToolCategory.VulnerabilityScanner)

        if session.targetHost.hasAfp() != '-1':
            session.toolManager.runByName('NmapAfp', Tool.ToolCategory.VulnerabilityScanner)

        if session.targetHost.hasAjp() != '-1':
            session.toolManager.runByName('NmapAjp', Tool.ToolCategory.VulnerabilityScanner)

        if session.targetHost.hasAllseeingeye() != '-1':
            session.toolManager.runByName('NmapAllseeingeye', Tool.ToolCategory.VulnerabilityScanner)

        if session.targetHost.hasAmqp() != '-1':
            session.toolManager.runByName('NmapAmqp', Tool.ToolCategory.VulnerabilityScanner)

        if session.targetHost.hasMysql() != '-1':
            print('mysql found')

        print('DONE')

    def _runStandardOnComplete(self, outFile):
        pass

    def runHttp(self):
        print('Running HTTP attack')

        # Run all HTTP scripts from Nmap
        print('Threading Nmap HTTP scans, this will take awhile')
        session.toolManager.runByName('Nmap-all-http', Tool.ToolCategory.VulnerabilityScanner)

        # Directory bruteforce, this will populate http directories and files
        print('Starting DIRB')
        session.runCmdSimple('dirb http://' + session.getRemoteHost() + ' /usr/share/wordlists/dirb/common.txt -S -w | tee ' + 
            session.getIntelDir() + '/DIRB.out', 'Running DIRB to find popular directories and files')
        session.parserManager.parseOutput('dirb', session.getIntelDir() + 'DIRB.out')

        print('Starting Gobuster')
        session.runCmdSimple('gobuster -e -u http://' + session.getRemoteHost() + ' -w /usr/share/wordlists/dirb/common.txt | tee ' + 
            session.getIntelDir() + '/gobuster.out', 'Running Gobuster to find popular directories and files')
        session.parserManager.parseOutput('Gobuster', session.getIntelDir() + 'gobuster.out')

        # WP scans
        if session.targetHost.getWordpressDir() != None:
            self.runWordPress()

        # Tools
        session.toolManager.runByName('sslyze', Tool.ToolCategory.Enumeration)
        session.runCmdSimple('apache-users -h ' + session.getRemoteHost() + ' -l /usr/share/wordlists/metasploit/unix_users.txt -p 80 -s 0 -e 403 -t 10', 'Checking for common Apache users')
        session.toolManager.runByName('davtest', Tool.ToolCategory.Web)

        #for file in session.targetHost.getHttpFiles():
        #    session.runCmdSimple('fimap -u "http://' + session.getRemoteHost() + '/' + file + '"')

        print('These tools could be useful, just requires manual input:')
        print('arachni_web <-- GUI')
        print('bbqsql <-- Interactive')
        print('BlindElephant <-- If it\'s wordpress')
        print('burpsuite <-- GUI')
        print('DONE')

    def runFtp(self):
        # hydra -l /usr/share/wordlists/metasploit/user -P /usr/share/wordlists/metasploit/ passwords ftp://192.168.1.101 –V 

        return

    def runWordPress(self, dir = None):
        if dir == None:
            dir = session.targetHost.getWordpressDir()
        
        if dir == None:
            return

        # WPScan
        tool = session.toolManager.getTool('WPScan', toolCategory = 4)
        if tool is None:
            print('COULD NOT RUN WPScan!!!')
        else:
            print('Starting WPScan')
            tool.run(threaded = 'false')

        # BlindElephant
        tool = session.toolManager.getTool('BlindElephant-wordpress', toolCategory = 4)
        if tool is None:
            print('COULD NOT RUN BlindElephant!!!')
        else:
            print('Starting BlindElephant-wordpress')
            tool.run(threaded = 'false')

        # Skipfish
        tool = session.toolManager.getTool('Skipfish', toolCategory = 4)
        if tool is None:
            print('COULD NOT RUN Skipfish!!!')
        else:
            print('Starting Skipfish')
            tool.run(threaded = 'false')

        # WhatWeb
        tool = session.toolManager.getTool('WhatWeb', toolCategory = 4)
        if tool is None:
            print('COULD NOT RUN WhatWeb!!!')
        else:
            print('Starting WhatWeb')
            tool.run(threaded = 'false')

    def runWindows(self):
        print('Running Windows attack')
        
        print('DONE')

    def runLinux(self):
        print('Running Linux attack')
        
        print('DONE')

    def runSmb(self):
        session.toolManager.runByName('enum4linux', ToolCategory.Enumeration)

        return

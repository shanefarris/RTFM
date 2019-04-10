
import os
import platform

from Session import *
import TargetHost
import Attack
from ToolManager import *
from Parsers import ParserSearchSploit, ParserSearchSploitNmap

class Templates:
    def __init__(self):
        pass

    def runStandard(self):
        try:
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
        
            # Firewall enumeration
            session.toolManager.runByName('NmapFirewalk', ToolCategory.Enumeration)
            session.toolManager.runByName('NmapFirewall', ToolCategory.VulnerabilityScanner)

            # Find services and attack them
            if session.targetHost.hasHttp() != '-1':
                self.runHttp()

            if session.targetHost.hasAcarsd() != '-1':
                session.toolManager.runByName('NmapAcars', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasAfp() != '-1':
                session.toolManager.runByName('NmapAfp', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasAjp() != '-1':
                session.toolManager.runByName('NmapAjp', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasAllseeingeye() != '-1':
                session.toolManager.runByName('NmapAllseeingeye', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasAmqp() != '-1':
                session.toolManager.runByName('NmapAmqp', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasMysql() != '-1':
                self.runMySql()

            if session.targetHost.hasSmb() != '-1':
                self.runSmb()

            if session.targetHost.hasCassandra() != '-1':
                session.toolManager.runByName('NmapCassandra', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasCics() != '-1':
                session.toolManager.runByName('NmapCics', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasClamAv() != '-1':
                session.toolManager.runByName('NmapClam', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasCoap() != '-1':
                session.toolManager.runByName('NmapCoap', ToolCategory.Enumeration)

            if session.targetHost.hasCvs() != '-1':
                session.toolManager.runByName('NmapCvs', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasDb2() != '-1':
                session.toolManager.runByName('NmapDb2', ToolCategory.Enumeration)

            if session.targetHost.hasDeluge() != '-1':
                session.toolManager.runByName('NmapDelugeRpc', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasDistccd() != '-1':
                session.toolManager.runByName('NmapDistccd', ToolCategory.Exploit)

            if session.targetHost.hasDns() != '-1':
                self.runDns()

            if session.targetHost.hasDrda() != '-1':
                session.toolManager.runByName('NmapDrda', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasIphoto() != '-1':
                session.toolManager.runByName('NmapIphoto', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasInformix() != '-1':
                session.toolManager.runByName('NmapInformixBrute', ToolCategory.Password)

            if session.targetHost.hasEtherNetIp() != '-1':
                session.toolManager.runByName('NmapEnip', ToolCategory.Enumeration)

            if session.targetHost.hasEsx() != '-1':
                session.toolManager.runByName('NmapVmware', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasFinger() != '-1':
                session.toolManager.runByName('NmapFinger', ToolCategory.Enumeration)

            if session.targetHost.hasFume() != '-1':
                session.toolManager.runByName('NmapFume', ToolCategory.Enumeration)

            if session.targetHost.hasFox() != '-1':
                session.toolManager.runByName('NmapFox', ToolCategory.Enumeration)

            if session.targetHost.hasFreelancer() != '-1':
                session.toolManager.runByName('NmapFreelancer', ToolCategory.Enumeration)

            if session.targetHost.hasFtp() != '-1':
                session.toolManager.runByName('NmapFtp', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasHddTemp() != '-1':
                session.toolManager.runByName('NmapHddTemp', ToolCategory.Enumeration)

            if session.targetHost.hasImap() != '-1':
                self.runImap()

            if session.targetHost.hasLotusNotesUser() != '-1':
                session.toolManager.runByName('NmapDominoUsers', ToolCategory.Exploit)

            if session.targetHost.hasLotusNotesConsole() != '-1':
                session.toolManager.runByName('NmapDominoConsole', ToolCategory.Exploit)

            if session.targetHost.hasMsSql() != '-1':
                session.toolManager.runByName('NmapMsSqlBrute', ToolCategory.Password)

            if session.targetHost.hasRdp() != '-1':
                self.runRdp()

            if session.targetHost.hasSnmp() != '-1':
                self.runSnmp()

            if session.targetHost.hasSsh() != '-1':
                session.toolManager.runByName('NmapSsh', ToolCategory.VulnerabilityScanner)

            if session.targetHost.hasVlcStream() != '-1':
                session.toolManager.runByName('NmapVlcStreamer', ToolCategory.Enumeration)

            print('DONE')
        except Exception as e:
            logging.exception(e)
            print(e)

    def _runStandardOnComplete(self, outFile):
        pass

    def runHttp(self):
        print('Running HTTP attack')

        # Run all HTTP scripts from Nmap
        print('Threading Nmap HTTP scans, this will take awhile')
        session.toolManager.runByName('Nmap-all-http', ToolCategory.VulnerabilityScanner)

        # Directory bruteforce, this will populate http directories and files
        print('Starting DIRB')
        session.runCmdSimple('dirb http://' + session.getRemoteHost() + ' /usr/share/wordlists/dirb/common.txt -S -w | tee ' + 
            session.getIntelDir() + '/DIRB.out', 'Running DIRB to find popular directories and files')
        session.parserManager.parseOutput('dirb', session.getIntelDir() + 'DIRB.out')

        print('Starting Gobuster')
        session.runCmdSimple('gobuster -e -u http://' + session.getRemoteHost() + ' -w /usr/share/wordlists/dirb/common.txt | tee ' + 
            session.getIntelDir() + '/gobuster.out', 'Running Gobuster to find popular directories and files')
        session.parserManager.parseOutput('Gobuster', session.getIntelDir() + 'gobuster.out')

        # Updating checklist
        session.checklistManager.setValue('Http', 2, 'DONE', 'Automatically ran this via template using dirb/common.txt.')

        # WP scans
        if session.targetHost.getWordpressDir() != None:
            self.runWordPress()

        # Tools
        session.toolManager.runByName('sslyze', ToolCategory.Enumeration)
        session.runCmdSimple('apache-users -h ' + session.getRemoteHost() + ' -l /usr/share/wordlists/metasploit/unix_users.txt -p 80 -s 0 -e 403 -t 10', 'Checking for common Apache users')
        session.toolManager.runByName('davtest', ToolCategory.Web)

        #for file in session.targetHost.getHttpFiles():
        #    session.runCmdSimple('fimap -u "http://' + session.getRemoteHost() + '/' + file + '"')

        # Generate wordlist based on HTML pages
        session.toolManager.runByName('CeWL', ToolCategory.Password)

        print('These tools could be useful, just requires manual input:')
        print('arachni_web <-- GUI')
        print('bbqsql <-- Interactive')
        print('BlindElephant <-- If it\'s wordpress')
        print('burpsuite <-- GUI')
        print('DONE')

    def runFtp(self):
        print('FTP CHECK')

        # hydra -l /usr/share/wordlists/metasploit/user -P /usr/share/wordlists/metasploit/ passwords ftp://192.168.1.101 –V 
        session.runCmdSimple(' nmap -v -p 21 --script=ftp-anon.nse ' + session.getRemoteHost(), 'Checking for annonyouse FTP account.', session.getIntelDir() + '/nmap_ftp_annon.out')
        
        return

    def runWordPress(self, dir = None):
        if dir == None:
            dir = session.targetHost.getWordpressDir()
        
        if dir == None:
            return

        # WPScan
        print('Starting WPScan')
        session.toolManager.runByName('WPScan', ToolCategory.Web, threaded = False)

        # BlindElephant
        print('Starting BlindElephant-wordpress')
        session.toolManager.runByName('BlindElephant-wordpress', ToolCategory.Web, threaded = False)

        # Skipfish
        print('Starting Skipfish')
        session.toolManager.runByName('Skipfish', ToolCategory.Web, threaded = False)

        # WhatWeb
        print('Starting WhatWeb')
        session.toolManager.runByName('WhatWeb', ToolCategory.Web, threaded = False)

    def runWindows(self):
        print('Running Windows attack')
        
        self.runSmb()

        print('DONE')

    def runLinux(self):
        print('Running Linux attack')
        
        print('DONE')

    def runSmb(self):
        print('SMB CHECK')

        # Enumeration and NULL session check
        session.toolManager.runByName('enum4linux', ToolCategory.Enumeration)

        # Updating checklist
        session.checklistManager.setValue('Smb', 1, 'DONE', 'Automatically ran this via template.')
        session.checklistManager.setValue('Smb', 2, 'DONE', 'Automatically ran this via template using enum4linux with \'a\' switch.')

        # More advanced enumeration
        session.toolManager.runByName('NmapSmbEnum', ToolCategory.Enumeration)
        
        # Checking for vulnerabilities
        session.toolManager.runByName('NmapSmbVuln', ToolCategory.VulnerabilityScanner)

        # Updating checklist
        session.checklistManager.setValue('Smb', 7, 'DONE', 'Automatically ran this via template.')
        
        # Bruteforcing
        session.toolManager.runByName('NmapSmbBrute', ToolCategory.Password)
        
        # Udating checklist
        session.checklistManager.setValue('Smb', 8, 'DONE', 'Automatically ran this via template, using nmap smb-brute.nse script.')

        return

    def runSnmp(self):
        print('SNMP CHECK')

        # Enumerate all
        session.runCmdSimple('snmpwalk -c public -v 1 ' + session.getRemoteHost(), 'Running SNMP enumeration ALL (snmpwalk)', session.getIntelDir() + '/snmp.out')

        # Look for Win users
        session.runCmdSimple('snmpwalk -c public -v 1 ' + session.getRemoteHost() + ' 1.3.6.1.4.1.77.1.2.25', 'Running SNMP enumeration Win users (snmpwalk)', session.getIntelDir() + '/snmp_users.out')

        # Look for Win processes
        session.runCmdSimple('snmpwalk -c public -v 1 ' + session.getRemoteHost() + ' 1.3.6.1.2.1.25.4.2.1.2', 'Running SNMP enumeration Win processes (snmpwalk)', session.getIntelDir() + '/snmp_processes.out')

        # Look for open TCP ports
        session.runCmdSimple('snmpwalk -c public -v 1 ' + session.getRemoteHost() + ' 1.3.6.1.2.1.6.13.1.3', 'Running SNMP enumeration open TCP ports (snmpwalk)', session.getIntelDir() + '/snmp_tcp_ports.out')

        # Look for software
        session.runCmdSimple('snmpwalk -c public -v 1 ' + session.getRemoteHost() + ' 1.3.6.1.2.1.25.6.3.1.2', 'Running SNMP enumeration software (snmpwalk)', session.getIntelDir() + '/snmp_software.out')

        session.runCmdSimple('snmp-check ' + session.getRemoteHost(), 'Running snmp-check', session.getIntelDir() + '/snmpcheck.out')

        session.toolManager.runByName('NmapSnmpEnum', ToolCategory.Enumeration)
        session.toolManager.runByName('NmapSnmpBrute', ToolCategory.Password)

        return

    def runImap(self):
        print('IMAP CHECK')
        session.toolManager.runByName('NmapImapEnum', ToolCategory.Enumeration)
        session.toolManager.runByName('NmapImapBrute', ToolCategory.Password)
        return

    def runMySql(self):
        print('MySQL CHECK')
        session.toolManager.runByName('NmapMySqlEnum', ToolCategory.Enumeration)
        session.toolManager.runByName('NmapMySqlBrute', ToolCategory.Password)
        return

    def runDns(self):
        print('DNS CHECK')
        session.toolManager.runByName('NmapDnsEnum', ToolCategory.Enumeration)
        session.toolManager.runByName('NmapDnsVul', ToolCategory.VulnerabilityScanner)
        return

    def runRdp(self):
        print('RPD CHECK')
        session.runThreadedCmd('nmap -sV --script=rdp-vuln-ms12-020 -p 3389 ' + session.getRemoteHost(), 'vuln-ms12-020 Check')
        session.setRemotePort('3389')
        session.setUserlist('../wordlists/usernames.txt')
        session.toolManager.runByName('Ncrack-multi user', ToolCategory.Password)
        return

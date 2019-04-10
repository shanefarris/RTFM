
import json
import logging
from enum import Enum, unique
from collections import defaultdict

# from Session import * # I miss C++
import Session
from MenuBase import *

@unique
class ToolCategory(Enum):
    Enumeration = 1
    VulnerabilityScanner = 2
    Exploit = 3
    Web = 4
    StressTest = 5
    Forensics = 6
    Wireless = 7
    SniffingSpoofing = 8
    Password = 9
    Maintaining = 10
    ReverseEng = 11
    Reporting = 12
    Hardware = 13

class Tool:
    def __init__(self, name, category, desc, example, cmd, args, parserName):
        self._name = name
        self._category = category
        self._desc = desc
        self._example = example
        self._cmd = cmd
        self._args = args
        self._parserName = parserName
        self._arguments = []    # TODO: Use this to replace string _args

    def __repr__(self):
        return 'Tool'

    def __str__(self):
        return 'Name: ' + str(self._name) + '\ncategory: ' + str(self._category) + '\nDescription: ' + str(self._desc) + \
            '\nExample: ' + str(self._example) + '\nCmd: ' + str(self._cmd) + '\nArgs: ' + str(self._args) + \
            '\nParser: ' + str(self._parserName)

    def compileCmd(self):
        cmdTemplate = self._cmd

        # Check for custom arguments
        arry = self.promptForArg()
        if arry != None:
            count = 1
            for arg in arry:
                argStr = '${arg' + str(count) + '}'
                self._cmd = self._cmd.replace(argStr, arg)
                count += 1

        # Look for standard arguments
        self._cmd = self._cmd.replace('${target}', Session.session.getRemoteHost())
        self._cmd = self._cmd.replace('${working_dir}', Session.session.getWorkingDir())
        self._cmd = self._cmd.replace('${pass_file}', Session.session.getWordlist())
        self._cmd = self._cmd.replace('${user_file}', Session.session.getUserlist())

        # Port might need to promp for input if value is 'ALL'
        standardArg = ['${interface}', '${target_mac}', '${gateway}']
        if '${port}' in self._cmd and Session.session.getRemotePort() == 'ALL':
            standardArg.append('${port}')
        else:
            self._cmd = self._cmd.replace('${port}', Session.session.getRemotePort())

        # Prompt for the other standard arguments
        for arg in standardArg:
            if arg in self._cmd:
                prompt = arg.replace('${', '').replace('}', ': ')
                print(prompt, end = '')
                choice = input()
                self._cmd = self._cmd.replace(arg, choice)

        ret = self._cmd             # Save our results
        self._cmd = cmdTemplate     # Reset our template
        return ret

    def compileOutfile(self):
        dir = self.getOutputFileName()
        outFile = ' | tee ' + dir
        return outFile

    def run(self, threaded = True, quiet = False, customOutfile = False, onComplete = None):
        # Show example, could be helpful if populating arguments
        print(self._example)

        cmd = self.compileCmd()
        
        if customOutfile == True:
            outFile = ''
        else:
            outFile = self.compileOutfile()

        if threaded == True:
            Session.session.runThreadedCmd(cmd + outFile, self._name, onComplete = onComplete)
        else:
            Session.session.runCmd(cmd + outFile, self._name, onComplete = onComplete)

        return outFile

    def promptForArg(self):
        # Looks for and fills in custom arguments
        if self._args == None or self._args == '':
            return None

        arry = []
        count = 1
        for prompt in self._args.split(','):
            # parse arg number and prompt string
            argStr = '${arg' + str(count) + '}'
            prompt = prompt.replace(argStr, '')
            prompt = prompt.replace(',', '')
            prompt = prompt.replace('=', ': ')
            
            # Search for default values
            default = ''
            if prompt.find('(') > -1 and prompt.find(')'):
                start = prompt.find('(') + 1
                end = prompt.find(')')
                default = prompt[start:end]
                
            # Prompt the user
            print(prompt, end = '')
            userInput = input()
            if userInput == '':
                userInput = default
            arry.append(userInput)
            count += 1

        return arry

    def getOutputFileName(self):
        dir = Session.session.getWorkingDir()
        
        if self._category == str(ToolCategory.Enumeration.value) or \
            self._category == str(ToolCategory.SniffingSpoofing.value) or \
            self._category == str(ToolCategory.Web.value) or \
            self._category == str(ToolCategory.VulnerabilityScanner.value):
            dir = Session.session.getIntelDir()
        elif self._category == str(ToolCategory.Exploit.value):
            dir = Session.session.getExploitDir()
        elif self._category == str(ToolCategory.Reporting.value):
            dir = Session.session.getReportDir()

        outFile = dir + '/' + self._name + '.out'
        return outFile

class ToolManager(MenuBase):
    def __init__(self):
        import platform

        self._toolList = {}
        for category in ToolCategory:
            self._toolList[category.value] = []

        toolsFile = './tools.json'
        if platform.system() == 'Windows':
            toolsFile = './tools_win.json'

        data = None
        with open(toolsFile, encoding="utf8") as f:
            data = json.load(f)

        for obj in data:
            try:
                if str(obj['category']).isdigit():
                    num = int(obj['category'])

                    self.addTool(Tool(obj['name'], 
                                      obj['category'], 
                                      obj['desc'], 
                                      obj['example'], 
                                      obj['cmd'], 
                                      obj['customInput'],
                                      obj['parser']), num)
                else:
                    logging.exception('Could not load tool:\n' + obj)
            except Exception as e:
                logging.exception(type(e))

        # Add custom tools
        import CustomTools
        import NmapScripts
        
        self.addTool(NmapScripts.NmapLoudTcp(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapLoudUdp(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapStandardTcp(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapStandardUdp(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapSneaky(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapPing(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapVersion(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapQuick(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapStealth(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapAcars(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapAfp(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapAjp(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapAllseeingeye(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapAmqp(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapIdentd(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapBackorifice(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapBACNet(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapBitcoin(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapBittorrent(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapBjnp(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapDiscoverScripts(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapEigrp(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapCassandra(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapCccam(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapCics(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapCitrixWeb(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapCitrixIca(), ToolCategory.Enumeration)        
        self.addTool(NmapScripts.NmapClam(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapCoap(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapCouchDb(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapCredSummary(), ToolCategory.Reporting)
        self.addTool(NmapScripts.NmapCups(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapCvs(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapDb2(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapDelugeRpc(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapDhcp(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapDistccd(), ToolCategory.Exploit)
        self.addTool(NmapScripts.NmapDnsEnum(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapDnsVul(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapDocker(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapDominoUsers(), ToolCategory.Exploit)
        self.addTool(NmapScripts.NmapDominoConsole(), ToolCategory.Exploit)
        self.addTool(NmapScripts.NmapIphoto(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapDrda(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapMultihomed(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapEnip(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapFinger(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapFirewalk(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapFirewall(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapFume(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapFox(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapFreelancer(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapFtp(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapHddTemp(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapHnap(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapHttpAnalytics(), ToolCategory.Forensics)
        self.addTool(NmapScripts.NmapHttpEnum(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapHttpExploit(), ToolCategory.Exploit)
        self.addTool(NmapScripts.NmapHttpVul(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapImapEnum(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapImapBrute(), ToolCategory.Password)
        self.addTool(NmapScripts.NmapVlcStreamer(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapVmware(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapMsSqlBrute(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapMySqlEnum(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapMySqlBrute(), ToolCategory.Password)
        self.addTool(NmapScripts.NmapSmbEnum(), ToolCategory.Enumeration)
        self.addTool(NmapScripts.NmapSmbVuln(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapScripts.NmapSmbBrute(), ToolCategory.Password)
        self.addTool(NmapScripts.NmapSnmpBrute(), ToolCategory.Password)

        self.addTool(CustomTools.SmtpUserVerify(), ToolCategory.Enumeration)
        
        if platform.system() == 'Windows':
            self.addTool(CustomTools.DownloadFileWindows(), ToolCategory.Maintaining)
        else:
            self.addTool(CustomTools.CustomWordlist(), ToolCategory.Password)
            self.addTool(CustomTools.HydraCustom(), ToolCategory.Password)
            self.addTool(CustomTools.BruteSopMultiServer(), ToolCategory.Password)
            self.addTool(CustomTools.CiscoGlobalExploiter(), ToolCategory.VulnerabilityScanner)
            self.addTool(CustomTools.OpenVAS(), ToolCategory.VulnerabilityScanner)
            self.addTool(CustomTools.SearchsploitNmap(), ToolCategory.Exploit)
            self.addTool(CustomTools.SearchsploitTargetHost(), ToolCategory.Exploit)
            self.addTool(CustomTools.SearchsploitCustomSearch(), ToolCategory.Exploit)
            self.addTool(CustomTools.DownloadFileLinux(), ToolCategory.Maintaining)
            self.addTool(CustomTools.SQLMapCustom(), ToolCategory.Web)

        return

    def __repr__(self):
        return 'ToolManager'

    def __str__(self):
        ret = ''
        for category in ToolCategory:
            for tool in self._toolList[category.value]:
                ret = ret + str(tool) + '\n\n'
        return ret

    def addTool(self, tool, toolCategory):
        try:
            if isinstance(toolCategory, (ToolCategory)):
                self._toolList[toolCategory.value].append(tool)
            else:
                self._toolList[toolCategory].append(tool)
        except Exception as e:
            print('Out of range')

    def getTools(self):
        return self._toolList

    def getToolsByCategory(self, toolCategory):
        try:
            return self._toolList[toolCategory]
        except:
            print('Out of range')

    def findToolIndex(self, name, toolCategory):
        try:
            toolsByCategory = None
            if isinstance(toolCategory, (int)) == True:
                toolsByCategory = self.getToolsByCategory(toolCategory)
            else:
                toolsByCategory = self.getToolsByCategory(toolCategory.value)

            index = 0
            for tool in toolsByCategory:
                if tool._name.lower() == name.lower():
                    return index
                index += 1

        except Exception as e:
            logging.exception(type(e))
            print(e)
            
        return -1

    def getTool(self, index, toolCategory):
        try:
            idx = index
            if isinstance(index, (int)) == False:
                idx = self.findToolIndex(index, toolCategory)

            toolsByCategory = None
            if isinstance(toolCategory, (ToolCategory)) == True:
                toolsByCategory = self.getToolsByCategory(toolCategory.value)
            else:
                toolsByCategory = self.getToolsByCategory(toolCategory)

            tool = toolsByCategory[idx]
            return tool
        except Exception as e:
            logging.exception(type(e))
            print(e)
            
        return None

    def printInfo(self, index, toolCategory):
        tool = self.getTool(index, toolCategory)

        if tool == None:
            print('Unable to find tool')
            return

        print(self.TITLE + 'Description:' + MenuBase.ENDC)
        print(tool._desc)
        print('')
        print(MenuBase.TITLE + 'Example:' + MenuBase.ENDC)
        print(tool._example)

        self.prompt()
     
    def run(self, index, toolCategory, threaded = True, quiet = False, customOutfile = False, onComplete = None):
        tool = self.getTool(index, toolCategory)
        
        outputFile = ''
        if tool == None:
            self.prompt('Unable to find tool')
        else:
            outputFile = tool.run(threaded = threaded, quiet = quiet, customOutfile = customOutfile, onComplete = onComplete)
            self.prompt()

        return outputFile

    def runByName(self, name, toolCategory, threaded = True, quiet = False, customOutfile = False, onComplete = None):
        index = self.findToolIndex(name, toolCategory)

        tool = self.getTool(index, toolCategory)
        
        outputFile = ''
        if tool == None:
            self.prompt('Unable to find tool')
        else:
            outputFile = tool.run(threaded = threaded, quiet = quiet, customOutfile = customOutfile, onComplete = onComplete)
            self.prompt()

        return outputFile
        
class Argument:
    def __init__(self, option, description, value = '', delim = '=', isBool = False):
        self._option = option
        self._description = description
        self._value = value
        self._delim = delim
        self._isBool = isBool
        return
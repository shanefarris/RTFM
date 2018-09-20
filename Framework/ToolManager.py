
import json
import logging
from enum import Enum, unique
from collections import defaultdict

from MenuBase import *
from Tool import Tool
from Tool import ToolCategory
from CustomTools import *
from NmapScripts import *

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
        self.addTool(NmapStealth(), ToolCategory.Enumeration)
        self.addTool(NmapAcars(), ToolCategory.Enumeration)
        self.addTool(NmapAfp(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapAjp(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapAllseeingeye(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapAmqp(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapIdentd(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapBackorifice(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapBACNet(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapBitcoin(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapBittorrent(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapBjnp(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapDiscoverScripts(), ToolCategory.Enumeration)
        self.addTool(NmapEigrp(), ToolCategory.Enumeration)
        self.addTool(NmapCccam(), ToolCategory.Enumeration)
        self.addTool(NmapCics(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapCitrixWeb(), ToolCategory.Enumeration)
        self.addTool(NmapCitrixIca(), ToolCategory.Enumeration)        
        self.addTool(NmapClam(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapCoap(), ToolCategory.Enumeration)
        self.addTool(NmapCouchDb(), ToolCategory.Enumeration)
        self.addTool(NmapCredSummary(), ToolCategory.Reporting)
        self.addTool(NmapCups(), ToolCategory.Enumeration)
        self.addTool(NmapCvs(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapDb2(), ToolCategory.Enumeration)
        self.addTool(NmapDelugeRpc(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapDhcp(), ToolCategory.Enumeration)
        self.addTool(NmapDistccd(), ToolCategory.Exploit)
        self.addTool(NmapDnsEnum(), ToolCategory.Enumeration)
        self.addTool(NmapDnsVul(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapDocker(), ToolCategory.Enumeration)
        self.addTool(NmapDominoUsers(), ToolCategory.Exploit)
        self.addTool(NmapDominoConsole(), ToolCategory.Exploit)
        self.addTool(NmapIphoto(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapDrda(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapMultihomed(), ToolCategory.Enumeration)
        self.addTool(NmapEnip(), ToolCategory.Enumeration)
        self.addTool(NmapFinger(), ToolCategory.Enumeration)
        self.addTool(NmapFirewalk(), ToolCategory.Enumeration)
        self.addTool(NmapFirewall(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapFume(), ToolCategory.Enumeration)
        self.addTool(NmapFox(), ToolCategory.Enumeration)
        self.addTool(NmapFreelancer(), ToolCategory.Enumeration)
        self.addTool(NmapFtp(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapHddTemp(), ToolCategory.Enumeration)
        self.addTool(NmapHnap(), ToolCategory.Enumeration)
        self.addTool(NmapHttpAnalytics(), ToolCategory.Forensics)
        self.addTool(NmapHttpEnum(), ToolCategory.Enumeration)
        self.addTool(NmapHttpExploit(), ToolCategory.Exploit)
        self.addTool(NmapHttpVul(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapVlcStreamer(), ToolCategory.Enumeration)
        self.addTool(NmapVmware(), ToolCategory.VulnerabilityScanner)
        self.addTool(NmapMsSqlBrute(), ToolCategory.VulnerabilityScanner)
        
        if platform.system() == 'Windows':
            pass
        else:
            self.addTool(CustomWordlist(), ToolCategory.Password)
            self.addTool(BruteSopSingleServer(), ToolCategory.Password)
            self.addTool(BruteSopMultiServer(), ToolCategory.Password)
            self.addTool(CiscoGlobalExploiter(), ToolCategory.VulnerabilityScanner)
            self.addTool(OpenVAS(), ToolCategory.VulnerabilityScanner)
            self.addTool(SearchsploitNmap(), ToolCategory.Exploit)
            self.addTool(SearchsploitTargetHost(), ToolCategory.Exploit)
            self.addTool(SearchsploitCustomSearch(), ToolCategory.Exploit)

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
     
    def run(self, index, toolCategory, **kwargs):
        tool = self.getTool(index, toolCategory)
        
        outputFile = ''
        if tool == None:
            self.prompt('Unable to find tool')
        else:
            outputFile = tool.run(**kwargs)
            self.prompt()

        return outputFile

    def runByName(self, name, toolCategory, **kwargs):
        index = self.findToolIndex(name, toolCategory)

        tool = self.getTool(index, toolCategory)
        
        outputFile = ''
        if tool == None:
            self.prompt('Unable to find tool')
        else:
            outputFile = tool.run(**kwargs)
            self.prompt()

        return outputFile
        
'''
if ToolCategory.Enumeration == toolCategory:
    pass
elif ToolCategory.VulnerabilityScanner == toolCategory:
    pass
elif ToolCategory.Exploit == toolCategory:
    pass
elif ToolCategory.Web == toolCategory:
    pass
elif ToolCategory.StressTest == toolCategory:
    pass
elif ToolCategory.Forensics == toolCategory:
    pass
elif ToolCategory.Wireless == toolCategory:
    pass
elif ToolCategory.SniffingSpoofing == toolCategory:
    pass
elif ToolCategory.Password == toolCategory:
    pass
elif ToolCategory.Maintaining == toolCategory:
    pass
elif ToolCategory.ReverseEng == toolCategory:
    pass
elif ToolCategory.Reporting == toolCategory:
    pass
elif ToolCategory.Hardware == toolCategory:
    pass
'''



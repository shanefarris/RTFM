
import json
import logging
from enum import Enum, unique
from collections import defaultdict

# from Session import * # I miss C++

import Session

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

        # Port might need to promp for input if value is 'ALL'
        standardArg = [ '${user_file}', '${interface}', '${target_mac}', '${gateway}' ]
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

    def run(self, **kwargs):
        threaded = 'true'
        quiet = False   # Not supported yet
        custom_outfile = False

        if kwargs is not None:
            for key, value in kwargs.items():
                if key == 'threaded':
                    threaded = value
                elif key == 'quiet':
                    quiet = value
                elif key == 'custom_outfile':
                    custom_outfile = value

        # Show example, could be helpful if populating arguments
        print(self._example)

        cmd = self.compileCmd()
        
        if custom_outfile in ['true', '1']:
            outFile = ''
        else:
            outFile = self.compileOutfile()

        if threaded in ['true', '1']:
            Session.session.runThreadedCmd(cmd + outFile, self._name)
        else:
            Session.session.runCmd(cmd + outFile, self._name)

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
                userInput == default
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



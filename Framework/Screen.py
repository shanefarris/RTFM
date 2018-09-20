
import os
import platform
from colorama import Fore, Back, Style, init

import logging
import Tool
import Templates
import Checklist
import Shells

from MenuBase import *
from Session import *

class Screen(MenuBase):

    def __init__(self):
        init()
        self._currentMenu = ''
        self._message = ''
        self._toolCategory = 0

        self.CLEAR_SCREEN = 'clear'
        if platform.system() == 'Windows':
            self.CLEAR_SCREEN = 'cls'

    def getBoarder(self):
        return self.BORDER + '************************************ ' + session.getId() + ' ************************************' + self.ENDC

    def printMenu(self, menuArray):
        os.system(self.CLEAR_SCREEN)
        star = self.BORDER + '*' + self.ENDC

        print(self.getBoarder());
        print(star)
        if len(self._message) > 0:
            print(star + '\t\t' + self.MSG + self._message + self.ENDC)

        for item in menuArray:
            print(star + ' ' + str(item))

        print(star)
        print(star + ' 0 = Main Menu\t\t00 = Quit\tList = List Menu')

        print(star)
        print(self.getBoarder())
        self.prompt()

    def createColumnArray(self, dictionary, col = 2, padding = 40):
        value = ''
        arry = [ ]

        for k, v in dictionary.items():
            # Negative key means a title or a blank line
            menuInput = k
            if menuInput < 0:
                if len(value) > 0:
                    arry.append(value)
                    value = ''

                arry.append(self.TITLE + v + self.ENDC)
            else:
                if k % col != 0:
                    value += (str(menuInput) + ' ' + str(v)).ljust(padding, ' ')
                else:
                    value += str(menuInput) + ' ' + str(v)
                    arry.append(value)
                    value = ''

        if len(value) > 0:
             arry.append(value)

        return arry

    def userinput(self):
        choice = input() # NOTE: changes behaviour in Python 3! 

        if choice is None:
            self.prompt("Try again.")

        if self.checkBuiltInCommands(choice) == True:
            return

        choice = choice.lower()
        choice = choice.strip()

        if choice == 'list':
            if platform.system() != 'Windows':
                os.system('reset')
                
            if self._currentMenu == 'options':
                self.optionsShow()
            elif self._currentMenu == 'stageSelection':
                self.stageShow()
            elif self._currentMenu == 'enumerationSelection':
                self.enumerationShow()
            elif self._currentMenu == 'internalSelection':
                self.internalShow()
            elif self._currentMenu == 'exploitSelection':
                self.exploitShow()
            elif self._currentMenu == 'maintainSelection':
                self.maintainShow()
            elif self._currentMenu == 'specificToolSelection':
                self.specificToolShow()
            elif self._currentMenu == 'specificToolSelection2':
                self.specificToolShow2()
            elif self._currentMenu == 'setupSelection':
                self.setupShow()
            elif self._currentMenu == 'settingsSelection':
                self.settingsShow()
            elif self._currentMenu == 'shellsSelection':
                self.shellsShow()
            return

        # Handle menu input
        if self._currentMenu == 'options':
            self.optionsHandle(choice)
        elif self._currentMenu == 'stageSelection':
            self.stageHandle(choice)
        elif self._currentMenu == 'enumerationSelection':
            self.enumerationHandle(choice)
        elif self._currentMenu == 'internalSelection':
            self.internalHandle(choice)
        elif self._currentMenu == 'exploitSelection':
            self.exploitHandle(choice)
        elif self._currentMenu == 'maintainSelection':
            self.maintainHandle(choice)
        elif self._currentMenu == 'specificToolSelection':
            self.specificToolHandle(choice)
        elif self._currentMenu == 'specificToolSelection2':
            self.specificToolHandle2(choice)
        elif self._currentMenu == 'setupSelection':
            self.setupHandle(choice)
        elif self._currentMenu == 'settingsSelection':
            self.settingsHandle(choice)
        elif self._currentMenu == 'shellsSelection':
            self.shellsHandle(choice)
        return

    def checkBuiltInCommands(self, choice):
        if choice == '0':
            self._message = 'Main Menu'
            self.optionsShow()
            return True
        elif choice == '00':
            session.endProgram()
            return True
        elif choice == 'list tools':
            self.prompt(session.toolManager)
            return True
        elif choice == 'list attacks':
            self.prompt(session.attackManager)
            return True
        elif choice == 'list loot files':
            [print(f) for f in session.getLootFiles()]
            self.prompt()
            return True
        elif choice == 'list intel files':
            [print(f) for f in session.getIntelFiles()]
            self.prompt()
            return True
        elif choice == 'list exploit files':
            [print(f) for f in session.getExploitFiles()]
            self.prompt()
            return True
        elif choice == 'list target services':
            [print(s) for s in session.targetHost.getServices()]
            self.prompt()
            return True
        elif choice == 'list target http':
            [print(d) for d in session.targetHost.getHttpDirectories()]
            [print(f) for f in session.targetHost.getHttpFiles()]
            self.prompt()
            return True
        elif choice.startswith('cmd '):
            cmd = choice[4:]
            session.runCmdSimple(cmd)
            self.prompt()
            return True
        elif choice == 'save session':
            session.save()
            self.prompt()
            return True
        elif choice == 'help':
            print('* list tools\n* list attacks\n* list loot files\n* list intel files\n* list exploit files\n* ' +
                'list target services\n* list target http\n* cmd [CMD]\n* save session')
            self.prompt()
            return True

        return False

    def optionsShow(self):
        self._currentMenu = 'options'

        arry = []       
        arry.append('8 = Settings Menu')
        arry.append('9 = Setup Menu')
        arry.append('')
        arry.append(self.TITLE + 'Attach Flow:')
        arry.append('10 = Remote Enumeration   11 = Local Enumeration   12 = Exploit ')
        arry.append('13 = Maintain Control     14 = Specific Tools')
        arry.append('')
        arry.append(self.TITLE + 'Templates:')
        arry.append('20 = Standard Attack, 21 = HTTP Attack, 22 = Windows, 23 = Linux')
        arry.append('')
        arry.append(self.TITLE + 'Workshop:')
        arry.append('40 = Wordlist Creator\t41 = Reverse Shells\t42 = Rainbow Table Generator')
        arry.append('')
        arry.append(self.TITLE + 'Checklist/Run-throughs:')
        arry.append('50 = Network Scan\t51 = HTTP')
        arry.append('')
        
        self.printMenu(arry)

    def optionsHandle(self, choice):
        self._message = ''

        if choice == '8':
            self.settingsShow()
        elif choice == '9':
            self.setupShow()
        elif choice == '10':
            self.enumerationShow()
        elif choice == '11':
            self.internalShow()
        elif choice == '12':
            self.exploitShow()
        elif choice == '13':
            self.maintainShow()
        elif choice == '14':
            self.specificToolShow()
        elif choice == '20':
            Templates.Templates().runStandard()
        elif choice == '21':
            Templates.Templates().runHttp()
        elif choice == '22':
            Templates.Templates().runWindows()
        elif choice == '23':
            Templates.Templates().runLinux()
        elif choice == '40':
            self.prompt('NOT DONE')
        elif choice == '41':
            self.shellsShow()
        elif choice == '42':
            self.prompt('NOT DONE (rtgen – Generate rainbow tables)')
            self.prompt()
        elif choice == '50':
            session.checklistManager.run('NetworkScan')
            self.prompt()
        elif choice == '51':
            session.checklistManager.run('Http')
            self.prompt()
        else:
            self.prompt('Try again')

    def stageShow(self):
        self._currentMenu = 'stageSelection'
        arry = ['1 = Enumeration', '2 = Vulnerability Scanning', '3 = Exploit', '4 = Elevation']
        self.printMenu(arry)

    def stageHandle(self, choice):
        if choice == '1':
            self.enumerationShow()
        elif choice == '2':
            self.prompt('Vulnerability not ready')
        elif choice == '3':
            self.prompt('Exploit not ready')
        elif choice == '4':
            self.prompt('Elevation not ready')
        else:
            self.prompt('Try again')

    def enumerationShow(self):
        self._currentMenu = 'enumerationSelection'

        arry = []

        # Scan options
        index = 1
        scans = session.enumeration.getScanDictionary()
        arry = self.createColumnArray(scans)

        self.printMenu(arry)

    def enumerationHandle(self, choice):
        c = choice
        session.enumeration.run(c)

    def internalShow(self):
        self._currentMenu = 'internalSelection'

        options = session.enumeration.getInternalDictionary()
        arry = self.createColumnArray(options, col = 1)

        self.printMenu(arry)

    def internalHandle(self, choice):
        if choice == '1':
            session.enumeration.localStandardScan()
        elif choice == '2':
            session.enumeration.runLynis()
        elif choice == '3':
            session.enumeration.runPrivesc()
        else:
            self.prompt('Try again')

    def exploitShow(self):
        self._currentMenu = 'exploitSelection'

        arry = []

        options = session.exploit.getExploitDictionary()
        arry = self.createColumnArray(options)

        self.printMenu(arry)

    def exploitHandle(self, choice):
        if choice.isdigit():
            num = int(choice)
            session.exploit.run(num)
        else:
            self.prompt('Try again')

    def maintainShow(self):
        self._currentMenu = 'maintainSelection'

        arry = []

        options = session.maintain.getMaintainDictionary()
        arry = self.createColumnArray(options)

        self.printMenu(arry)

    def maintainHandle(self, choice):
        if choice.isdigit():
            num = int(choice)
            port = '80'
            if num > 0:
                self.prompt('Enter port: ')
                port = input()
                port = port.replace(' ', '')
                if len(port) == 0:
                    port = '80'

                session.maintain.runNetcat(num, port)
        else:
            self.prompt('Try again')
            return

    def specificToolShow(self):
        self._currentMenu = 'specificToolSelection'

        arry = []
        for category in Tool.ToolCategory:
            arry.append(str(category.value) + ' = ' + str(category.name))

        self.printMenu(arry)

    def specificToolHandle(self, choice):
        # Basically just need to set the self._toolCategory
        if choice.isdigit():
            num = int(choice)
            if num > 0:
                self._toolCategory = num
                self.specificToolShow2()
        else:
            self.prompt('Try again')
            return

    def specificToolShow2(self):
        self._currentMenu = 'specificToolSelection2'

        options = {}
        count = 1
        for tool in session.toolManager.getToolsByCategory(self._toolCategory):
            options[count] = str(tool._name)
            count += 1

        if len(options) > 30:
            arry = self.createColumnArray(options, col = 3, padding = 33)
        else:
            arry = self.createColumnArray(options, col = 2)    
        
        arry.append('')
        arry.append('List Info NUM\t\tBack = Tools Main Menu')
        self.printMenu(arry)

    def specificToolHandle2(self, choice):
        choice = choice.replace(' ', '')

        if choice.isdigit():
            num = int(choice)
            if num > 0:
                session.toolManager.run((num - 1), self._toolCategory)
        elif 'listinfo' in choice:
            choice = choice.replace('listinfo', '')
            if choice.isdigit():
                num = int(choice)
                session.toolManager.printInfo((num - 1), self._toolCategory)
            else:
                self.prompt('Try again')
                return
        elif 'parse' in choice:
            choice = choice.replace('parse', '')
            if choice.isdigit():
                num = int(choice)
                tool = session.toolManager.getTool((num - 1), self._toolCategory)
                if tool == None:
                    self.prompt('Unable to find tool')
                else:
                    session.parserManager.parseTool(tool)
            else:
                self.prompt('Try again')
                return
        elif 'back' in choice:
            self.specificToolShow()
        else:
            self.prompt('Try again')
            return
            
    def setupShow(self):
        import Setup
        self._currentMenu = 'setupSelection'
        setup = Setup.Setup()
        
        options = setup.getOptions()

        arry = self.createColumnArray(options)
        self.printMenu(arry)

    def setupHandle(self, choice):
        import Setup
        choice = choice.replace(' ', '')

        if choice.isdigit():
            num = int(choice)
            setup = Setup.Setup()
            
            if num > 0 and num < 30:
                setup.runInstall(num)
            elif num > 0 and num >= 30:
                setup.runOptions(num)
            else:
                self.prompt('Try again')
        else:
            self.prompt('Try again')
            
        return

    def settingsShow(self):
        self._currentMenu = 'settingsSelection'
        
        arry = []
        arry.append(self.TITLE + 'Settings:')
        osList = '1 = ' + self.SETTING + 'Agnostic   ' + self.ENDC + \
                 '2 = ' + self.SETTING + 'Windows   ' + self.ENDC + \
                 '3 = ' + self.SETTING + 'Linux/Unix   ' + self.ENDC + \
                 '4 = ' + self.SETTING + 'Embedded   ' + self.ENDC + \
                 '5 = ' + self.SETTING + 'Printer' + self.ENDC

        if session.getTargetOs() == 'Windows':
            osList = osList.replace('Windows', 'Windows*')
        elif session.getTargetOs() == 'Linux':
            osList = osList.replace('Unix', 'Unix*')
        elif session.getTargetOs() == 'Embedded':
            osList = osList.replace('Embedded', 'Embedded*')
        elif session.getTargetOs() == 'Printer':
            osList = osList.replace('Printer', 'Printer*')
        else:
            osList = osList.replace('Agnostic', 'Agnostic*')
            
        arry.append(osList)
        arry.append('10 ' + self.SETTING + 'Session=' + self.ENDC + session.getSessionId())
        arry.append('11 ' + self.SETTING + 'RHOST=' + self.ENDC + session.getRemoteHost())
        arry.append('12 ' + self.SETTING + 'RPORT=' + self.ENDC + session.getRemotePort())
        arry.append('13 ' + self.SETTING + 'Threads=' + self.ENDC + session.getThreads())
        arry.append('14 ' + self.SETTING + 'USE_SDKS=' + self.ENDC + str(session.USE_SDKS))
        arry.append('')
        arry.append('100 ' + self.SETTING + 'Default Wordlist=' + self.ENDC + os.path.basename(session.getWordlist()))
        arry.append('101 ' + self.SETTING + 'HTTP Wordlist=' + self.ENDC + os.path.basename(session.getHttpWordlist()))
        arry.append('102 ' + self.SETTING + 'Database Wordlist=' + self.ENDC + os.path.basename(session.getDbWordlist()))
        arry.append('103 ' + self.SETTING + 'Default Usernames=' + self.ENDC + os.path.basename(session.getUserlist()))

        self.printMenu(arry)

    def settingsHandle(self, choice):
        choice = choice.replace(' ', '')

        if choice == '1':
            self._message = 'Targeting all Operating Systems'
            session.setTargetOs('Agnostic')
        elif choice == '2':
            self._message = 'Targeting Windows'
            session.setTargetOs('Windows')
        elif choice == '3':
            self._message = 'Targeting Linux/Unix'
            session.setTargetOs('Linux')
        elif choice == '4':
            self._message = 'Targeting Embedded'
            session.setTargetOs('Embedded')
        elif choice == '5':
            self._message = 'Targeting Print Server'
            session.setTargetOs('Printer')
        elif choice.startswith('session='):
            session.load(choice.replace('session=', '').replace(' ', ''))
        elif choice.startswith('rhost='):
            session.setRemoteHost(choice.replace('rhost=', '').replace(' ', ''))
        elif choice.startswith('rport='):
            session.setRemotePort(choice.replace('rport=', '').replace(' ', ''))
        elif choice.startswith('threads='):
            session.setThreads(choice.replace('threads=', '').replace(' ', ''))
        elif choice.startswith('use_sdks='):
            temp = choice.replace('use_sdks=', '').replace(' ', '')
            if temp.lower() == 'true':
                session.USE_SDKS = True
            else:
                session.USE_SDKS = False

        elif choice == '10':
            session.load(choice[2:].strip())
        elif choice == '11':
            session.setRemoteHost(choice[2:].strip())
        elif choice == '12':
            session.setRemotePort(choice[2:].strip())
        elif choice == '13':
            session.setThreads(choice[2:].strip())
        elif choice == '14':
            session.setThreads(choice[2:].strip())

        elif choice.startswith('100'):
            session.setWordlist(choice[3:].strip())
        elif choice.startswith('101'):
            session.setHttpWordlist(choice[3:].strip())
        elif choice.startswith('102'):
            session.setDbWordlist(choice[3:].strip())
        elif choice.startswith('103'):
            session.setUserlist(choice[3:].strip())            
        
        else:
            self.prompt('Try again')

        self.settingsShow()
            
        return
            
    def shellsShow(self):
        self._currentMenu = 'shellsSelection'
        self.printMenu(['Generate Shells:', '1 = Create Shells File' ])

    def shellsHandle(self, choice):
        shellMenu = Shells.ShellsMenu
        if choice == '1':
            Shells.ShellsMenu().run()
        else:
            self.prompt('Try again')  
        return
            
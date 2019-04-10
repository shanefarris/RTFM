
import os
import platform
from colorama import Fore, Back, Style, init

import logging
import ToolManager
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
            self.showMenu()
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
        elif self._currentMenu == 'attackFlowSelection':
            self.attackFlowHandle(choice)
        elif self._currentMenu == 'templateSelection':
            self.templateHandle(choice)
        elif self._currentMenu == 'workshopSelection':
            self.workshopHandle(choice)
        elif self._currentMenu == 'checklistSelection':
            self.checklistHandle(choice)
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
        elif choice == 'list notes':
            [print(s) for s in session.targetHost.getNotes()]
            self.prompt()
            return True
        elif choice == 'list processes':
            for t, p in session.getActiveProcs().items():
                print(str(p.pid) + ': ' + t)
            self.prompt()
            return True
        elif choice.startswith('end process'):
            pid = choice[11:]
            session.endProcess(pid)
            self.prompt()
            return True
        elif choice == 'list checklists':
            [print(c._CategoryName) for i, c in session.checklistManager.getChecklists().items()]
            self.prompt()
            return True
        elif choice.startswith('show checklist '):
            arg = choice[15:]
            if arg.isdigit() == True:
                session.checklistManager.showAllChecklistByIndex(int(arg))
            else:
                session.checklistManager.showAllChecklist(arg)
            self.prompt()
            return True
        elif choice.startswith('cmd '):
            cmd = choice[4:]
            session.runCmdSimple(cmd)
            self.prompt()
            return True
        elif choice.startswith('add note '):
            note = choice[9:]
            session.targetHost.addNotes(note)
            self.prompt()
            return True
        elif choice == 'save session':
            session.save()
            self.prompt()
            return True
        elif choice == 'help':
            print('* list tools\n* list attacks\n* list loot files\n* list intel files\n* list exploit files\n* ' +
                'list target services\n* list target http\n* list notes\n* list processes\n* end process [PID]\n* ' +
                'list checklists\n* show checklist [NAME] or [INDEX]\n* '
                'cmd [CMD]\n* save session\n* add note [NOTE]')
            self.prompt()
            return True

        return False

    def showMenu(self):
        Utility.resetScreen()
                
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
        elif self._currentMenu == 'attackFlowSelection':
            self.attackFlowShow()
        elif self._currentMenu == 'templateSelection':
            self.templateShow()
        elif self._currentMenu == 'workshopSelection':
            self.workshopShow()
        elif self._currentMenu == 'checklistSelection':
            self.checklistShow()

        return

    def optionsShow(self):
        self._currentMenu = 'options'

        arry = []       
        arry.append('8 = Settings Menu')
        arry.append('9 = Setup Menu')
        arry.append('')
        arry.append('10 = Attach Flow')
        arry.append('11 = Templates')
        arry.append('12 = Workshop')
        arry.append('13 = Checklist/Run-throughs')
        arry.append('14 = Specific Tools')
        
        arry.append('')
        
        self.printMenu(arry)

    def optionsHandle(self, choice):
        self._message = ''

        if choice == '8':
            self.settingsShow()
        elif choice == '9':
            self.setupShow()
        elif choice == '10':
            self.attackFlowShow()
        elif choice == '11':
            self.templateShow()
        elif choice == '12':
            self.workshopShow()
        elif choice == '13':
            self.checklistShow()
        elif choice == '14':
            self.specificToolShow()
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
        for category in ToolManager.ToolCategory:
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
        arry.append('14 ' + self.SETTING + 'use_sdks=' + self.ENDC + str(session.USE_SDKS))
        arry.append('15 ' + self.SETTING + 'output_tty=' + self.ENDC + str(session.getOutputTty()))
        arry.append('16 ' + self.SETTING + 'auto_screenshot=' + self.ENDC + str(session.getAutoScreenShot()))
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
        elif choice.startswith('output_tty='):
            session.setOutputTty(choice.replace('output_tty=', '').replace(' ', ''))
        elif choice.startswith('auto_screenshot='):
            temp = choice.replace('auto_screenshot=', '').replace(' ', '')
            if temp.lower() == 'true':
                session.setAutoScreenShot(True)
            else:
                session.setAutoScreenShot(False)
        elif choice.startswith('10'):
            session.load(choice[2:].strip())
        elif choice.startswith('11'):
            session.setRemoteHost(choice[2:].strip())
        elif choice.startswith('12'):
            session.setRemotePort(choice[2:].strip())
        elif choice.startswith('13'):
            session.setThreads(choice[2:].strip())
        elif choice.startswith('14'):
            temp = choice[2:].strip()
            if temp.lower() == 'true':
                session.USE_SDKS = True
            else:
                session.USE_SDKS = False
        elif choice.startswith('15'):
            session.setOutputTty(choice[2:].strip())
        elif choice.startswith('16'):
            temp = choice[2:].strip()
            if temp.lower() == 'true':
                session.setAutoScreenShot(True)
            else:
                session.setAutoScreenShot(False)
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

    def attackFlowShow(self):
        self._currentMenu = 'attackFlowSelection'

        arry = []       
        arry.append(self.TITLE + 'Attach Flow:')
        arry.append('1 = Remote Enumeration')
        arry.append('2 = Local Enumeration')
        arry.append('3 = Exploit ')
        arry.append('4 = Maintain Control')

        self.printMenu(arry)

    def attackFlowHandle(self, choice):
        c = choice
        if choice == '1':
            self.enumerationShow()
        elif choice == '2':
            self.internalShow()
        elif choice == '3':
            self.exploitShow()
        elif choice == '4':
            self.maintainShow()

    def templateShow(self):
        self._currentMenu = 'templateSelection'

        arry = []       
        arry.append(self.TITLE + 'Templates:')
        arry.append('1 = Standard Attack')
        arry.append('2 = HTTP Attack')
        arry.append('3 = Windows ')
        arry.append('4 = Linux')

        self.printMenu(arry)

    def templateHandle(self, choice):
        c = choice
        if choice == '1':
            Templates.Templates().runStandard()
        elif choice == '2':
            Templates.Templates().runHttp()
        elif choice == '3':
            Templates.Templates().runWindows()
        elif choice == '4':
            Templates.Templates().runLinux()
        return

    def workshopShow(self):
        self._currentMenu = 'workshopSelection'

        arry = []       
        arry.append(self.TITLE + 'Workshop:')
        arry.append('1 = Wordlist Creator')
        arry.append('2 = Reverse Shells')
        arry.append('3 = Rainbow Table Generator')

        self.printMenu(arry)
        return

    def workshopHandle(self, choice):
        c = choice
        if choice == '1':
            self.prompt('NOT DONE')
        elif choice == '2':
            self.shellsShow()
        elif choice == '3':
            self.prompt('NOT DONE (rtgen – Generate rainbow tables)')
            self.prompt()
        return

    def checklistShow(self):
        self._currentMenu = 'checklistSelection'

        arry = []       
        arry.append(self.TITLE + 'Checklists and Notes:')

        for i, item in session.checklistManager.getChecklists().items():
            arry.append(str(i) + ' = ' + item._CategoryName)

        self.printMenu(arry)
        return

    def checklistHandle(self, choice):
        if choice.isnumeric() == True:
            index = int(choice)
            item = session.checklistManager.getChecklists().get(index)
            if item == None:
                print('Could not find list.')
                return 

            print(item._CategoryName)
            session.checklistManager.run(item._CategoryName)
            self.checklistShow()
        return

            

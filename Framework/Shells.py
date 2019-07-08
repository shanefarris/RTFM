# listeners
# nc -l -p 5232 -vvv


import os
import platform
import base64
from Session import *
from MenuBase import *

class Shell:
    def __init__(self, name, desc, codeLines):
        self._name = name
        self._desc = desc
        self._lines = codeLines
        self._base64 = base64.b64encode(bytes(codeLines, 'utf-8'))
        self._encrypted = base64.b64encode(bytes(codeLines, 'utf-8'))

    def __repr__(self):
        return 'Shell'

    def __str__(self):
        return 'Name: ' + str(self._name) + '\nDescription: ' + str(self._desc) + '\nCode: ' + '\n' + self._lines #+ \
            #'\nBase64: ' + str(self._base64) + '\nEncrypted: ' + str(self._encrypted) + '\n'

class ShellsMenu(MenuBase):

    def __init__(self):
        self._shells = { }

        shellsFile = './reverse_shells.json'

        data = None
        with open(shellsFile, encoding="utf8") as f:
            data = json.load(f)

        index = 1
        for obj in data:
            try:
                shell = Shell(obj['name'], obj['description'], obj['code'])
                self._shells[index] = shell
                index += 1
            except Exception as e:
                logging.exception(type(e))
        return

    def run(self, index):
        print('Enter the IP to reverse to: ', end = '')
        host = input()

        print('Enter the port: ', end = '')
        port = input()

        self.generateShell(index, host, port)

        return self.prompt('nc -l -p PORT -vvv')

    def runAll(self):
        print('Enter the IP to reverse to: ', end = '')
        host = input()

        print('Enter the port: ', end = '')
        port = input()

        self.generateAllShells(host, port)
        self.createShellsFile()

        return self.prompt('nc -l -p PORT -vvv')

    def getShells(self):
        return self._shells

    def generateAllShells(self, host, port):
        for shell in self._shells:
            shell._lines = shell._lines.replace('${target}', host)
            shell._lines = shell._lines.replace('${port}', port)

        try:
            with open(session.getExploitDir() + '/shells.txt','w') as outfile:
                for shell in self._shells:
                    outfile.write(str(shell) + '\n\n')

        except Exception as e:
            print(e)
            logging.exception(type(e))

        return

    def generateShell(self, index, host, port):
        if index > len(self._shells):
            return

        shell = self._shells[index]
        shell._lines = shell._lines.replace('${target}', host)
        shell._lines = shell._lines.replace('${port}', port)

        try:
            with open(session.getExploitDir() + '/shell.txt','w') as outfile:
                outfile.write(str(shell))

        except Exception as e:
            print(e)
            logging.exception(type(e))

        return

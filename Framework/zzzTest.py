
import json
from Session import *
import Attack
from pprint import pprint
'''
infile = open('searchsploit.txt','r').readlines()
with open('output.txt','w') as outfile:
    for index,line in enumerate(infile):
        if index == 0 or index == 1:
            continue
        elif index == 2:
            outfile.write('[')
        elif line == '}\n':
            line = '},\n'
            outfile.write(line)
        else:
            outfile.write(line)

    outfile.write(']')
'''
session.init()
data = None
with open('searchsploit_nmap_quick.xml.json_formatted.txt') as f:
    data = json.load(f)

for obj in data:
    #print(obj)
    print('')

    if len(obj['RESULTS_EXPLOIT']) > 0:
        service = obj['SEARCH']
        for result in obj['RESULTS_EXPLOIT']:
            name = result['Title']
            id = result['EDB-ID']
            date = result['Date']
            type = result['Type']
            platform = result['Platform']
            file = result['Path']

            session.attackManager.addAttack(Attack.Attack(name, file, '', service, id, date, type, platform))

for attack in session.attackManager.getAttacks():
    print(attack)
#print(data)







'''
for host, services in session.targetHosts:
                for service in services:
                    terms = service.getName() + ' ' + service.getVersion()
                    if host == '127.0.0.1' or host == 'localhost':
                        terms += ' local'

                    outFile = exploitDir + '/' + service.getPort() + '_standard_template.json'
                    cmd = 'searchsploit --json ' + terms + ' | tee ' + outFile
                    session.runThreadedCmd(cmd, 'Searchsploit', None, self.parseSearchSploit, outFile)
'''
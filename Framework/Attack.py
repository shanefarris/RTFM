
import Session
import TargetHost

class Attack:
    def __init__(self, name, file, description, service, id, date, type, platform):
        self._name = name
        self._file = file
        self._desc = description
        self._service = service
        self._id = id
        self._date = date
        self._type = type
        self._platform = platform

    def __repr__(self):
        return 'Attack'

    def __str__(self):
        return 'Name: ' + str(self._name) + '\nFile: ' + str(self._file) + '\nDescription: ' + str(self._desc) + '\nServices: ' + str(self._service) + '\nID: ' + \
            str(self._id) + '\nDate: ' + str(self._date)  + '\nType: ' + str(self._type)  + '\nPlatform: ' + str(self._platform)

    def getName(self):
        return self._name

    def getFile(self):
        return self._file

    def getDesc(self):
        return self._desc

    def getService(self):
        return self._service

    def getId(self):
        return self._id

    def getDate(self):
        return self._date

    def getType(self):
        return self._type

    def getPlatform(self):
        return self._platform

    def getPath(self):
        return self._path

class AttackManager:
    def __init__(self):
        self._attacks = []

    def __repr__(self):
        return 'AttackManager'

    def __str__(self):
        ret = ''
        for attack in self._attacks:
            ret = ret + str(attack) + '\n\n'

        return ret

    def getAttacks(self):
        return self._attacks

    def addAttack(self, attack):
        try:
            for a in self._attacks:
                if a.getId() == attack.getId():
                    return False;

            self._attacks.append(attack)
        except Exception as e:
            print(e)

        return True
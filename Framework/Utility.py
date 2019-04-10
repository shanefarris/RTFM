
def getAllFiles(dir):
    arry = []
    for root, directories, filenames in os.walk(dir):
        for filename in filenames: 
            arry.append(path.join(root,filename))

    return arry

def getTimestamp():
    import time
    import datetime

    timestamp = time.time()
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def resetScreen():
    import os
    import platform

    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('reset')
                                 

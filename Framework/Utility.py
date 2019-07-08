
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
                                 
def getLocalIpAddress():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def getAllFiles(dir):
    arry = []
    for root, directories, filenames in os.walk(dir):
        for filename in filenames: 
            arry.append(path.join(root,filename))

    return arry



def writeFile(pLogical, pPhysical, path):
    f = open(path, "a")
    
    for i in range(0, min(len(pPhysical), len(pLogical))):
        f.write( "(" + str(pPhysical[i]) + "," + str(pLogical[i]) + ") ")

    f.write("\n")
    f.close()

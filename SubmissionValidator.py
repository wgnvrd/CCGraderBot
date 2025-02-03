    
import os


def checkDirec(direcName, fileList):
    dirCheck = True
    comment = ""
    if not os.path.isdir(os.path.join('testing',direcName)):

        return False, "Missing Directory Name: " + direcName
    else:
        
        for p in fileList:
            if not os.path.exists(os.path.join('.\\testing',p)):
                dirCheck = False
                comment += "\nMissing File: " + p
    return dirCheck, comment
                
 
   
            
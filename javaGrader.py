import os
import subprocess

import junitparser


def jgrade(test, source, Scores):
    #Compile Code
    subprocess.run(["javac","-d", "out", "-cp", "lib\junit-platform-console-standalone-1.11.4.jar",test,source])
    #Run Code
    subprocess.run(['java', '-jar', '.\lib\junit-platform-console-standalone-1.11.4.jar', 'execute', '--class-path', '.\\out\\', '--scan-class-path', '--reports-dir=results'])
    data = junitparser.JUnitXml.fromfile(os.path.join("results", "TEST-junit-jupiter.xml"))
    commentDict = {key: [] for key in list(Scores.keys())}
    comment = "\n"
    score = 0
    for case in data:
        category = case.system_out.split()[-1]
        
        if category not in Scores.keys():
            comment+= "Error " + case.name + "not testable: " + category + "\n"
        else:
            #JUnit only creates a result if theres an error or a failure -- so if there's no result its a success
            if case.result:
                if isinstance(case.result[0], junitparser.Failure):
                    commentDict[category].append("\n FAILURE: "+ case.name)
                    Scores[category] = 0
                elif isinstance(case.result[0], junitparser.Error):
                    commentDict[category].append("\n ERROR: "+ case.name)
                    Scores[category] = 0

            else:
                commentDict[category].append("\n SUCCESS: " + case.name)
    for key in commentDict.keys():
        comment += key + " tests"
        for com in commentDict[key]:
            comment += com
        comment += "\n"
    for val in Scores.values():
        score += val
    return score, comment

            

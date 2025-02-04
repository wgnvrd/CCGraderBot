import os
import subprocess

import junitparser

from pathlib import Path

# remove this later
import configparser
from TestModule import TestModule
from CanvasHelper import get_submission
from zipfile import ZipFile

class JUnitModule(TestModule):
    def __init__(self,test,source,Scores,max_score):
        super().__init__(max_score)
        self.test = test
        self.source = source
        self.Scores = Scores

    def get_score(self):
        return self.score
    
    def get_feedback(self):
        return self.feedback
    
    def run(self):
        #Compile Code
        subprocess.run(["javac","-d", "out", "-cp", "lib\junit-platform-console-standalone-1.11.4.jar",self.test,self.source])
        print("compiled code")
        #Run Code
        subprocess.run(['java', '-jar', '.\lib\junit-platform-console-standalone-1.11.4.jar', 'execute', '--class-path', '.\\out\\', '--scan-class-path', '--reports-dir=results'])
        print("run code")
        print(os.getcwd())
        data = junitparser.JUnitXml.fromfile(os.path.join("results", "TEST-junit-jupiter.xml"))
        commentDict = {key: [] for key in list(self.Scores.keys())}
        for case in data:
            category = case.system_out.split()[-1]
            
            if category not in self.Scores.keys():
                self.feedback+= "Error " + case.name + "not testable: " + category + "\n"
            else:
                #JUnit only creates a result if theres an error or a failure -- so if there's no result its a success
                if case.result:
                    if isinstance(case.result[0], junitparser.Failure):
                        commentDict[category].append("\n FAILURE: "+ case.name)
                        self.Scores[category] = 0
                    elif isinstance(case.result[0], junitparser.Error):
                        commentDict[category].append("\n ERROR: "+ case.name)
                        self.Scores[category] = 0

                else:
                    commentDict[category].append("\n SUCCESS: " + case.name)
        for key in commentDict.keys():
            self.feedback += key + " tests"
            for com in commentDict[key]:
                self.feedback += com
            self.feedback += "\n"
        for val in self.Scores.values():
            self.score += val

if __name__ == "__main__":
    print("start")
    config = configparser.ConfigParser()
    config.read('config_files/Recall.ini')
    values = config['DEFAULT']
    course_id = values["CourseId"]
    assign_id = values['AssignId']
    #UNZIP TEST
    sub = get_submission(course_id, assign_id, userId=24388)
    for attachment in sub.attachments:
        print(attachment.display_name)
        path = 'testing\\' + attachment.display_name
        
        print("Downloading attachments...")
        attachment.download(path)
        print(path)

    with ZipFile(path) as zip:
        print(os.getcwd())
        zip.extractall(Path("testing"))
    
    testPath = "testing\\" + values["TestFilePath"]
    print(testPath)
    srcFiles = "testing\\" + values["FilePath"]
    print(srcFiles)
    jum = JUnitModule(testPath,srcFiles,dict([(k, 1) for k in config["JAVA"]["TestCases"].split()]),4)
    print(str(jum.get_score()) + ", " + str(jum.get_feedback()))
    print("made jum")
    jum.run()
    print(jum.get_score(),jum.get_feedback())      

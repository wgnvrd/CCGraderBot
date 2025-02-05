import os
import subprocess

import junitparser

from pathlib import Path

from glob import glob

# remove this later
import configparser
from test_module import TestModule
from CanvasHelper import get_submission
from zipfile import ZipFile

class JavaDocAggregatorModule(TestModule):
    def __init__(self,source):
        self.source = source
        self.feedback = ""
    
    def run(self):
        srcFiles = os.path.join(".","testing",self.source)
        # # Parse the Java file
        # parser = javadocparser.JavadocParser()
        # javadoc = parser.parse_file("YourJavaFile.java")

        # # Access the extracted Javadoc comments
        # for class_javadoc in javadoc.classes:
        #     print(f"Class: {class_javadoc.name}")
        #     print(f"Description: {class_javadoc.description}")

        #     for method_javadoc in class_javadoc.methods:
        #         print(f"Method: {method_javadoc.name}")
        #         print(f"Description: {method_javadoc.description}")
        #         # Access parameters, return values, and other details

        
        # source_dir = Path("./testing/first_assignment/src/")
        # files = " ".join(str(p) for p in source_dir.glob("*"))

        def get_feedback():
            return self.feedback

        with open(srcFiles, "r") as file:
            docstart = "/**"
            docend = "*/"
            self.printer = False
            # lines = file.readlines()
            # print(type(lines))
            line = file.readline()
            while line:
                if docstart in line:
                    self.printer = True
                    line = file.readline()
                elif docend in line:
                    line = file.readline().strip()
                    self.feedback += line
                    print(line + "\n")
                    self.printer = False
                    line = file.readline()
                    # print("Type: " + str(type(line)) + ", " + str(line),end="")
                elif self.printer is True:
                    line = line.strip()[2:]
                    print(line)#.strip())
                    line = file.readline()
                else:
                    line = file.readline()
        
        # files = glob(self.source)
        
        # #Compile Code
        # subprocess.run(["javac","-d", "out", "-cp", os.path.join("lib","junit-platform-console-standalone-1.11.4.jar"),self.test,*files])# self.source])
        
        # #Run Code
        # subprocess.run(['java', '-jar', os.path.join("lib","junit-platform-console-standalone-1.11.4.jar"), 'execute', '--class-path', './out/', '--scan-class-path', '--reports-dir=results'])
        # data = junitparser.JUnitXml.fromfile(os.path.join("results", "TEST-junit-jupiter.xml"))
        # commentDict = {key: [] for key in list(self.Scores.keys())}
        # for case in data:
        #     category = case.system_out.split()[-1]
            
        #     if category not in self.Scores.keys():
        #         self.feedback+= "Error " + case.name + "not testable: " + category + "\n"
        #     else:
        #         #JUnit only creates a result if theres an error or a failure -- so if there's no result its a success
        #         if case.result:
        #             if isinstance(case.result[0], junitparser.Failure):
        #                 commentDict[category].append("\n FAILURE: "+ case.name)
        #                 self.Scores[category] = 0
        #             elif isinstance(case.result[0], junitparser.Error):
        #                 commentDict[category].append("\n ERROR: "+ case.name)
        #                 self.Scores[category] = 0

        #         else:
        #             commentDict[category].append("\n SUCCESS: " + case.name)
        # for key in commentDict.keys():
        #     self.feedback += key + " tests"
        #     for com in commentDict[key]:
        #         self.feedback += com
        #     self.feedback += "\n"
        # for val in self.Scores.values():
        #     self.score += val

if __name__ == "__main__":
    
    # config = configparser.ConfigParser()
    # config.read(os.path.join("config_files","Recall.ini"))
    # values = config['DEFAULT']
    # course_id = values["CourseId"]
    # assign_id = values['AssignId']
    # #UNZIP TEST
    # sub = get_submission(course_id, assign_id, userId=24388)
    # for attachment in sub.attachments:
    #     print(attachment.display_name)
    #     path = os.path.join('testing', attachment.display_name)
        
    #     print("Downloading attachments...")
    #     attachment.download(path)

    # with ZipFile(path) as zip:
    #     print(os.getcwd())
    #     zip.extractall(Path("testing"))
    
    srcFiles = Path("test_doc.java")
    jdam = JavaDocAggregatorModule(srcFiles)
    jdam.run()
    # print(str(jdam.get_score()) + " points\nFeedback:\n" + str(jdam.get_feedback()))      

import os
import subprocess

import junitparser

from pathlib import Path

from glob import glob
# remove this later
import configparser
from test_input_wrapper import TestInputWrapper
from test_module import TestModule
from CanvasHelper import get_submission
from zipfile import ZipFile
"""
Module for running JUnit Tests
"""
class JUnitModule(TestModule):
    """
    max_score - max score earnable with this test
    test_types - Subcategories of test and the value associated with each subcategory
    """
    def __init__(self,max_score,test,test_types, fatal = False):
        super().__init__()
        
        self.max_score = max_score
        self.test = Path("testing") /Path(test)
        self.fatal = fatal

        self.Scores = test_types
        self.feedback += "\n UNIT TESTS"

    def get_score(self):
        return self.score
    
    def get_feedback(self):
        return self.feedback
    
    def run(self, working_directory):
        # source_dir = Path("./testing/first_assignment/src/")
        # files = " ".join(str(p) for p in source_dir.glob("*"))

        
        #files = glob(self.source)
        #Compile Code
        #Run Code
        """
        Code Should be compiled before this module is ran -- if not, will error out
        """
        subprocess.run(['java', '-jar', os.path.join("..","..","lib","junit-platform-console-standalone-1.11.4.jar"), 'execute', '--class-path', './out/', '--scan-class-path', '--reports-dir=results'], cwd = working_directory.path)
        data = junitparser.JUnitXml.fromfile(os.path.join(working_directory.path, "results", "TEST-junit-jupiter.xml"))
        
        """
        Parses through JUnit output file to find which tests failed, and which tests passed
        """
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
                        if self.fatal:
                            self.testing_done = True
                    elif isinstance(case.result[0], junitparser.Error):
                        commentDict[category].append("\n ERROR: "+ case.name)
                        self.Scores[category] = 0
                        if self.fatal:
                            self.testing_done = True

                else:
                    commentDict[category].append("\n SUCCESS: " + case.name)
        """
        Parses through each category and adds the respective points for each successful category
        """
        for key in commentDict.keys():
            self.feedback += "\n" + key + " tests"
            for com in commentDict[key]:
                self.feedback += com
            self.feedback += "\n"
        for val in self.Scores.values():
            self.score += val





"""
Testing Main Code
"""
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(os.path.join("config_files","Recall.ini"))
    values = config['DEFAULT']
    course_id = values["CourseId"]
    assign_id = values['AssignId']
    #UNZIP TEST
    sub = get_submission(course_id, assign_id, userId=24388)
    for attachment in sub.attachments:
        print(attachment.display_name)
        path = os.path.join('testing', attachment.display_name)
        
        print("Downloading attachments...")
        attachment.download(path)

    with ZipFile(path) as zip:
        print(os.getcwd())
        zip.extractall(Path("testing"))
    
    testPath = os.path.join("./testing", values["TestFilePath"])
    srcFiles = os.path.join("./testing", values["FilePath"])
    jum = JUnitModule(testPath,srcFiles,dict([(k, 1) for k in config["JAVA"]["TestCases"].split()]),4)
    jum.run()
    print(str(jum.get_score()) + " points\nFeedback:\n" + str(jum.get_feedback()))      

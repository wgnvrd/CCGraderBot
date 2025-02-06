import argparse
import configparser, os, pathlib, junitparser
from typing import List
import subprocess
from CanvasHelper import  grade_submission, get_submission
from zipfile import ZipFile

from pathlib import Path
from SubmissionValidator import checkDirec
import UnzipDirectory
import ValidateDirectory
import javaDocModule
from javaGrader import jgrade 
import JUnitModule
import tomlkit

# Kazu's modified version of Kiernan's autograder that's 
# attempting to use the modularized structure that takes in toml files
class Autograder():
    def __init__(self, course_id):
        self.course_id = course_id
    def get_ungraded_assignments():
        pass
    
    def poll_canvas():
        pass

#Example of Grading from a file
""" 
userId is the id of the submission to be graded
config is the config file for the specific assignment -- i think this would
be in some sort of database/dictionary thing attached to the assignment id
"""
# grade(43491, 155997, 24388, 'config_files/Recall.ini')
# grade(43491, 155997, 24388, 'config_files/autograder.toml')
def grade(courseId, assignmentId, userId, configFile):
    url = "https://canvas.coloradocollege.edu/api/v1/"
    #Critical Information for finding and testing the assignment stored in config file
    #How many of these attributes would be best to be on command line vs written into file?
    #config = configparser.ConfigParser()
    #config.read(configFile)
    #values = config['DEFAULT']
    #course_id = values["CourseId"]
    #assign_id = values['AssignId']
    #testPath = "testing\\" + values["TestFilePath"]
    #srcFiles = "testing\\" + values["FilePath"]

    config = tomlkit.read(os.path.join("config_files", "danielle-s-cp222-43491"))
    language = config[assignmentId]["language"]

    #We add up the score as we progress through testing
    score = 0
    #Start Comment
    comment = 'RESULTS FOR ' + config[assignmentId]["assignment-name"] + "\n"
    #Dictionary of test categories to record test results
    

# def grade(courseId, assignmentId, userId, configFile):
#     url = "https://canvas.coloradocollege.edu/api/v1/"
#     #Critical Information for finding and testing the assignment stored in config file
#     #How many of these attributes would be best to be on command line vs written into file?
#     config = tomlkit.read(configFile)
#     values = config['DEFAULT']
#     course_id = values["CourseId"]
#     assign_id = values['AssignId']
#     testPath = "testing\\" + values["TestFilePath"]
#     srcFiles = "testing\\" + values["FilePath"]
#     #We add up the score as we progress through testing
#     score = 0
#     #Start Comment
#     comment = 'RESULTS FOR ' + values["DirectoryName"] + "\n"
#     #Dictionary of test categories to record test results
#     Scores = dict([(k, 1) for k in config["JAVA"]["TestCases"].split()])



    #UNZIP TEST
    sub = get_submission(courseId, assignmentId, userId)
    testingPath = Path("testing")
    for attachment in sub.attachments:
        print(attachment.display_name)
        zipPath = testingPath / attachment.display_name
        
        print("Downloading attachments...")
        attachment.download(zipPath)
        print(zipPath)

    ###ASSEMBLE TEST MODULES###
    testcount = 0
    tests = []
    for entry in config[assignmentId+'.pipeline']['steps']:
        match(entry["type"]):
            case("unzip"):
                tests[testcount] = UnzipDirectory.UnzipDirectory(zipPath, testingPath)
                testcount += 1
            case("directory"):
                root = testingPath / "first_assignment"
                plist = List[Path]
                for f in entry['paths']:
                    plist.append(Path(f))
                tests[testcount] = ValidateDirectory.ValidateDirectory(0.5, root,plist)
                testcount += 1
            case("javadoc"):
                plist = List[Path]
                for f in entry["paths"]:
                    plist.append(root / f)
                tests[testcount] = javaDocModule.javaDocModule(0.5, plist)
            case("unit-tests"):
                #For some reason my brain is not parsing how to fit this format onto the JUnit tests right now, I can come back to this later tonight
                tests[testcount] = JUnitModule.JUnitModule(entry["path"],)



    #DIRECTORY CHECK TEST
    #results = checkDirec(values['DirectoryName'],config["DEFAULT"]["MandatoryFiles"].split())
   # print(results)
    #if not results[0]:
    #    comment += results[1]
    #    os.remove(path)
     #   grade_submission(get_submission(course_id, assign_id,userId),score, comment)
     #   return -1
   # score += 1

    
    #UNIT TESTS
    match(values["Language"]):
        case "Java":
            JUnitModule = JUnitModule(testPath,srcFiles,Scores,4)
            results = [JUnitModule.get_score(),JUnitModule.get_comment()]
        case "Python":
            results
        case "_":
            print("Error: Language not properly configured or supported")
            return -1
        
    score += results[0]
    comment += results[1]

    #END TO END TESTS GO HERE


    os.remove(path)
    grade_submission(get_submission(course_id, assign_id,userId),score, comment)

def writeConfig(courseId, assignId, testFilePath, language):
    config = configparser.ConfigParser()
    config['DEF'] = {
        'Language' : language,
        'CourseId' : courseId,
        'AssignId' : assignId,
        'TestFile' : testFilePath}
    
    config.write(open(os.path.join('config_files', "testCon.ini"),'w'))




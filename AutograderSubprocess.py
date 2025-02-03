import argparse
import configparser, os, pathlib, junitparser
import subprocess
from CanvasHelper import get_submission, grade_submission#,get_assignment, get_course, 
from zipfile import ZipFile 

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
#
def grade(userId, configFile):
    url = "https://canvas.coloradocollege.edu/api/v1/"
    #Critical Information for finding and testing the assignment stored in config file
    #How many of these attributes would be best to be on command line vs written into file?
    config = configparser.ConfigParser()
    config.read(configFile)
    values = config['DEFAULT']
    course_id = values["CourseId"]
    assign_id = values['AssignId']
    testPath = "testing\\" + values["TestFilePath"]
    srcFiles = "testing\\" + values["FilePath"]
    #We add up the score as we progress through testing
    score = 0
    #Start Comment
    comment = 'RESULTS FOR ' + values["DirectoryName"] + "\n"
    #Dictionary of test categories to record test results
    Scores = dict([(k, 1) for k in config["JAVA"]["TestCases"].split()])


    #Our extract code isn't working for me right now? I'm assuming its in development
    sub = get_submission(course_id, assign_id, userId)
    for attachment in sub.attachments:
        path = 'testing\\' + attachment.display_name
        
        print("Downloading attachments...")
        attachment.download(path)

    with ZipFile(path) as zip:
        zip.extractall( path = ".\\testing")

    #Verify Directory
    dirCheck = True
    if not os.path.isdir(os.path.join('testing',values['DirectoryName'])):
        score = 0
        comment += "Missing Directory Name: first_assignment"
        grade_submission(get_submission(course_id, assign_id,userId),score, comment)
        os.remove(path)
        return -1
    else:
        filePaths = config["DEFAULT"]["MandatoryFiles"]
        for p in filePaths.split():
            if not os.path.exists(os.path.join('.\\testing',p)):
                comment += "\nMissing File: " + p
                dirCheck = False
    if not dirCheck:
        grade_submission(get_submission(course_id, assign_id,userId),score, comment)
        os.remove(path)
        os.remove(os.path.join("testing", values['DirectoryName']))
        return -1
            
    score +=1
    
    
    #First compile the Junit test
    
    #Hardcoded Compile for now -- format is "javac" "-d" "*OUTPUT_DIRECTORY*" "-cp" "JARFILE" "FILESTOBECOMPILED"
    subprocess.run(["javac","-d", "out", "-cp", "lib\junit-platform-console-standalone-1.11.4.jar",testPath,srcFiles])
    subprocess.run(['java', '-jar', '.\lib\junit-platform-console-standalone-1.11.4.jar', 'execute', '--class-path', '.\\out\\', '--scan-class-path', '--reports-dir=results'])
                    
    data = junitparser.JUnitXml.fromfile(os.path.join("results", "TEST-junit-jupiter.xml"))
    for case in data:
        category = case.system_out.split()[-1]
        
        if category not in Scores.keys():
            comment+= "Error " + case.name + "not testable: " + category + "\n"
        else:
            if case.result:
                if isinstance(case.result[0], junitparser.Failure):
                    comment += "\n FAILURE: "+ case.name + "\n"
                    Scores[category] = 0
                elif isinstance(case.result[0], junitparser.Error):
                    comment += "\n ERROR: "+ case.name + "\n"
                    Scores[category] = 0

            else:
                comment += "\n SUCCESS: " + case.name + "\n"

    for val in Scores.values():
        score += val
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


    

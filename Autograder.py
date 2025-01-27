import argparse
import configparser, os, pathlib, junitparser
from CanvasAPI import grade_assignment, extract_zip, get_submission

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
    config = configparser.ConfigParser()
    config.read(configFile)
    values = config['DEFAULT']
    course_id = values["CourseId"]
    assign_id = values['AssignId']
    score = 0
    comment = 'RESULTS FOR ' + values["FileName"]

    

    #Right here is where we would run whatever testing file is in the config 
    #I'm just gonna hard code the score/comment that would return for this example

    
    #Verify Directory
    sub = get_submission(course_id, assign_id, userId)["attachments"][0]["url"]
    extract_zip(sub)
    if not os.path.isdir(os.path.join('testing',values['FileName'])):
        score = 0
        comment = "Improper Directory Structure/Name"
    else:
        score +=1
        
    """
    INSERT CODE FOR TESTING HERE
    """
     
     #Hard coding for example purposes
    data = junitparser.JUnitXml.fromfile(os.path.join("testing", "bad.xml"))
    #Iterate through every type of test
    for suite in data:
        fail = False
        comment += "\n\n " + suite.name
        for case in suite:
            #Check for failures
            if case.result:
                print(case.result)
                if isinstance(case.result[0], junitparser.Failure):
                    comment += "\n FAILURE: "+ case.name
                    fail = True
            else:

                comment += "\n SUCCESS: " + case.name
            #If there's no failures -- points go up
        if not fail:
            score += 1

                    



    grade_assignment(values["CourseId"], values["AssignId"],userId, score, my_comment=comment)

def writeConfig(courseId, assignId, testFilePath, language):
    config = configparser.ConfigParser()
    config['DEF'] = {
        'Language' : language,
        'CourseId' : courseId,
        'AssignId' : assignId,
        'TestFile' : testFilePath}
    
    config.write(open(os.path.join('config_files', "testCon.ini"),'w'))


    

# import argparse
import os#, pathlib, 
import time
from pathlib import Path
from random import randint

import junitparser
import configparser

from CanvasHelper import (
    grade_submission, 
    get_submission,
    get_ungraded_submissions
)
from canvasapi import Canvas
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CANVAS_ACCESS_TOKEN")
API_URL = "https://canvas.coloradocollege.edu/"

class Autograder():
    def __init__(self, course_id):
        self.canvas = Canvas(API_URL, API_KEY)
        self.course = self.canvas.get_course(course_id)
        self.ungraded_assignments = set()
    
    # def submission_is_graded(self, submission: Submission):
    #     return submission.grade and submission.grade_matches_current_submission
    
    # def submission_is_resubmission(self, submission: Submission):
    #     return submission.attempt > 1

    # def get_ungraded_submissions(self, assignment: Assignment):
    #     submissions = assignment.get_submissions()
    #     return [s for s in submissions if not self.submission_is_graded(s)]

    # def get_ungraded_assignments(self):
    #     assignments = self.course.get_assignments()
    #     ungraded_submissions = []
    #     for assignment in assignments:
    #         ungraded_submissions += self.get_ungraded_submissions(assignment)

    def poll(self, condition, interval: float):
        while True:
            value = condition()
            if value:
                return value
            time.sleep(interval)

    def poll_canvas(self, assignment_id):
        dest = Path('testing/downloads/')
        while True:
            print("Looking for ungraded assignments...")
            assignment = self.course.get_assignment(assignment_id)
            ungraded_submissions = self.poll(lambda: get_ungraded_submissions(assignment=assignment), interval=10)
            for submission in ungraded_submissions:
                print("Downloading attachments...")
                for attachment in submission.attachments:
                    path = dest / attachment.display_name
                    if not path.exists():
                        attachment.download(path)
                    # Test would probably be run here
                print("Assigning automatic grade to submission")
                score = randint(1, 4)
                submission.edit(submission={'posted_grade': score}, comment={'text_comment': f"Attempt {submission.attempt} grade: {score}"})

            
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

    grade_submission(values["CourseId"], values["AssignId"],userId, score, my_comment=comment)

def writeConfig(courseId, assignId, testFilePath, language):
    config = configparser.ConfigParser()
    config['DEF'] = {
        'Language' : language,
        'CourseId' : courseId,
        'AssignId' : assignId,
        'TestFile' : testFilePath}
    
    config.write(open(os.path.join('config_files', "testCon.ini"),'w'))


if __name__ == "__main__":
    autograder = Autograder(43491)
    autograder.poll_canvas(155997)

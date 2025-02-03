# import argparse
import os#, pathlib, 
import time
from pathlib import Path
from random import randint

import junitparser
import configparser

from CanvasHelper import (
    get_canvas_api,
    get_submission,
    grade_submission, 
    get_ungraded_submissions
)

class Autograder():
    def __init__(self, course_id):
        self.canvas = get_canvas_api()
        self.course = self.canvas.get_course(course_id)
        self.ungraded_assignments = set()
    
    # def submission_is_graded(self, submission: Submission):
    #     return submission.grade and submission.grade_matches_current_submission
    
    # def submission_is_resubmission(self, submission: Submission):
    #     return submission.attempt > 1

    # def get_ungraded_submissions(self, assignment: Assignment):
    #     submissions = assignment.get_submissions()
    #     return [s for s in submissions if not self.submission_is_graded(s)]

    def get_ungraded_assignment_submissions(self):
        """
        Checks all open assignments for ungraded submissions.
        """
        assignments = self.course.get_assignments()
        ungraded_submissions = []
        for assignment in assignments:
            ungraded_submissions += get_ungraded_submissions(assignment)
        return ungraded_submissions

    def poll(self, func, condition=lambda x: x, interval: float=10):
        """
        Given a function 
        """
        while True:
            value = func()
            if condition(value):
                return value
            time.sleep(interval)

    def poll_canvas(self):
        dest = Path('testing/downloads/')
        while True:
            print("Looking for ungraded assignments...")
            # assignment = self.course.get_assignment(assignment_id)
            ungraded_submissions = self.poll(lambda: self.get_ungraded_assignment_submissions())
            for submission in ungraded_submissions:
                print(submission) 
                print("Downloading attachments")
                for attachment in submission.attachments:
                    print("Ungraded submission ID", submission.id)
                    path = dest / attachment.display_name
                    # if not path.exists():
                    #     print("Downloading attachments...")
                    #     attachment.download(path)
                #     # Test would probably be run here
                score = randint(1, 4)
                print(f"Automatically assigning random grade of {score} to submission")
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
    # sub = get_submission(course_id, assign_id, userId)["attachments"][0]["url"]
    # extract_zip(sub)
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

    submission = get_submission(values["CourseId"], values["AssignId"],userId)
    grade_submission(submission, score, my_comment=comment)

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
    autograder.poll_canvas()

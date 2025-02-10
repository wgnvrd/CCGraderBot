# import argparse
import os#, pathlib, 
import time
from pathlib import Path
from random import randint

from canvasapi.submission import Submission
from canvasapi.canvas_object import CanvasObject
from canvasapi.exceptions import ResourceDoesNotExist
import configparser
from dotenv import load_dotenv
import junitparser
from slugify import slugify
from test_runner import TestRunner
from SLURMRunner import SLURMRunner

from CanvasHelper import (
    get_canvas_api,
    get_submission,
    grade_submission, 
    get_ungraded_submissions
)
# from ConfigHandler import ConfigHandler
# from ValidateDirectory import ValidateDirectory
# from UnzipDirectory import UnzipDirectory

canvas = get_canvas_api()
load_dotenv(".env")

AUTOGRADE_DIR = Path("/home/i_wagenvoord/autograding/downloads")

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
        Given a function, poll every time period until the function passes the condition
        """
        while True:
            value = func()
            if condition(value):
                return value
            time.sleep(interval)

    def poll_canvas(self):
        while True:
            print("Looking for ungraded assignments...")
            # assignment = self.course.get_assignment(assignment_id)
            ungraded_submissions = self.poll(lambda: self.get_ungraded_assignment_submissions())
            for submission in ungraded_submissions:
                if submission.id == 3336088:
                    continue
                self.dispatch_test(submission)
        
    def download_submission(self, submission: Submission, dest: Path):
        """ Download student submission """
        for attachment in submission.attachments:
            print("Ungraded submission ID", submission.id)
            path = dest / attachment.display_name
            attachment.download(path)
        # score = randint(1, 4)
        # print(f"Automatically assigning random grade of {score} to submission")
        # submission.edit(submission={'posted_grade': score}, comment={'text_comment': f"Attempt {submission.attempt} grade: {score}"})

    def _make_dirname(self, canvas_object: CanvasObject):
        """
        Generate string in {name}-{id} format 
        """
        return Path(slugify(canvas_object.name) + "-" + str(canvas_object.id))

    def generate_test_dir(self, s: Submission):
        """ Generate file path to download submission """
        course = canvas.get_course(s.course_id)
        assignment = course.get_assignment(s.assignment_id)
        user_id = s.user_id
        try:
            user_name = canvas.get_user(s.user_id).name
        except ResourceDoesNotExist: # If using test user
            user_name = "Test User"

        user_name=slugify(user_name)
        course_dir = self._make_dirname(course)
        assignment_dir = self._make_dirname(assignment)
        test_path = course_dir / assignment_dir / f"{user_name}-{user_id}-{s.attempt}"
        test_dir = AUTOGRADE_DIR / test_path
        return test_dir

    def dispatch_test(self, submission: Submission):
        """ Build and execute testing pipeline on student submission. """ 
        test_dir = self.generate_test_dir(submission)
        if not test_dir.exists():
            test_dir.mkdir(parents=True, exist_ok=True)
        self.download_submission(submission=submission, dest=test_dir)
        # Run test from config
        runner = SLURMRunner()
        runner.deploy(submission, test_dir)
        # Get corresponding test modules based on config
        # uz = UnzipDirectory(
        #     target=test_dir / "first_assignment-f3fe1b4b-d786-4c7a-98d6-f0e9e300e38c.zip",
        #     dest=test_dir
        # )

        # vd = ValidateDirectory(
        #     max_score=2, 
        #     root=Path(test_dir) / "first_assignment", 
        #     paths=[Path(p) for p in ["test/FirstTest.java", "src/First.java", "src/FirstI.java", "src/FirstException.java", "src/RunFirst.java"]]
        # )
        # test_modules = [uz, vd]
        # run tests
        # for tm in test_modules:
        #     tm.run()

        # for tm in test_modules:
        #     print(tm.get_score())
        #     print(tm.get_feedback())
        # get corresponding test directories (maybe this should be done in SLURM)
        # deploy it in SLURM

    
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

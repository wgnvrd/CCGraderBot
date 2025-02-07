from dotenv import load_dotenv
import os

from canvasapi import Canvas
from canvasapi.submission import Submission
from canvasapi.assignment import Assignment

class CanvasHelper():
    def __init__(self):
        """
        Init method for the CanvasHelper class"""
        load_dotenv()
        # Canvas API URL
        self.API_URL = "https://canvas.coloradocollege.edu"
        # Canvas API key
        self.API_KEY = os.getenv("CANVAS_ACCESS_TOKEN")
        # header = {"Authorization" : "Bearer " + API_KEY}

        # Initialize a new Canvas object
        self.canvas = Canvas(self.API_URL, self.API_KEY)

    def get_canvas_api(self):
        """
        Gets the current canvas object
        """
        return self.canvas

    def make_canvas(self,api_key):
        """
        Creates a canvas object using a given api key
        """
        return Canvas(self.API_URL, api_key)

    def get_submission(self,course_id, assign_id, userId):
        """
        Gets a submission from this object's canvas instance
        using a given course id, assignment id, and user id
        """
        return self.canvas.get_course(course_id).get_assignment(assign_id).get_submission(userId)

    def grade_submission(self,submission, score, comment):
        """
        Grades a given submission according to the given score and comment
        """
        submission.edit(submission={'posted_grade': score}, comment={'text_comment': comment})

    def submission_is_graded(self,submission: Submission):
        """
        Returns a boolean indicating whether a submission has been graded or not
        """
        return submission.grade and submission.grade_matches_current_submission

    def submission_is_resubmission(self,submission: Submission):
        """
        Returns a boolean indicating whether a submission is a resubmission attempt or not
        """
        return submission.attempt > 1

    def get_ungraded_submissions(self,assignment: Assignment):
        """
        gets all submissions for a given assignment that are ungraded
        """
        submissions = assignment.get_submissions()
        return [s for s in submissions if not self.submission_is_graded(s)]
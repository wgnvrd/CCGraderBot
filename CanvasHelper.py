import requests
from dotenv import load_dotenv
import os
import zipfile
import io

from canvasapi import Canvas
from canvasapi.submission import Submission
from canvasapi.assignment import Assignment

load_dotenv()
# Canvas API URL
API_URL = "https://canvas.coloradocollege.edu"
# Canvas API key
API_KEY = os.getenv("CANVAS_ACCESS_TOKEN")
# header = {"Authorization" : "Bearer " + API_KEY}

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Get the current canvas object
def get_canvas_api():
    return canvas

def make_canvas(api_key):
    return Canvas(API_URL, api_key)

# temp to hopefully make the demo work
def get_submission(course_id, assign_id, userId):
    return canvas.get_course(course_id).get_assignment(assign_id).get_submission(userId)

# grade a given submission according to the given score and comment
def grade_submission(submission, score, comment):
    submission.edit(submission={'posted_grade': score}, comment={'text_comment': comment})

# returns a boolean indicating whether a submission has been graded or not
def submission_is_graded(submission: Submission):
    return submission.grade and submission.grade_matches_current_submission

# returns a boolean indicating whether a submission is a resubmission attempt or not
def submission_is_resubmission(submission: Submission):
    return submission.attempt > 1

# gets all submissions for a given assignment that are ungraded
def get_ungraded_submissions(assignment: Assignment):
    submissions = assignment.get_submissions()
    return [s for s in submissions if not submission_is_graded(s)]

def get_submission(course_id, assign_id, userId):
    return canvas.get_course(course_id).get_assignment(assign_id).get_submission(userId)

print(canvas.get_courses(enrollment_type="teacher")[0].name)
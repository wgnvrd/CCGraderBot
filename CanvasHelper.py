import requests
from dotenv import load_dotenv
import os
import zipfile
import io

from canvasapi import Canvas

load_dotenv()
# Canvas API URL
API_URL = "https://canvas.coloradocollege.edu"
# Canvas API key
API_KEY = os.getenv("CANVAS_ACCESS_TOKEN")
# header = {"Authorization" : "Bearer " + API_KEY}

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

def get_course(course_id):
    return canvas.get_course(course_id)

def get_assignment(course_id,assign_id):
    course = get_course(course_id)
    return course.get_assignment(assign_id)

def get_assignments(course_id):
    course = get_course(course_id)
    return course.get_assignments()

def get_ungraded_assignments(course_id):
    course = get_course(course_id)
    return course.get_assignments(bucket='ungraded')

def get_submission(course_id,assign_id, user_id):
    course = get_course(course_id)
    assignment = course.get_assignment(assign_id)
    return assignment.get_submission(user_id)

def get_submissions(course_id, assign_id):
    course = get_course(course_id)
    assignment = course.get_assignment(assign_id)
    return assignment.get_submissions()

def get_ungraded_submissions(assignment):
    submissions = assignment.get_submissions()
    ungraded = []
    for sub in submissions:
        if(submission_is_graded(sub)==True):
            ungraded.append(sub)
    return ungraded

def grade_submission(submission, score, comment):
    submission.edit(submission={'posted_grade': score})

# IMPORTANT: THIS RETURNS A LIST, NOT A PAGINATEDLIST
def get_ungraded_assignments(course_id):
    course = canvas.get_course(course_id)
    # assignments = course.get_assignments(bucket="ungraded")
    assignments = course.get_assignments()
    assignment_list = []
    for assignment in assignments:
        assignment_list.append(assignment)
    
    ungraded_assignments = []
    for assign in assignment_list:
        ungraded_submissions = get_ungraded_submissions(assign)
        submission_list = []
        for submission in ungraded_submissions:
            submission_list.append(submission)
        print(assign)
        print(submission_list)
        print(len(submission_list))
        if (len(submission_list) != 0):
            ungraded_assignments.append(assign)
    return ungraded_assignments
    
def submission_is_graded(submission):
    return submission.grade is None or not submission.grade_matches_current_submission

def submission_is_resubmission(submission):
    return submission.attempt > 1

# def get_ungraded_submissions(assignment):
#     submissions = assignment.get_submissions()
#     return [s for s in submissions if self.submission_is_resubmission(s)]

    # load_dotenv()

    # CANVAS_ACCESS_TOKEN = os.getenv("CANVAS_ACCESS_TOKEN")
    # header = {"Authorization" : "Bearer " + CANVAS_ACCESS_TOKEN}
    # url = "https://canvas.coloradocollege.edu/api/v1/"

    # # ID for CP222: 43491
    # # ID for Recall JAVA: 155997
    # # ID of submission: 3331124
    # # ID of user: 24366

    # def grade_assignment(course_id, assignment_id, user_id, score, my_comment):
    #     r = put_request(f"courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}", score=score, comment=my_comment)
    #     return r

    # def create_score():
    #     pass

    # def post_request(endpoint):
    #     pass

    # def put_request(endpoint, **kwargs):
    #     print("endpoint:", url + endpoint)
    #     payload = {'submission[posted_grade]': kwargs['score']}
    #     if 'comment' in kwargs:
    #         payload.update({'comment[text_comment]': kwargs['comment']})
    #     r = requests.put(url + endpoint, data=payload, headers=header)
    #     return r

    # # restructure this later because this only works for lists
    # def make_request(endpoint, params=None):
    #     r = requests.get(url + endpoint, headers = header, params=params)
    #     # print(r)
    #     data = []
    #     data += r.json()
    #     while r.links.get('next', False): 
    #         r = requests.get(r.links['next']['url'], headers = header)
    #         data += r.json()
    #     return data

    # def extract_zip(url):
    #     r = requests.get(url,headers = header)
    #     z = zipfile.ZipFile(io.BytesIO(r.content))
    #     z.extractall(os.path.join("testing"))

    # def get_courses():
    #     data = make_request(endpoint="courses")
    #     return data

    # # def get_line_items(course_id):
    # #     data = make_request(endpoint=f"/lti/courses/{course_id}/line_items")
    # #     return data
    # def get_external_tools(course_id):
    #     data = make_request(endpoint=f"courses/{course_id}/external_tools")
    #     return data

    # def get_assignments(course_id, params=None):
    #     # params = {"bucket": "upcoming"}
    #     # params = None
    #     data = make_request(endpoint=f"courses/{course_id}/assignments", params=params)
    #     return data

    # def get_submissions(course_id, assign_id):
    #     data = make_request(endpoint=f"courses/{course_id}/assignments/{assign_id}/submissions")
    #     return data

    # def get_submission(course_id, assign_id, user_id):
    #     endpoint = f"courses/{course_id}/assignments/{assign_id}/submissions/{user_id}"
    #     r = requests.get(url + endpoint, headers = header)
    #     # print(r)
    #     return r.json()


import requests
from dotenv import load_dotenv
import os
import zipfile
import io

load_dotenv()

CANVAS_ACCESS_TOKEN = os.getenv("CANVAS_ACCESS_TOKEN")
header = {"Authorization" : "Bearer " + CANVAS_ACCESS_TOKEN}
url = "https://canvas.coloradocollege.edu/api/v1/"

# ID for CP222: 43491
# ID for Recall JAVA: 155997
# ID of submission: 3331124
# ID of user: 24366

def grade_assignment(course_id, assignment_id, user_id, score, comment):
    r = put_request(f"courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}", score=score, comment='good job')
    return r

def create_score():
    pass

def post_request(endpoint):
    pass

def put_request(endpoint, **kwargs):
    print("endpoint:", url + endpoint)
    payload = {'submission[posted_grade]': kwargs['score']}
    if 'comment' in kwargs:
        payload.update({'comment[text_comment]': kwargs['comment']})
    r = requests.put(url + endpoint, data=payload, headers=header)
    return r

# restructure this later because this only works for lists
def make_request(endpoint, params=None):
    r = requests.get(url + endpoint, headers = header, params=params)
    print(r)
    data = []
    data += r.json()
    while r.links.get('next', False): 
        r = requests.get(r.links['next']['url'], headers = header)
        data += r.json()
    return data

def extract_zip(url):
    r = requests.get(url,headers = header)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(".")

def get_courses():
    data = make_request(endpoint="courses")
    return data

# def get_line_items(course_id):
#     data = make_request(endpoint=f"/lti/courses/{course_id}/line_items")
#     return data
def get_external_tools(course_id):
    data = make_request(endpoint=f"courses/{course_id}/external_tools")
    return data

def get_assignments(course_id, params=None):
    # params = {"bucket": "upcoming"}
    # params = None
    data = make_request(endpoint=f"courses/{course_id}/assignments", params=params)
    return data

def get_submissions(course_id, assign_id):
    data = make_request(endpoint=f"courses/{course_id}/assignments/{assign_id}/submissions")
    return data

def get_submission(course_id, assign_id, user_id):
    endpoint = f"courses/{course_id}/assignments/{assign_id}/submissions/{user_id}"
    r = requests.get(url + endpoint, headers = header)
    print(r)
    return r.json()


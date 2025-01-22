import requests
import os
import zipfile
import io
import json
from dotenv import load_dotenv

load_dotenv()
CANVAS_ACCESS_TOKEN = os.getenv("CANVAS_ACCESS_TOKEN")
header = {"Authorization" : "Bearer " + CANVAS_ACCESS_TOKEN}
url = "https://canvas.coloradocollege.edu/api/v1/"

# ID for CP222: 43491
# ID for Recall JAVA: 155997
# ID of submission: 3331124
# ID of user: 24366

def main():
    #Doin like a simple navigation of classes with really simple input stuff -- definitely needs to be replaced at somepoint
    inputs = [0,1]
    print("Welcome! What would you like to do?")
    val = int(input("0. Exit \n1. See my Courses\n"))

    while val not in inputs:
        print('Bad input; Please try again')
        val = int(input("0. Exit \n1. See my Courses\n"))

    if int(val) == 0:
        quit()

    # Get all of the courses -- skip the weird empty ones that break every thing
    courseList = []
    data = get_courses()
    # Every Course in an easy to read way
    for course in data:
        if 'name' in course and 'id' in course:
            courseList.append(course)
    print("Here are all of your courses!")
    print("Index |  ID  |  Name ")
    count = 0
    for course in courseList:
        print('{0} | {1} | {2}'.format(count, course['id'], course['name']))
        count +=1


""" 
    data = get_assignments(43491)
    for assignment in data:
       if 'name' in assignment and 'id' in assignment:
            print(assignment['id'], assignment['name'])
    
    # data = get_submissions(43491, 155997)

    # for sub in data:
    #     print(sub)
    #     if 'attachments' in sub:
    #         if sub['attachments'][0]['content-type'] == 'application/x-zip-compressed':
    #             link = sub['attachments'][0]['url']
    #             extract_zip(link) 
    # data = get_external_tools(43491)
    # print(data)
    r = grade_assignment(course_id=43491, assignment_id=155997, user_id=24366, score=2)
    data = r.json()
    print(data)
    
def grade_assignment(course_id, assignment_id, user_id, score):
    r = put_request(f"courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}", score=score)
    return r

def create_score():
    pass

def post_request(endpoint):
    pass

def put_request(endpoint, **kwargs):
    print("endpoint:", url + endpoint)
    r = requests.put(url + endpoint, data=json.dumps({"submission": {"posted_grade": "2"}}), headers=header)
    return r

    for sub in data:
        if 'attachments' in sub:
            link = sub['attachments'][0]['url']
            r = requests.get(link,headers = header)
            print(r.json()) """
            
        
 
def make_request(endpoint):
    r = requests.get(url + endpoint, headers = header)
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

def get_assignments(course_id):
    data = make_request(endpoint=f"courses/{course_id}/assignments")
    return data

def get_submissions(course_id, assign_id):
    data = make_request(endpoint=f"courses/{course_id}/assignments/{assign_id}/submissions")
    return data
if __name__ == "__main__":
    main()
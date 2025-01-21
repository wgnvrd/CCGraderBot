import requests
import os
from dotenv import load_dotenv

load_dotenv()
CANVAS_ACCESS_TOKEN = os.getenv("CANVAS_ACCESS_TOKEN")
header = {"Authorization" : "Bearer " + CANVAS_ACCESS_TOKEN}
url = "https://canvas.coloradocollege.edu/api/v1/"

# ID for CP222: 43491
# ID for Recall JAVA: 155997
def main():
    # data = get_courses()
    # print(data[0].keys())
    # for course in data:
    #     if 'name' in course and 'id' in course:
    #         print(course['id'], course['name'])
    #data = get_assignments(43491)
    #for assignment in data:
     #   if 'name' in assignment and 'id' in assignment:
      #      print(assignment['id'], assignment['name'])
    
    data = get_submissions(43491, 155997)

    for sub in data:
        if 'attachments' in sub:
            link = sub['attachments'][0]['url']
            r = requests.get(link,headers = header)
            
        
 
def make_request(endpoint):
    r = requests.get(url + endpoint, headers = header)
    data = []
    data += r.json()
    while r.links.get('next', False): 
        r = requests.get(r.links['next']['url'], headers = header)
        data += r.json()
    return data

def get_courses():
    data = make_request(endpoint="courses")
    return data

def get_assignments(course_id):
    data = make_request(endpoint=f"courses/{course_id}/assignments")
    return data

def get_submissions(course_id, assign_id):
    data = make_request(endpoint=f"courses/{course_id}/assignments/{assign_id}/submissions")
    return data
if __name__ == "__main__":
    main()
import requests

from CanvasAPI import header, get_submission, get_courses, grade_assignment

def main():
    #Doin like a simple navigation of classes with really simple input stuff -- definitely needs to be replaced at somepoint
    get_submission(course_id=43491, assign_id=155997, user_id=24366)
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
        count+=1

    for sub in data:
        if 'attachments' in sub:
            link = sub['attachments'][0]['url']
            r = requests.get(link,headers = header)
            print(r.json())

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
    """

    print("\n\n\nspace\n\n\n")
    r = grade_assignment(course_id=43491, assignment_id=155997, user_id=24366, score=3, comment='good job')
    print("\n\n\nspace\n\n\n")

    print(r)

    print("\n\n\nspace\n\n\n")

    data = r.json()
    print(data)

if __name__ == "__main__":
    main()
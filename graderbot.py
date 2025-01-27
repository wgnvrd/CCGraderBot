from CanvasAPI import grade_assignment, get_submission, extract_zip, get_submissions

import argparse
import random

# ID for CP222: 43491
# ID for Recall JAVA: 155997
# ID of submission: 3331124
# ID of user: 24366

# Takes in a list of words and turns them back
# into a string
def make_comment(my_list):
    comment = my_list[0]
    for i in range(1,len(my_list)):
        if my_list[i] == ".":
            comment = comment + my_list[i]
        else:
            comment = comment + " " + my_list[i]
    return comment

# placeholder autograder until there's actually something to hook into
# Randomly generates a float between 0-4 and attaches a comment based on
# where in the range the score lands, then it returns them as a dictionary
def placeholder_autograder():
    score = random.random()*4
    if score > 3:
        comment = "good job"
    elif score > 2:
        comment = "barely passing"
    elif score > 1:
        comment = "do better"
    elif score >= 0:
        comment = "come to office hours"
    graded = {
        "score": score,
        "comment": comment
    }
    return graded

parser = argparse.ArgumentParser()
parser.add_argument("method", type=str, help="Determines the method to be run")
parser.add_argument("--course_id", type=int, help="Course ID of the class you're trying to access")
parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
parser.add_argument("--user_id", type=int,help="User ID of the student whose work you're trying to access")
parser.add_argument("--score",type=int,help="The raw score you're trying to give to the submission")
parser.add_argument("--comment",nargs="+",type=str,help="Comment you're giving to the submission")

args = parser.parse_args()

# This if case accesses the submission of a user id for an assignment id and currently just grades
# according to the given score and comment. This will develop more as we work out
# the autograder -Kazu 1/26/25
# python graderbot.py grade --course_id 43491 --assign_id 155997 --user_id 24366 --score 3 --comment good job
if(args.method == str("grade")):
    args.comment = make_comment(args.comment)
    print("Method: grade")
    print("Course ID: " + str(args.course_id))
    print("Assignment ID: " + str(args.assign_id))
    print("User ID: " + str(args.user_id))
    print("Score: " + str(args.score))
    print("Comment: " + args.comment)

    r = grade_assignment(args.course_id, args.assign_id, args.user_id, args.score, args.comment)
    data = r.json()
    print(data)

# This if case can pull and extract the zip submission of a given user id for a given assignment id
# As it currently stands, this if case is probably more likely going to be used for any future loops
# than download_zips -Kazu 1/26/25
# python graderbot.py download_zip --course_id 43491 --assign_id 155997 --user_id 24366
elif(args.method == str("download_zip")):
    print("Method: download zip")
    print("Course ID: " + str(args.course_id))
    print("Assignment ID: " + str(args.assign_id))
    print("User ID: " + str(args.user_id))
    url = get_submission(str(args.course_id),str(args.assign_id),str(args.user_id))["attachments"][0]["url"]
    print(url)
    extract_zip(url)
    print("User id " + str(args.user_id) + "'s submission for assign_id " + str(args.assign_id) + " extracted")

# This method can hypothetically pull and extracted all the zip submissions for a given assignment id. 
# Retrofitting later would probably make it use the autograder that's still in development -Kazu 1/26/25
# python graderbot.py download_zips --course_id 43491 --assign_id 155997
elif(args.method == str("download_zips")):
    print("Method: download zips")
    print("Course ID: " + str(args.course_id))
    print("Assignment ID: " + str(args.assign_id))
    url = get_submissions(str(args.course_id),str(args.assign_id))
    for sub in range(0,len(url)):
        userid = url[sub]["user_id"]
        link = get_submission(str(args.course_id),str(args.assign_id),str(userid))["attachments"][0]["url"]
        extract_zip(link)
    print(str(len(url)) + " zip(s) extracted")

# Temp pipeline for autograding from the command line that I set up. 
# It pulls and extracts all the zips submitted for an assignment,
# then it uses a temp method I made to assign each submission a random
# score and associated comment, then it grades each submission using
# those scores and comments.
# Once we have the autograder actually set up, hopefully this can 
# actually have it plug into that. -Kazu 1/26/25
# python graderbot.py autograde --course_id 43491 --assign_id 155997
elif(args.method == str("autograde")):
    print("Method: download zips")
    print("Course ID: " + str(args.course_id))
    print("Assignment ID: " + str(args.assign_id))
    url = get_submissions(str(args.course_id),str(args.assign_id))
    for sub in range(0,len(url)):
        userid = url[sub]["user_id"]
        link = get_submission(str(args.course_id),str(args.assign_id),str(userid))["attachments"][0]["url"]
        extract_zip(link)
        print("autograder method placeholder slot?")
        grade = placeholder_autograder()
        print(str(grade["score"]) + ", " + grade["comment"])
        r = grade_assignment(args.course_id, args.assign_id, userid, grade["score"], grade["comment"])
        data = r.json()
        print(data)
    print(str(len(url)) + " zip(s) extracted")

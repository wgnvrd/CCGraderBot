# from CanvasAPI import grade_assignment, get_submission, extract_zip, get_submissions, get_assignments, 
from CanvasHelper import get_course, get_assignment, get_assignments, get_ungraded_assignments, get_submission, grade_submission

import argparse
import sys
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

#--------------------------------------------------------------



class GraderBot(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Graderbot attempting to use git format',
            usage='''gb <command> [<args>]''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[2:3])
        print(args)
        if not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        print("Command exists")
        getattr(self, args.command)()

# get_course_test, get_assignment_test, get_assignments_test, 
# get_ungraded_assignments_test, get_submission_test, 
# grade_submission_test
    def get_course(self):
        parser = argparse.ArgumentParser(description="Get a single course")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        course = parser.parse_args(sys.argv[3:])
        print(course.course_id)
        print(get_course(int(course.course_id)))
        print("Running gb get_course")
    # def commit(self):
    #     parser = argparse.ArgumentParser(
    #         description='Record changes to the repository')
    #     # prefixing the argument with -- means it's optional
    #     parser.add_argument('--amend', action='store_true')
    #     # now that we're inside a subcommand, ignore the first
    #     # TWO argvs, ie the command (git) and the subcommand (commit)
    #     args = parser.parse_args(sys.argv[2:])
    #     print 'Running git commit, amend=%s' % args.amend

    # def fetch(self):
    #     parser = argparse.ArgumentParser(
    #         description='Download objects and refs from another repository')
    #     # NOT prefixing the argument with -- means it's not optional
    #     parser.add_argument('repository')
    #     args = parser.parse_args(sys.argv[2:])
    #     print 'Running git fetch, repository=%s' % args.repository
if __name__ == "__main__":
    GraderBot()


#-----------------------------------------------------------------------
# parser = argparse.ArgumentParser()
# parser.add_argument("method", type=str, help="Determines the method to be run")
# parser.add_argument("--course_id", type=int, help="Course ID of the class you're trying to access")
# parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
# parser.add_argument("--user_id", type=int,help="User ID of the student whose work you're trying to access")
# parser.add_argument("--score",type=int,help="The raw score you're trying to give to the submission")
# parser.add_argument("--comment",nargs="+",type=str,help="Comment you're giving to the submission")

# args = parser.parse_args()

# # python graderbot.py test --course_id 43491 --assign_id 155997 --user_id 24366
# if(args.method == str("test")):
#     course = get_course(int(args.course_id))
#     print("Course: " + str(course))
#     singleassign = get_assignment(course, int(args.assign_id))
#     print("\nAssignment: " + str(singleassign))
#     allassign = get_assignments(course)
#     print("\nAll Assignments:")
#     for assignment in allassign:
#         print(assignment)
#     ungraded = get_ungraded_assignments(course)
#     print("\nUngraded Assignments")
#     for assignment in ungraded:
#         print(assignment)
#     sub = get_submission(singleassign, int(args.user_id))
#     print("Submission:")
#     print(sub)
#     grade_submission(sub,2,"good job")
#     print("Graded?")




# -------------------------------------------------------------------------------------------------------------------
    # # This if case accesses the submission of a user id for an assignment id and currently just grades
    # # according to the given score and comment. This will develop more as we work out
    # # the autograder -Kazu 1/26/25
    # # python graderbot.py grade --course_id 43491 --assign_id 155997 --user_id 24366 --score 3 --comment good job
    # elif(args.method == str("grade")):
    #     args.comment = make_comment(args.comment)
    #     print("Method: grade")
    #     print("Course ID: " + str(args.course_id))
    #     print("Assignment ID: " + str(args.assign_id))
    #     print("User ID: " + str(args.user_id))
    #     print("Score: " + str(args.score))
    #     print("Comment: " + args.comment)

    #     r = grade_assignment(args.course_id, args.assign_id, args.user_id, args.score, args.comment)
    #     data = r.json()
    #     print(data)

    # # This if case can pull and extract the zip submission of a given user id for a given assignment id
    # # As it currently stands, this if case is probably more likely going to be used for any future loops
    # # than download_zips -Kazu 1/26/25
    # # python graderbot.py download_zip --course_id 43491 --assign_id 155997 --user_id 24366
    # elif(args.method == str("download_zip")):
    #     print("Method: download zip")
    #     print("Course ID: " + str(args.course_id))
    #     print("Assignment ID: " + str(args.assign_id))
    #     print("User ID: " + str(args.user_id))
    #     url = get_submission(str(args.course_id),str(args.assign_id),str(args.user_id))["attachments"][0]["url"]
    #     print(url)
    #     extract_zip(url)
    #     print("User id " + str(args.user_id) + "'s submission for assign_id " + str(args.assign_id) + " extracted")

    # # This method can hypothetically pull and extracted all the zip submissions for a given assignment id. 
    # # Retrofitting later would probably make it use the autograder that's still in development -Kazu 1/26/25
    # # python graderbot.py download_zips --course_id 43491 --assign_id 155997
    # elif(args.method == str("download_zips")):
    #     print("Method: download zips")
    #     print("Course ID: " + str(args.course_id))
    #     print("Assignment ID: " + str(args.assign_id))
    #     url = get_submissions(str(args.course_id),str(args.assign_id))
    #     for sub in range(0,len(url)):
    #         userid = url[sub]["user_id"]
    #         link = get_submission(str(args.course_id),str(args.assign_id),str(userid))["attachments"][0]["url"]
    #         extract_zip(link)
    #     print(str(len(url)) + " zip(s) extracted")

    # # Temp pipeline for autograding from the command line that I set up. 
    # # It pulls and extracts all the zips submitted for an assignment,
    # # then it uses a temp method I made to assign each submission a random
    # # score and associated comment, then it grades each submission using
    # # those scores and comments.
    # # Once we have the autograder actually set up, hopefully this can 
    # # actually have it plug into that. -Kazu 1/26/25
    # # python graderbot.py autograde --course_id 43491 --assign_id 155997
    # elif(args.method == str("autograde_assign")):
    #     print("Method: autograde assignment")
    #     print("Course ID: " + str(args.course_id))
    #     print("Assignment ID: " + str(args.assign_id))
    #     url = get_submissions(str(args.course_id),str(args.assign_id))
    #     for sub in range(0,len(url)):
    #         userid = url[sub]["user_id"]
    #         link = get_submission(str(args.course_id),str(args.assign_id),str(userid))["attachments"][0]["url"]
    #         extract_zip(link)
    #         print("autograder method placeholder slot?")
    #         grade = placeholder_autograder()
    #         print(str(grade["score"]) + ", " + grade["comment"])
    #         r = grade_assignment(args.course_id, args.assign_id, userid, grade["score"], grade["comment"])
    #         data = r.json()
    #         print(data)
    #     print(str(len(url)) + " zip(s) extracted")

    # # Hypothetical if case that can grade all the assignments for a course
    # # python graderbot.py autograde_course --course_id 43491
    # elif(args.method == str("autograde_course")):
    #     print("Method: autograde course")
    #     print("Course ID: " + str(args.course_id))
    #     a = get_assignments(str(args.course_id))
    #     print("len(a): " + str(len(a)))
    #     graded = 0
    #     nosubs = 0
    #     for assign in range(0,len(a)):
    #         print("Assignment id: "+ str(a[assign]["id"]))
    #         print("Assignment name: " + str(a[assign]["name"]))
    #         assignid = a[assign]["id"]
    #         if(a[assign]["has_submitted_submissions"]==True):
    #             s = get_submissions(str(args.course_id),str(assignid))
    #             print("Number of submissions: " + str(len(s)))
    #             for sub in range(0,len(s)):
    #                 userid = s[sub]["user_id"]
    #                 link = get_submission(str(args.course_id),str(assignid),str(userid))["attachments"][0]["url"]
    #                 extract_zip(link)
    #                 print("autograder method placeholder slot?")
    #                 grade = placeholder_autograder()
    #                 print("Score: " + str(grade["score"]) + ", Comment: " + grade["comment"])
    #                 r = grade_assignment(args.course_id, args.assign_id, userid, grade["score"], grade["comment"])
    #                 data = r.json()
    #             print(str(len(s)) + " zip(s) extracted")
    #             graded+=1
    #         else:
    #             print("No submissions for " + str(a[assign]["name"]))
    #             nosubs+=1
    #     print(str(graded)+ " assignment(s) graded, " + str(nosubs) + " assignment(s) had no submissions")

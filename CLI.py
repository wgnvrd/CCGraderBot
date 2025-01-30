from CanvasHelper import get_canvas_api, get_ungraded_submissions, grade_submission, submission_is_graded, submission_is_resubmission

import argparse
import sys

# ID for CP222: 43491
# ID for Recall JAVA: 155997
# ID of submission: 3331124
# ID of user: 24388

# Takes in a list of words and turns them back into a string
def make_comment(my_list):
    comment = my_list[0]
    for i in range(1,len(my_list)):
        if my_list[i] == ".":
            comment = comment + my_list[i]
        else:
            comment = comment + " " + my_list[i]
    return comment

# References https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
class CLI(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Graderbot attempting to use git format',
            usage='''<command> [<args>]''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        self.canvas = get_canvas_api()
        if not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

# Gets a course using an input course id
    def gc(self, course_id):
        return self.canvas.get_course(int(course_id))
    
# Gets an assignment using an input course id and assignment id 
    def ga(self, course_id, assign_id):
        return self.gc(course_id).get_assignment(int(assign_id))
    
# Gets a submission using an input course id, assignment id, and user id
    def gs(self, course_id, assign_id, user_id):
        return self.gc(course_id).get_assignment(int(assign_id)).get_submission(int(user_id))

# python CLI.py get_course --course_id 43491
    def get_course(self):
        parser = argparse.ArgumentParser(description="Get a single course")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_course")
        course = self.gc(args.course_id)
        print(course)

# python CLI.py get_assignment --course_id 43491 --assign_id 155997
    def get_assignment(self):
        parser = argparse.ArgumentParser(description="Get a single assignment")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_assignment")
        assignment = self.ga(int(args.course_id),int(args.assign_id))
        print(assignment)

# python CLI.py get_assignments --course_id 43491
    def get_assignments(self):
        parser = argparse.ArgumentParser(description="Gets all assignments for a course")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_assignments")
        assignments = self.gc(args.course_id).get_assignments()
        for assignment in assignments:
            print(assignment)

# python CLI.py get_submission --course_id 43491 --assign_id 155997 --user_id 24388
    def get_submission(self):
        parser = argparse.ArgumentParser(description="Gets the most recent submission by a user id for an assignment")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        parser.add_argument("--user_id", type=int,help="User ID of the student whose work you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_submission")
        submission = self.gs(args.course_id,args.assign_id,args.user_id)
        print(submission)

# python CLI.py get_submissions --course_id 43491 --assign_id 155997
    def get_submissions(self):
        parser = argparse.ArgumentParser(description="Gets all submissions for an assignment")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_submissions")
        submissions = self.ga(args.course_id,args.assign_id).get_submissions()
        for submission in submissions:
            print(submission)

# python CLI.py get_ungraded_submissions --course_id 43491 --assign_id 155997
    def get_ungraded_submissions(self):
        parser = argparse.ArgumentParser(description="Gets all ungraded submissions for an assignment")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_ungraded_submissions")
        assignment = self.ga(args.course_id,args.assign_id)
        submissions = get_ungraded_submissions(assignment)
        for submission in submissions:
            print(str(submission))

# python CLI.py submission_is_graded --course_id 43491 --assign_id 155997 --user_id 24388
    def submission_is_graded(self):
        parser = argparse.ArgumentParser(description="Checks if a submission is graded")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        parser.add_argument("--user_id", type=int,help="User ID of the student whose work you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running submission_is_graded")
        submission = self.gs(args.course_id,args.assign_id,args.user_id)
        print("Is submission from user id " + str(args.user_id) + " for assignment id " + str(args.assign_id)
              + " for course id " + str(args.course_id) + " graded?: " + str(submission_is_graded(submission)))

# python CLI.py submission_is_resubmission --course_id 43491 --assign_id 155997 --user_id 24388
    def submission_is_resubmission(self):
        parser = argparse.ArgumentParser(description="Checks if a submission is a resubmission")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        parser.add_argument("--user_id", type=int,help="User ID of the student whose work you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running submission_is_resubmission")
        submission = self.gs(args.course_id,args.assign_id,args.user_id)
        print("Is submission from user id " + str(args.user_id) + " for assignment id " + str(args.assign_id)
              + " for course id " + str(args.course_id) + " a resubmission?: " + str(submission_is_resubmission(submission)))

# python CLI.py grade_submission --course_id 43491 --assign_id 155997 --user_id 24388 --score 3 --comment "good job?"
    def grade_submission(self):
        parser = argparse.ArgumentParser(description="Grade the most recent submission by a user id for an assignment. If you want punctuation, I think you need to add quotation marks")
        parser.add_argument("--course_id", type=int, help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        parser.add_argument("--user_id", type=int,help="User ID of the student whose work you're trying to access")
        parser.add_argument("--score",type=int,help="The raw score you're trying to give to the submission")
        parser.add_argument("--comment",nargs="+",type=str,help="Comment you're giving to the submission")
        args = parser.parse_args(sys.argv[2:])
        print("Running grade_submission")
        submission = self.gs(args.course_id,args.assign_id,args.user_id)
        grade_submission(submission,args.score,make_comment(args.comment))

if __name__ == "__main__":
    CLI()
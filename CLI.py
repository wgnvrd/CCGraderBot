from CanvasHelper import get_canvas_api, get_ungraded_submissions, grade_submission, submission_is_graded, submission_is_resubmission, make_canvas

import argparse
import sys
import ConfigHandler

#delete later
import os

# ID for CP222: 43491
# ID for Recall JAVA: 155997
# ID of submission: 3331124
# ID of user: 24388

def make_comment(my_list):
    """
    This method takes in a list of words and turns them back into a string 
    because the comment section reads inputs to the command line and
    returns a list of words
    """
    comment = my_list[0]
    for i in range(1,len(my_list)):
        if my_list[i] == ".":
            comment = comment + my_list[i]
        else:
            comment = comment + " " + my_list[i]
    return comment

class CLI(object):
    """
    This is the class that's responsible for the command line
    It has a variety of methods that let you get information
    about anything within a course
    References https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
    """
    def __init__(self):
        """
        This is the constructor for the command line interface
        It creates the initial command line interface prompt
        that determines what you want to do
        """
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

    def gc(self, course_id):
        """
        This is a shortcut method that gets a course using an input course id
        """
        return self.canvas.get_course(int(course_id))

    def gag(self,course_id):
        """
        This is a shortcut method that gets assignment groups 
        for a course using an input course id
        """
        return self.canvas.get_course(int(course_id)).get_assignment_groups()
     
    def ga(self, course_id, assign_id):
        """
        This is a shortcut method that gets an assignment 
        using an input course id and assignment id
        """
        return self.gc(course_id).get_assignment(int(assign_id))
    
    def gs(self, course_id, assign_id, user_id):
        """
        This is a shortcut method that gets a submission 
        using an input course id, assignment id, and user id
        """
        return self.gc(course_id).get_assignment(int(assign_id)).get_submission(int(user_id))

    def get_course(self):
        """
        This is the method the CLI diverts to to get a course using a given course id
        example command: python CLI.py get_course --course_id 43491
        """
        parser = argparse.ArgumentParser(description="Get a single course")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_course")
        course = self.gc(args.course_id)
        print(course)


    def get_courses(self):
        parser = argparse.ArgumentParser(description="Get all courses for the user")
        parser.add_argument("--active", help = "Status of classes to return")
        args = parser.parse_args(sys.argv[2:])
        if args.active:
            courses = self.canvas.get_courses(enrollment_state = 'active',enrollment_type = "teacher")
        else:
            courses = self.canvas.get_courses(enrollment_type = "teacher")
        for c in courses:
            
            print(c)


    def get_assignment_groups(self):
        """
        This is the method the CLI diverts to to get the groups of assignments 
        for a course using a given course id
        example command: python CLI.py get_course_groups --course_id 43491
        """
        parser = argparse.ArgumentParser(description="Get a single course's groups")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_assignment_groups")
        assignment_groups = self.gag(args.course_id)
        for group in assignment_groups:
            print(group)

    def get_assignment(self):
        """
        This is the method the CLI diverts to to get an assignment
        using a given course id and assignment id
        example command: python CLI.py get_assignment --course_id 43491 --assign_id 155997
        """
        parser = argparse.ArgumentParser(description="Get a single assignment")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_assignment")
        assignment = self.ga(int(args.course_id),int(args.assign_id))
        print(assignment)

    def get_assignments(self):
        """
        This is the method the CLI diverts to to get the assignments for a course
        using a given course id
        example command: python CLI.py get_assignments --course_id 43491
        """
        parser = argparse.ArgumentParser(description="Gets all assignments for a course")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_assignments")
        assignments = self.gc(args.course_id).get_assignments()
        for assignment in assignments:
            print(assignment)

    def get_submission(self):
        """
        This is the method the CLI diverts to to get a submission for an assignment
        of a course using a given course id, assignment id, and user id
        example command: python CLI.py get_submission --course_id 43491 --assign_id 155997 --user_id 24388
        """
        parser = argparse.ArgumentParser(description="Gets the most recent submission by a user id for an assignment")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        parser.add_argument("--user_id", type=int,help="User ID of the student whose work you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_submission")
        submission = self.gs(args.course_id,args.assign_id,args.user_id)
        print(submission)

    def get_submissions(self):
        """
        This is the method the CLI diverts to to get all submissions for an assignment
        of a course using a given course id and assignment id
        example command: python CLI.py get_submissions --course_id 43491 --assign_id 155997
        """
        parser = argparse.ArgumentParser(description="Gets all submissions for an assignment")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_submissions")
        submissions = self.ga(args.course_id,args.assign_id).get_submissions()
        for submission in submissions:
            print(submission)

    def get_ungraded_submissions(self):
        """
        This is the method the CLI diverts to to get all ungraded submissions for an assignment
        of a course using a given course id and assignment id
        example command: python CLI.py get_ungraded_submissions --course_id 43491 --assign_id 155997
        """
        parser = argparse.ArgumentParser(description="Gets all ungraded submissions for an assignment")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running get_ungraded_submissions")
        assignment = self.ga(args.course_id,args.assign_id)
        submissions = get_ungraded_submissions(assignment)
        for submission in submissions:
            print(str(submission))

    def submission_is_graded(self):
        """
        This is the method the CLI diverts to to check whether a user's submission
        is graded using the CanvasHelper's submission_is_graded method and accessing
        the submission using a given course id, assignment id, and user id
        example command: python CLI.py submission_is_graded --course_id 43491 --assign_id 155997 --user_id 24388
        """
        parser = argparse.ArgumentParser(description="Checks if a submission is graded")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        parser.add_argument("--user_id", type=int,help="User ID of the student whose work you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running submission_is_graded")
        submission = self.gs(args.course_id,args.assign_id,args.user_id)
        print("Is submission from user id " + str(args.user_id) + " for assignment id " + str(args.assign_id)
              + " for course id " + str(args.course_id) + " graded?: " + str(submission_is_graded(submission)))

    def submission_is_resubmission(self):
        """
        This is the method the CLI diverts to to check whether a user's submission
        is graded using the CanvasHelper's submission_is_resubmission method and accessing
        the submission using a given course id, assignment id, and user id
        example command: python CLI.py submission_is_resubmission --course_id 43491 --assign_id 155997 --user_id 24388
        """
        parser = argparse.ArgumentParser(description="Checks if a submission is a resubmission")
        parser.add_argument("--course_id", help="Course ID of the class you're trying to access")
        parser.add_argument("--assign_id", type=int, help="Assignment ID of the assignment you're trying to access")
        parser.add_argument("--user_id", type=int,help="User ID of the student whose work you're trying to access")
        args = parser.parse_args(sys.argv[2:])
        print("Running submission_is_resubmission")
        submission = self.gs(args.course_id,args.assign_id,args.user_id)
        print("Is submission from user id " + str(args.user_id) + " for assignment id " + str(args.assign_id)
              + " for course id " + str(args.course_id) + " a resubmission?: " + str(submission_is_resubmission(submission)))

    def grade_submission(self):
        """
        This is the method the CLI diverts to to grade a user's submission
        using a given score and comment, and accesses the submission using a given
        course id, assignment id, and user id
        example command: python CLI.py grade_submission --course_id 43491 --assign_id 155997 --user_id 24388 --score 3 --comment "good job?"
        """
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

    def verify_api_key(self):
        """
        This is the method the CLI diverts to to verify that an API keygenerate the course configuration file
        using ConfigHandler's generate_course_config method
        for a course accessed using a given course id
        example command: python CLI.py generate_course_config --course_id 43491
        """
        parser = argparse.ArgumentParser(description="Verify that the given key can be used for canvas calls")
        parser.add_argument("--api_key", type=int, help="API key that you're using for grading")
        args = parser.parse_args(sys.argv[2:])
        try:
            test = make_canvas(args.api_key)#os.getenv("CANVAS_ACCESS_TOKEN"))
            print(type(test))
            print("Given Canvas API key verified")
        except:
            print("Given Canvas API key is not valid")
            return -1

    def generate_course_config(self):
        """
        This is the method the CLI diverts to to generate the course configuration file
        using ConfigHandler's generate_course_config method
        for a course accessed using a given course id
        example command: python CLI.py generate_course_config --course_id 43491
        """
        parser = argparse.ArgumentParser(description="Grade the most recent submission by a user id for an assignment. If you want punctuation, I think you need to add quotation marks")
        parser.add_argument("--course_id", type=int, help="Course ID of the class you're trying to access")
        args = parser.parse_args(sys.agv[2:])
        confighandler = ConfigHandler()
        confighandler.generate_course_config(args.course_id)
        print("Course config file generated")

if __name__ == "__main__":
    """
    This is just a placeholder main method for testing
    """
    CLI()

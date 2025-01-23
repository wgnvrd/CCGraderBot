from main import grade_assignment, get_submission, extract_zip
import argparse

# ID for CP222: 43491
# ID for Recall JAVA: 155997
# ID of submission: 3331124
# ID of user: 24366

def make_comment(my_list):
    comment = my_list[0]
    for i in range(1,len(my_list)):
        comment = comment + " " + my_list[i]
    return comment

parser = argparse.ArgumentParser()
parser.add_argument("method", type=str, help="Determines the method to be run")
parser.add_argument("--course_id", type=int, required=True, help="Course ID of the class you're trying to access")
parser.add_argument("--assignment_id", type=int, required=True, help="Assignment ID of the assignment you're trying to access")
parser.add_argument("--user_id", type=int, required=True,help="User ID of the student whose work you're trying to access")
parser.add_argument("--score",type=int,help="The raw score you're trying to give to the submission")
parser.add_argument("--comment",nargs="+",type=str,help="Comment you're giving to the submission")

args = parser.parse_args()

# python graderbot.py grade --course_id 43491 --assignment_id 155997 --user_id 24366 --score 3 --comment good job
if(args.method == str("grade")):
    args.comment = make_comment(args.comment)
    print("Method: grade")
    print("Course ID: " + str(args.course_id))
    print("Assignment ID: " + str(args.assignment_id))
    print("User ID: " + str(args.user_id))
    print("Score: " + str(args.score))
    print("Comment: " + args.comment)

    r = grade_assignment(args.course_id, args.assignment_id, args.user_id, args.score, args.comment)
    data = r.json()
    print(data)

# python graderbot.py download_zip --course_id 43491 --assignment_id 155997 --user_id 24366
elif(args.method == str("download_zip")):
    print("Method: download zip")
    print("Course ID: " + str(args.course_id))
    print("Assignment ID: " + str(args.assignment_id))
    print("User ID: " + str(args.user_id))
    url = get_submission(str(args.course_id),str(args.assignment_id),str(args.user_id))["attachments"][0]["url"]
    print(url)
    extract_zip(url)
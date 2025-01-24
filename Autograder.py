import argparse
import configparser
from CanvasAPI import grade_assignment

class Autograder():
    def __init__(self, course_id):
        self.course_id = course_id
    
    def poll_canvas():
        pass 

#Example of Grading from a file
""" 
userId is the id of the submission to be graded
config is the config file for the specific assignment -- i think this would
be in some sort of database/dictionary thing attached to the assignment id
"""
#
def grade(userId, configFile):

    config = configparser.ConfigParser()
    config.read(configFile)

    values = config['DEFAULT']

    #Right here is where we would run whatever testing file is in the config 
    #I'm just gonna hard code the score/comment that would return for this example

    """
    INSERT CODE FOR TESTING HERE
    """
    grade_assignment(values["CourseId"], values["AssignId"],userId, 2.5, comment="This was graded from a config file")



    
from typing import List, ClassVar
from pathlib import Path
import argparse
import sys

from CompileModule import CompileModule
from JUnitModule import JUnitModule
from UnzipDirectory import UnzipDirectory
from ValidateDirectory import ValidateDirectory
from e2eModule import e2eModule
from javaDocModule import javaDocModule
from test_module import TestModule
from test_input_wrapper import TestInputWrapper
from CanvasHelper import get_canvas_api
from ConfigHandler import get_config_handler

canvas = get_canvas_api()

parser = argparse.ArgumentParser(
    prog="Test Runner",
    description="Build and run test pipelines based on config",
)
parser.add_argument('test_dir')
parser.add_argument('course_id')
parser.add_argument('assignment_id')
parser.add_argument('submission_id')

#python3 test_runner.py ./testing/first_assignment.zip  43491 155997 24388

class TestRunner():
    """
    Initializes and runs pipeine based on assignment configuration.
    """
    def __init__(self, attach_path: Path, config: dict):
        self.config: dict = config
        self.map: dict = {
            "ValidateDirectory": ValidateDirectory,
            "UnzipDirectory": UnzipDirectory,
            "JavaDoc": javaDocModule,
            "JUnit": JUnitModule,
            "Compile":CompileModule,
            "EndToEnd" : e2eModule
        }
        self.target = attach_path
        self.pipeline: List[TestModule] = []
        self.score = 0
        self.feedback = ""

    def build_pipeline(self):
        """
        Convert configuration of modules to a list of TestModules and store
        it in self.pipeline.
        """
        # start by moving this to init
        pipeline_config: dict = self.config['pipeline']
        
        self.input = TestInputWrapper(self.target)
        
        
        for module_config in pipeline_config['steps']: 
            test_module_class: ClassVar[TestModule] = self.map[module_config['type']]
            del module_config['type']
            test_module: TestModule = test_module_class(**module_config)
            self.pipeline.append(test_module)

    def run(self):
        for test_module in self.pipeline:
            
            test_module.run(self.input)
            self.score += test_module.get_score()
            self.feedback += test_module.feedback
            self.feedback += "\n"
            if test_module.get_testing_done():
                return

    def get_score(self):
        return self.score

    def get_feedback(self):
        return self.feedback

if __name__ == "__main__":
    args = parser.parse_args()
    test_dir = Path(args.test_dir)
    course = canvas.get_course(args.course_id)
    assignment = course.get_assignment(args.assignment_id)
    submission = assignment.get_submission(args.submission_id)

    ch = get_config_handler()
    config = ch.get_assignment_config(course, args.assignment_id)

    test_runner = TestRunner(test_dir, config)
    
    test_runner.build_pipeline()
    test_runner.run()

    score = test_runner.get_score()
    feedback = test_runner.get_feedback()
    submission.edit(submission={'posted_grade': score}, comment={'text_comment': feedback})
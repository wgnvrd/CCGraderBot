from typing import List, ClassVar
from pathlib import Path
import argparse
import sys
import json
from glob import glob

from CompileModule import CompileModule
from JUnitModule import JUnitModule
from UnzipDirectory import UnzipDirectory
from ValidateDirectory import ValidateDirectory
from e2eModule import e2eModule
from javaDocModule import javaDocModule
from settings import PROGRAM_DIR
from test_module import TestModule
from test_input_wrapper import TestInputWrapper
from CanvasHelper import get_canvas_api
from ConfigHandler import get_config_handler

canvas = get_canvas_api()

parser = argparse.ArgumentParser(
    prog="Test Runner",
    description="Build and run test pipelines based on config",
)
parser.add_argument('test_dir', type=Path)
parser.add_argument('course_id', type=int)
parser.add_argument('assignment_id', type=int)
parser.add_argument('submission_id', type=int)
parser.add_argument('user_id', type=int)

#python3 test_runner.py ./testing/first_assignment.zip  43491 155997 24388

OUT_DIR = PROGRAM_DIR / "test_output"

class TestRunner():
    """
    Initializes and runs pipeine based on assignment configuration.
    New Modules just need to be added to the below dictionary
    - Ensure that the input parameters for the module match the parameters in the config file INCLUDING parameter names
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
        self.input = None

    def build_pipeline(self):
        """
        Convert configuration of modules to a list of TestModules and store
        it in self.pipeline.
        """
        # start by moving this to init
        modules: list = self.config['modules']
        
        self.input = TestInputWrapper(self.target)
        
        for module in modules: 
            test_module_class: ClassVar[TestModule] = self.map[module['type']]
            del module['type']
            test_module: TestModule = test_module_class(**module)
            self.pipeline.append(test_module)

    def run(self):
        """
        Run each test -- if theres a fatal failure, ends the rest of the testing
        """
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
    # Any standard output here will be seen in the SLURM output
    args = parser.parse_args()
    test_dir = Path(args.test_dir)
    # course = canvas.get_course(args.course_id)
    # assignment = course.get_assignment(args.assignment_id)
    # submission = assignment.get_submission(args.submission_id)

    ch = get_config_handler()
    # course_config = ch.get_course_config_file(args.course_id)['default']
    config = ch.get_assignment_config(args.course_id, args.assignment_id)
    
    print(config)
    input_fname = list(test_dir.glob('*.zip'))[0]

    test_runner = TestRunner(test_dir / input_fname, config)
    
    test_runner.build_pipeline()
    test_runner.run()

    # (Band-aid code) For now, let's report score and feedback to Autograder by writing to a JSON file? 
    # We need a better solution for this
    score = test_runner.get_score()
    feedback = test_runner.get_feedback()

    # For SLURM logs
    print(score)
    print(feedback)
    
    output = {
        "course_id": args.course_id,
        "assignment_id": args.assignment_id,
        "submission_id": args.submission_id,
        "user_id": args.user_id,
        "score": score,
        "feedback": feedback
    }
    
    with open(OUT_DIR / f"{args.course_id}-{args.assignment_id}-{args.submission_id}.json", "w") as f:
        json.dump(output, f)

    # submission.edit(submission={'posted_grade': score}, comment={'text_comment': feedback})

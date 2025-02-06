from typing import List, ClassVar
from pathlib import Path
import argparse
import sys

from UnzipDirectory import UnzipDirectory
from ValidateDirectory import ValidateDirectory
from test_module import TestModule
from test_input_wrapper import TestInputWrapper
from CanvasHelper import get_canvas_api
from ConfigHandler import ConfigHandler

canvas = get_canvas_api()

parser = argparse.ArgumentParser(
    prog="Test Runner",
    description="Build and run test pipelines based on config",
)
parser.add_argument('test_dir')
parser.add_argument('course_id')
parser.add_argument('assignment_id')
parser.add_argument('submission_id')

class TestRunner():
    """
    Initializes and runs pipeine based on assignment configuration.
    """
    def __init__(self, test_folder: Path, config: dict):
        self.config: dict = config
        self.map: dict = {
            "ValidateDirectory": ValidateDirectory,
            "UnzipDirectory": UnzipDirectory
        }
        self.pipeline: List[TestModule] = []
        self.score = 0
        self.feedback = 0

    def build_pipeline(self):
        """
        Convert configuration of modules to a list of TestModules and store
        it in self.pipeline.
        """
        # start by moving this to init
        pipeline_config: dict = self.config['pipeline']
        self.input = TestInputWrapper(self.test_folder / self.pipeline['input'])

        for module_config in pipeline_config: 
            test_module_class: ClassVar[TestModule] = self.map[module_config['type']]
            del module_config['type']
            test_module: TestModule = test_module_class(**module_config)
            self.pipeline += test_module

    def run(self):
        for test_module in self.pipeline:
            test_module.run(self.input)
            self.score += test_module.get_score()
            self.feedback += test_module.feedback()
            self.feedback += "/n"

    def get_score(self):
        return self.score

    def get_feedback(self):
        return self.feedback

if __name__ == "__main__":
    args = parser.parse_args()
    course = canvas.get_course(args.course_id)
    assignment = canvas.get_assignment(args.assignment_id)
    submission = canvas.get_submission(args.submission_id)

    ch = ConfigHandler()
    config = ch.get_assignment_config(course, args.assignment_id)

    test_runner = TestRunner(args.test_dir, config)
    test_runner.build_pipeline()
    test_runner.run()

    score = test_runner.get_score()
    feedback = test_runner.get_feedback()
    submission.edit(submission={'posted_grade': score}, comment={'text_comment': feedback})
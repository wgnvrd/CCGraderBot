import os
from pathlib import Path
from typing import List
from test_input_wrapper import TestInputWrapper
from test_module import TestModule
from check_file import check_file;
class javaDocModule(TestModule):
    def __init__(self, max_score: float, files: List[Path], fatal = False):
        super().__init__()
        self.fatal = fatal
        self.max_score = max_score
        self.files = files


    def run(self, working_directory):
        allGood = True
        for f in self.files:
            f = working_directory.path / Path(f)
            try:
                with open( f) as file:
                    try:
                        problems = check_file(file)
                    except ValueError:
                        allGood = False
                        self.feedback += "\n Error in JavaDocChecker -- Will be manually reviewed"
                        
                if problems:
                    allGood = False
                    self.score = 0
                    self.feedback += f"\n{os.path.basename(f)}:"
                    self.feedback += "\n".join(problems)
                    if self.fatal:
                        self.testing_done = True


            except FileNotFoundError:
                print(f"\nFile \"{f}\" not found.")
                exit(1)
        if allGood:
            self.score = self.max_score
            self.feedback += "\n JavaDoc Test Passed"

        
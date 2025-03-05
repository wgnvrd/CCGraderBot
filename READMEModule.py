import os
from pathlib import Path
import subprocess
from typing import List
from test_input_wrapper import TestInputWrapper
from test_module import TestModule
from check_file import check_file;
class READMEModule(TestModule):
    def __init__(self, max_score: float, readMe: Path, fatal = False):
        super().__init__()
        self.fatal = fatal
        self.max_score = max_score
        self.readMe = readMe
        self.feedback += "\nREADME Check Test\n"


    def run(self, working_directory):
        results = subprocess.run(["python3", "C:/Users/nesmc/OneDrive/Desktop/Capstone/CCGraderBot/readme_file_checker.py", working_directory.path / self.readMe, working_directory.path],capture_output = True, text = True, cwd= working_directory.path)
        if results.returncode != 0:
            self.feedback += results.stdout
            self.feedback += "\n Did you forget to add any files to the README?"
            if self.fatal:
                self.testing_done = True
        else:
            self.feedback += results.stdout
            self.feedback += "README Check Passed"
            self.score = self.max_score

        
import os
from pathlib import Path
import zipfile

from test_module import TestModule
from test_result_enums import TestResult
from test_input_wrapper import TestInputWrapper

class UnzipDirectory(TestModule):
    def __init__(self, target: TestInputWrapper = TestInputWrapper("null"), max_score: int = 0, fatal = True):
        super().__init__()
        self.give_zip = False
        if isinstance(target, str):
            self.target = target
            self.give_zip = True
        
        self.max_score = max_score

    def run(self, working_directory: TestInputWrapper):
        
        self.dest = os.path.dirname(working_directory.path)
        if self.give_zip:
            working_directory.set_path(self.target)
        try:
            print(working_directory.path)
            with zipfile.ZipFile(working_directory.path, 'r') as zip_ref:
                zip_ref.extractall(self.dest)
            self.feedback = f"Unzipped {os.path.basename(working_directory.path)} to {os.path.basename(self.dest)}\n\n"
            self.score = self.max_score
            if self.give_zip:
                self.dest = self.dest +"/" +zip_ref.infolist()[1].filename.split("/")[0]
            working_directory.set_path(self.dest)
        except FileNotFoundError:
            self.score = 0
            self.testing_done = True
            self.feedback= f"ERROR: File {working_directory.path.name} Not Found -- Did you zip your files together properly? -- Try to avoid using characters like periods and brackets -- stick to letters, numbers and underscores!"

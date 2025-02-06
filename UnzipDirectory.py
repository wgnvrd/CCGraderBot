from pathlib import Path
import zipfile

from test_module import TestModule
from test_result_enums import TestResult
from test_input_wrapper import TestInputWrapper

class UnzipDirectory(TestModule):
    def __init__(self, target: TestInputWrapper, dest: Path, max_score: int = 0):
        self.target: TestInputWrapper = target
        self.dest = dest
        self.max_score = max_score

    def run(self):
        with zipfile.ZipFile(self.target.path, 'r') as zip_ref:
            zip_ref.extractall(self.dest)
        self.feedback = f"Unzipped {self.target.path} to {self.dest}"
        self.score = self.max_score
        self.target.set_path(self.dest)

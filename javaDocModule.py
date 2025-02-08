from pathlib import Path
from typing import List
from test_input_wrapper import TestInputWrapper
from test_module import TestModule
from check_file import check_file;
class javaDocModule(TestModule):
    def __init__(self, max_score: float, files: List[Path]):
        super().__init__()
        
        self.max_score = max_score
        self.files = files


    def run(self, working_directory):
        for f in self.files:
            f = working_directory.path / Path(f)
            try:
                with open( f) as file:
                    problems = check_file(file)
                if problems:
                    self.score = 0
                    self.feedback += f"\n{f}:"
                    self.feedback += "\n".join(problems)
                else:
                    self.score = self.max_score
                    self.feedback += "\n JavaDoc Test Passed"

            except FileNotFoundError:
                print(f"\nFile \"{f}\" not found.")
                exit(1)

        
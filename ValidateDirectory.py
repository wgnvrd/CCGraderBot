import os
from typing import List
from pathlib import Path

from test_module import TestModule
from test_result_enums import TestResult
from test_input_wrapper import TestInputWrapper

class ValidateDirectory(TestModule):
    def __init__(self,  max_score: float, root: Path, paths: List[Path], fatal = True):
        super().__init__()
        
        self.max_score = max_score
        self.root = Path(root)
        self.paths = [self.root / Path(p) for p in paths]

    def run(self, working_directory: TestInputWrapper):
        if not os.path.exists(working_directory.path / self.root):
            # maybe this should be an exception since this is a configuration error?
            self.feedback += f"Root directory {self.root} does not exist. Aborting. Please ensure that all of your files, including folers like src, are zipped up in an internal folder with the exact name {self.root}, i.e. instead of src/Example.java, {self.root}/src/Example.java\n "
            self.result = TestResult.FAIL
            self.testing_done = True
        else:
            for p in self.paths:
                if not os.path.exists(working_directory.path / p):
                    print(working_directory.path / p)
                    self.testing_done = True
                    self.feedback += f"File {p} does not exist. Aborting."
                    self.score = 0
                    self.result = TestResult.FAIL
                    return self.result
                self.feedback += f"{p} exists\n"
            self.score = self.max_score
            self.result = TestResult.PASS
            self.feedback += "PASSED VALIDATE DIRECTORY\n\n"
        working_directory.set_path(working_directory.path / self.root)
        return self.result

if __name__ == "__main__":
    vd = ValidateDirectory(
        2, 
        Path("C:\\Users\\isabe\\Documents\\repos\\cc-grader-bot\\testing\\downloads\\first_assignment\\first_assignment"), 
        [Path(p) for p in ["test/FirstTest.java", "src/First.java", "src/FirstI.java", "src/FirstException.java", "src/RunFirst.java"]]
    )
    vd.run()
    print(vd.get_score())
    print(vd.get_feedback())
    print(vd.result)

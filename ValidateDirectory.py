import os
from typing import List
from pathlib import Path

from test_module import TestModule
from test_result_enums import TestResult
from test_input_wrapper import TestInputWrapper

class ValidateDirectory(TestModule):
    def __init__(self, max_score: float, root: Path, paths: List[Path]):
        super().__init__()
        self.max_score = max_score
        self.root = Path("testing") / Path(root)
        self.paths = [self.root / Path(p) for p in paths]

    def run(self, folder):
        if not os.path.exists(self.root):
            # maybe this should be an exception since this is a configuration error?
            self.feedback += f"{self.root} does not exist. Aborting."
            self.result = TestResult.FAIL
        else:
            for p in self.paths:
                if not os.path.exists(p):
                    self.testing_done = True
                    self.feedback += f"{p.absolute()} does not exist. Aborting."
                    self.score = 0
                    self.result = TestResult.FAIL
                self.feedback += f"{p} exists\n"
            self.score = self.max_score
            self.result = TestResult.PASS
            self.feedback += "PASSED VALIDATE DIRECTORY\n\n"

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

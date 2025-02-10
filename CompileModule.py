import os
from pathlib import Path
import subprocess
from test_module import TestModule


class CompileModule(TestModule):
    def __init__(self,max_score,source):
        super().__init__()
        
        self.max_score = max_score
        self.source = source
        self.feedback += "\n COMPILATION TEST"

    def run(self, working_directory):
        self.paths = [working_directory.path / Path(p) for p in self.source]
        try:
            subprocess.run(["javac","-d", os.path.join(working_directory.path,"out"), "-cp", os.path.join("lib","junit-platform-console-standalone-1.11.4.jar"),*self.paths ])# self.source])
        except FileNotFoundError:
            self.feedback += "\n Compilation Error, FileNotFound"
            self.testing_done = True
            return
        self.score = self.max_score
        self.feedback += "\n Compilation Succesful"
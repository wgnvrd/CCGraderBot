import os
from pathlib import Path
import subprocess
from test_module import TestModule


class CompileModule(TestModule):
    def __init__(self,max_score,source, additional = []):
        super().__init__()
        
        self.max_score = max_score
        self.source = source
        self.feedback += "\n COMPILATION TEST"
        self.additional = additional

    def run(self, working_directory):
        self.paths = [working_directory.path / Path(p) for p in self.source]
        self.paths += self.additional
        try:
            subprocess.run(["javac","-d", os.path.join(working_directory.path,"out"), "-cp", os.path.join("lib","junit-platform-console-standalone-1.11.4.jar"),*self.paths], capture_output=True, text = True, check = True )# self.source])
        except FileNotFoundError:
            self.feedback += "\n Compilation Error, FileNotFound"
            self.testing_done = True
            return
        except Exception as e:
            self.feedback += f"Error : Compilation Not Successful"
            self.testing_done= True
            return
        except subprocess.CalledProcessError as e:
            self.feedback += f"Error: Compilation Not Successful"
            self.testing_done= True
        self.score = self.max_score
        self.feedback += "\n Compilation Succesful"
import subprocess
from test_module import TestModule
from test_result_enums import TestResult


class e2eModule(TestModule):
    def __init__(self, maxPoints, source_files, reqs):
        super().__init__(maxPoints)
       
        self.source = source_files
        self.reqs = reqs

    def run(self):
        
        # Not sure what this function call is gonna look like but I think that the idea is clear
        try:
            result = subprocess.run(['java', self.source], capture_output = True, text = True)
        except subprocess.CalledProcessError as e:
            self.feedback += "\n" + "Command failed with exit code:" + e.returncode 
            self.feedback += "\n" + "Error output:" + e.stderr.decode()
        #If output not an expected output -- set score to 0
        if result.stdout in self.reqs.keys():
            self.score = self.reqs[result.stdout]
        else:
            self.score = 0
        self.feedback += result.stdout


        self.testing_done = True



        

    


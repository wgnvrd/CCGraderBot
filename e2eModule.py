import subprocess
from test_module import TestModule
from test_result_enums import TestResult

"""
End to End Testing Module:
Max Points -- Not Sure if we need this -- may be removed
Command -- List of flags for command i.e. for "rm -rf" command = ["rm","-rf"]
reqs -- Dictionary where keys are final output of command and values are the points associated with that output
"""
class e2eModule(TestModule):
    def __init__(self, maxPoints, command, reqs):
        super().__init__(maxPoints)
       
        self.command = command
        self.reqs = reqs

    def run(self):
        
        # Not sure what this function call is gonna look like but I think that the idea is clear
        try:
            result = subprocess.run(self.command, capture_output = True, text = True)
        except subprocess.CalledProcessError as e:
            self.feedback += "\n" + "Command failed with exit code:" + e.returncode 
            self.feedback += "\n" + "Error output:" + e.stderr.decode()
        #If output not an expected output -- set score to 0
        self.feedback += result.stdout.split("\n")[-2]
        if self.feedback in self.reqs.keys():
            self.score = self.reqs[self.feedback]
        else:
            self.score = 0
        


        self.testing_done = True



        

    


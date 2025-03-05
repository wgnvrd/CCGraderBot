import subprocess
from test_module import TestModule
from test_result_enums import TestResult

"""
End to End Testing Module:
Max Points -- Not Sure if we need this -- may be removed
Command -- List of flags for command i.e. for "rm -rf" command = ["rm","-rf"]
reqs -- Dictionary where keys are final output of command and values are the points associated with that output
fatal -- if true, if this test fails, ends all further tests
"""
class e2eModule(TestModule):
    def __init__(self, max_score, command, reqs, fatal =False):
        super().__init__()
        self.max = max_score
        self.command = command
        self.reqs = reqs

    def run(self, working_directory):
        
        # Not sure what this function call is gonna look like but I think that the idea is clear
        try:
            print(self.command)
            result = subprocess.run(self.command, capture_output = True, text = True, cwd= working_directory.path, shell = True)
        except subprocess.CalledProcessError as e:
            print("error")
            self.feedback += "\n" + "Command failed with exit code:" + e.returncode 
            self.feedback += "\n" + "Error output:" + e.stderr.decode()
            if self.fatal:
                self.testing_done = True
        #If output not an expected output -- set score to 0
        #This checks the second to last line output -- we could make this configurable
        #Its like this because Java println and Python print both put \n at the end of lines, creating a empty line in the -1 position

        self.feedback += result.stdout
        if result.stdout.split("\n")[-2].strip() in self.reqs.keys():
            
            self.score = self.reqs[result.stdout.split("\n")[-2].strip()]
        else:
            self.score = 0
            if self.fatal:
                self.testing_done = True
        


    



        

    


from test_module import TestModule
from check_file import check_file;
class javaDocModule(TestModule):
    files = []
    def __init__(self,max, files):
        self.__init__(max)
        self.files = files


    def run(self):
        for f in self.files:
            try:
                with open(f) as file:
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

        self.testing_done = True
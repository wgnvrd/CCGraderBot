class TestModule():
    """
    All testing modules should subclass this module. Each instantiation of a test
    module should keep track of its own score and feedback output.
    """
    def __init__(self):
        self.score = 0 
        self.feedback = ""
        # Setting this to true should prevent accidental accumulation of scores?
        self.testingDone = False 

    def run(self):
        """
        Calculate score and feedback based on student submission and inputs. 
        """
        pass

    def get_score(self):
        return self.score 

    def get_feedback(self):
        return self.feedback 
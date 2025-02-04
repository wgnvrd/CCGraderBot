class TestModule():
    """
    All testing modules should subclass this module. Each instantiation of a test
    module should keep track of its own score and feedback output.
    """
    def __init__(self, max_score: int):
        self.score = 0 
        self.feedback = ""
        self.max_score = max_score # may or may not be useful in certain modules
        # Setting this to true should prevent accidental accumulation of scores?
        self.testing_done = False 
        self.result = None

    def run(self):
        """
        Calculate score and feedback based on student submission and inputs. 
        """
        pass

    def get_testing_done(self):
        return self.testing_done

    def get_score(self):
        return self.score 

    def get_feedback(self):
        return self.feedback 
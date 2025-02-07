import os
import subprocess
from pathlib import Path
from test_module import TestModule
import shutil

class PyDocAggregatorModule(TestModule):
    """
    This is one of the test modules that aggregates the javadoc
    in all given python files and puts the output in a specific
    directory called 'pydoc_aggregation_results'
    """
    def __init__(self,directory_name,filepaths):
        """
        This is the constructor for a PyDocAggregatorModule
        It takes in what you would like to call the folder where output will
        be stored(directory_name)
        and it also takes in a list of file paths to each of the files
        for which documentation should be collected
        """
        self.name = directory_name
        self.paths = filepaths
    
    def run(self):
        """
        The primary method of the class
        It loops through the list of given file paths and
        aggregates documentation for each of them
        """
        for path in self.paths:
            if not os.path.exists(path):
                print("File at filepath " + path + " was not found")
                return
        print("All given filepaths lead to existing files")
        
        pdoc_agg_results_storage = Path("./pydoc_aggregation_results")
        if not os.path.isdir(pdoc_agg_results_storage):
            os.mkdir(pdoc_agg_results_storage)
        
        doc_agg = os.path.join(pdoc_agg_results_storage,self.name)
        if os.path.isdir(doc_agg):
            shutil.rmtree(doc_agg)
        os.mkdir(doc_agg)

        for path in self.paths:
            subprocess.run(["python","-m","pydoc","-w",path])
            docfile = os.path.join(".",str(os.path.basename(path))[:-3] + ".html")  # os.path.join(".",str(str(path)[:-3] + ".html"))
            shutil.move(docfile,doc_agg)

if __name__ == "__main__":
    """
    The pseudo main method of the file made just for testing
    """
    jdam = PyDocAggregatorModule("Jane",["./testing/python_test_folder/python_test1.py","./testing/python_test_folder/python_test2.py"])
    # Yes, it does work on itself. Here's how to run it on the javadoc and pydoc aggregator modules
    # jdam = PyDocAggregatorModule("Meta",["./PyDocAggregatorModule.py","./JavaDocAggregatorModule.py"])
    jdam.run()    

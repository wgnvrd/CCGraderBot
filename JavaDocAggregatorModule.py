import os
import subprocess
from pathlib import Path
from test_module import TestModule
import shutil

class JavaDocAggregatorModule(TestModule):
    """
    This is one of the test modules that aggregates the javadoc
    in all given java files and puts the output in a specific
    directory called 'javadoc_aggregation_results'
    """
    def __init__(self,directory_name,filepaths):
        """
        This is the constructor for a JavaDocAggregatorModule
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
        
        jdoc_agg_results_storage = Path("./javadoc_aggregation_results")
        if not os.path.isdir(jdoc_agg_results_storage):
            os.mkdir(jdoc_agg_results_storage)
            print("Directory '%s' created" % jdoc_agg_results_storage)
        
        doc_agg = os.path.join(jdoc_agg_results_storage,self.name)
        if os.path.isdir(doc_agg):
            shutil.rmtree(doc_agg)
        os.mkdir(doc_agg)
        print("Directory '%s' created" % doc_agg)

        for path in self.paths:
            source_name = path.rsplit("/",1)[1]
            dirpath = os.path.join(doc_agg,source_name)
            if os.path.isdir(dirpath):
                shutil.rmtree(dirpath)
            os.makedirs(dirpath)
            print("Directory '%s' created" % dirpath)
            subprocess.run(["javadoc","-d",dirpath,path])
        

if __name__ == "__main__": 
    """
    The pseudo main method of the file made just for testing
    """
    jdam = JavaDocAggregatorModule("John",["./testing/java_test_folder/java_test1.java","./testing/java_test_folder/java_test2.java"])
    jdam.run()
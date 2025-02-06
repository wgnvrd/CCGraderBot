import os
import subprocess

import junitparser

from pathlib import Path

from glob import glob
import shutil

# remove this later
import configparser
from test_module import TestModule
from CanvasHelper import get_submission
from zipfile import ZipFile

class PyDocAggregatorModule(TestModule):
    def __init__(self,name,source):
        self.name = name
        self.source = source
        self.feedback = ""
    
    def run(self):
        srcFiles = os.path.join(".","testing",self.source)
        directory =  str(self.source) + "_" + str(self.name)
        parent_dir = "."
        path = os.path.join(parent_dir, directory)
        
        oldfile = os.path.join(path,str(str(self.source)[:-3] + ".html"))
        if os.path.exists(oldfile):
            os.remove(oldfile)
        if os.path.isdir(path):
            os.rmdir(path)
        

        os.makedirs(path)
        print("Directory '%s' created" % directory)
        subprocess.run(["python","-m","pydoc","-w",srcFiles])
        docfile = os.path.join(".",str(str(self.source)[:-3] + ".html"))
        goal = os.path.join(".",directory)
        shutil.move(docfile,goal)

if __name__ == "__main__":
    srcFiles = Path("python_test.py")
    pdam = PyDocAggregatorModule("Jane",srcFiles)
    pdam.run()     

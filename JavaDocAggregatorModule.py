import os
import subprocess

import junitparser

from pathlib import Path

from glob import glob

# remove this later
import configparser
from test_module import TestModule
from CanvasHelper import get_submission
from zipfile import ZipFile

class JavaDocAggregatorModule(TestModule):
    def __init__(self,name,source):
        self.name = name
        self.source = source

        self.feedback = ""

    def run(self):
        srcFiles = os.path.join(".","testing",self.source)
        directory =  str(self.source) + "_" + str(self.name)
        parent_dir = "."
        path = os.path.join(parent_dir, directory)
        os.makedirs(path)
        print("Directory '%s' created" % directory)
        subprocess.run(["javadoc","-d",path,srcFiles])

if __name__ == "__main__":    
    srcFiles = Path("test_doc.java")
    jdam = JavaDocAggregatorModule("John",srcFiles)
    jdam.run()     

from test_module import TestModule

import subprocess
import time

class PyRuntimeModule(TestModule):
    """
    This module is responsible for collecting runtime data on student python submissions.
    It should aggregate a configurable number of tests to be able to account for any potential
    inconsistencies
    """
    def __init__(self,python_file_paths,exec_num):
        """
        This is the constructor for a RuntimeModule instance
        In this placeholder, it stores a folder of runtimes it collects
        """
        super().__init__()
        self.runtimes = []
        self.agg_runtime = 0
        self.python_file_paths = python_file_paths
        self.exec_num = exec_num

    def format_seconds(self,seconds):
        """
        Formatting method for the wall clock runtime
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = round(seconds % 60,5)
        return f"{hours} hours {minutes} minutes {remaining_seconds} seconds"

    def run(self):
        """
        Run method for the python runtime module
        This method aggregates multiple runs of all given files 
        by executing a command using the Linux 'time' utility 
        to retrieves the wall clock runtime for all given filepaths
        """
        for path in self.python_file_paths:
            try:
                for i in range(0,self.exec_num):
                    start_time = time.perf_counter()
                    subprocess.run(['python3', path])
                    end_time = time.perf_counter()
                    runtime = end_time - start_time
                    self.runtimes.append(runtime)
                self.agg_runtime = sum(self.runtimes) / len(self.runtimes)
                duration = self.format_seconds(self.agg_runtime)
                self.feedback += f"The aggregated wall clock runtime of '{path}' across {self.exec_num} run(s) is: {duration}\n"
            except subprocess.CalledProcessError as e:
                print(f"Error executing Python file: {e}")
                return None
            except FileNotFoundError:
                print(f"Python file not found at path: {path}")
                return None

if __name__ == "__main__":
    """
    Main method for testing purposes
    """
    path_list = ["./testing/python_test_folder/python_test1.py","./testing/python_test_folder/python_test2.py","./testing/python_test_folder/python_test3.py","./testing/python_test_folder/python_test4.py"]
    prm = PyRuntimeModule(path_list,3)
    print("Made PyRuntimeModule")
    prm.run()
    print(prm.get_feedback())

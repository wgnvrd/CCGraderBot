from test_module import TestModule

import subprocess
import time

class JavaRuntimeModule(TestModule):
    """
    This module is responsible for collecting runtime data on student java submissions.
    It should aggregate a configurable number of tests to be able to account for any potential
    inconsistencies
    """

    def __init__(self,java_file_paths,exec_num):
        """
        This is the constructor for a JavaRuntimeModule instance
        It stores a folder for the runtimes it collects, a variable for the aggregated runtime,
        a list of filepaths to test, and a number of times each file should be timed
        """
        super().__init__()
        self.runtimes = []
        self.agg_runtime = 0
        self.java_file_paths = java_file_paths
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
        Run method for the java runtime module
        This method aggregates multiple runs of all given files 
        by executing a command using the Linux 'time' utility 
        to retrieve the wall clock runtime for all given filepaths
        """
        for path in self.java_file_paths:
            try:
                for i in range(0,self.exec_num):
                    start_time = time.perf_counter()
                    subprocess.run(['java', path])
                    end_time = time.perf_counter()
                    runtime = end_time - start_time
                    self.runtimes.append(runtime)
                self.agg_runtime = sum(self.runtimes) / len(self.runtimes)
                duration = self.format_seconds(self.agg_runtime)
                self.feedback += f"The aggregated wall clock runtime of '{path}' across {self.exec_num} run(s) is: {duration}\n"
            except subprocess.CalledProcessError as e:
                print(f"Error executing Java file: {e}")
                return None
            except FileNotFoundError:
                print(f"Java file not found at path: {path}")
                return None

if __name__ == "__main__":
    path_list = ["./testing/java_test_folder/java_test1.java","./testing/java_test_folder/java_test2.java","./testing/java_test_folder/java_test3.java"]
    jrm = JavaRuntimeModule(path_list,3)
    print("Made JavaRuntimeModule")
    jrm.run()
    print(jrm.get_feedback())

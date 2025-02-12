from test_module import TestModule

import subprocess
import os
import time

class CRuntimeModule(TestModule):
    """
    This module is responsible for collecting runtime data on student C submissions.
    It should aggregate a configurable number of tests to be able to account for any potential
    inconsistencies
    """
    def __init__(self,c_file_paths,exec_num):
        """
        This is the constructor for a RuntimeModule instance
        In this placeholder, it stores a folder of runtimes it collects
        """
        super().__init__()
        self.runtimes = []
        self.agg_runtime = 0
        self.c_file_paths = c_file_paths
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
        Run method for the C runtime module
        This method aggregates multiple runs of all given files 
        by executing a command using the Linux 'time' utility 
        to retrieve the wall clock runtime for all given filepaths
        Specifically, this implementation compiles the code at the start
        then times each run command before aggregating them into
        an average time
        """
        for path in self.c_file_paths:
            self.runtimes = []
            try:
                executable_name = os.path.splitext(path)[0]
                if os.path.exists(path[:-2]):
                    os.remove(path[:-2])
                
                # Compile the C code 
                compile_process = subprocess.run(['gcc', path, '-o', executable_name],
                                                capture_output=True, text=True)

                # Check for compilation errors
                if compile_process.returncode != 0:
                    print(f"Compilation error:\n{compile_process.stderr}")
                    return None
                
                # Run the code for the given number of test runs
                for i in range(0,self.exec_num):
                    start_time = time.perf_counter()
                    # Run the compiled executable
                    run_process = subprocess.run([executable_name], capture_output=True, text=True)
                    end_time = time.perf_counter()
                    runtime = end_time - start_time
                    self.runtimes.append(runtime)
                
                # remove the compile file
                if os.path.exists(path[:-2]):
                    os.remove(path[:-2])
                
                # Calculate and format the aggregated wall clock runtime
                self.agg_runtime = sum(self.runtimes) / len(self.runtimes)
                duration = self.format_seconds(self.agg_runtime)
                self.feedback += f"The aggregated wall clock runtime of '{path}' across {self.exec_num} run(s) is: {duration}\n"
            except subprocess.CalledProcessError as e:
                print(f"An error occurred: {e}")
                return None
            except FileNotFoundError:
                print(f"File not found: {path}")
                return None

if __name__ == "__main__":
    """
    Main method for testing purposes
    """
    path_list = ["./testing/c_test_folder/c_test1.c","./testing/c_test_folder/c_test2.c","./testing/c_test_folder/c_test3.c","./testing/c_test_folder/c_test4.c"]
    prm = CRuntimeModule(path_list,3)
    print("Made CRuntimeModule")
    prm.run()
    print(prm.get_feedback())

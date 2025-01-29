import os
import subprocess
from pathlib import Path
from canvasapi import Submission

"""
Generate an sbatch script
Submit the script to SLURM using sbatch <script name>
Use squeue or some artifact left in the file system to check that the run is complete
"""
class SLURMRunner():
    def __init__(self, dest_dir):
        self.dest_dir = Path(dest_dir)

    def download_attachments(submission: Submission):
        """
        Download attachments to the following directory: 
        `{course}-{course_id}/{assignment_name}-{assignment_id}/{user_name}-{user_id}/attempt-{submission_attempt}/`
        """
        course_id = submission.course_id
        assignment_id = submission.assignment_id
        user_id = submission.user_id
        submission = submission.attempt
        download_path = self.dest_dir # /

    def slurm_deploy(self, assignment):
        pass
        # make folder

        # download assignments to folder
        # retrieve test script
        # run test script on assignment
        # return True if successful
           

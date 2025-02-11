import subprocess
from pathlib import Path
from textwrap import dedent

from canvasapi.submission import Submission

from CanvasHelper import get_canvas_api
from ConfigHandler import get_config_handler
from settings import PROGRAM_DIR

canvas = get_canvas_api()

SLURM_DIR = PROGRAM_DIR  / "slurm"
"""
Generate an sbatch script
Submit the script to SLURM using sbatch <script name>
Use squeue or some artifact left in the file system to check that the run is complete
"""
class SLURMRunner():
    def __init__(self):
        self.ch = get_config_handler()

    # def download_attachments(self, s: Submission):
    #     """
    #     Download attachments to the following directory: 
    #     `{course}-{course_id}/{assignment_name}-{assignment_id}/{user_name}-{user_id}/attempt-{submission_attempt}/`
    #     """
    #     course = canvas.get_course(s.course_id)
    #     assignment = course.get_assignment(s.assignment_id)
    #     # user = canvas.get_user(s.user_id)
    #     user_id = s.user_id
    #     attempt = s.attempt

    #     # download_path = self.dest_dir / f"{course.name}-{course.id}" / f"{assignment.name}-{assignment.id}" / f"{user.name}-{user.id}" / f"attempt-{attempt}"
    #     # This is specifically for the test user. The above path is correct.
    #     download_path = self.dest_dir / f"{course.name}-{course.id}" / f"test_user-{user_id}" / f"{assignment.name}-{assignment.id}-attempt-{attempt}"
    #     if not download_path.exists():
    #         download_path.mkdir(parents=True, exist_ok=True)

    #     for attachment in s.attachments:
    #         attachment.download(download_path / attachment.display_name)

    def get_slurm_script_path(self, s: Submission) -> Path:
        return Path(f"autograde-{s.course_id}-{s.assignment_id}.slurm")

    def generate_slurm_script(self, s: Submission, test_dir: Path):
        """
        Generate a SLURM script template.
        Output scripts will have format assignment_name-user_id-attempt_number-job_number.out 
        Ideally Canvas grading will be based on SLURM output.
        Tests will be run within SLURM.
        Output for grading can be logged in a separate file based on test results.
        This file will be used to assign a score.
        """
        course_id = s.course_id
        assignment_id = s.assignment_id
        submission_id = s.id
        user_id = s.user_id
        # course = canvas.get_course(course_id)
        config = self.ch.get_course_config_file(course_id)['default']
        repo_location = "/home/i_wagenvoord/cc-grader-bot"
        slurm_script_path = self.get_slurm_script_path(s)
        print(slurm_script_path)
        print(config)
        # unit_tests = config["pipeline"]["steps"][0]["path"] # hard-coded
        script = f"""#!/bin/bash
            #SBATCH --job-name={slurm_script_path.name}-{"{}"}{"{}"}
            #SBATCH --output=%j.out
            #SBATCH --nodes=1
            #SBATCH --ntasks=1
            #SBATCH --cpus-per-task=1
            #SBATCH --time=00:01:00

            echo %j
            module load {config['module-name']}
            cd {repo_location} 
            python3 test_runner.py {test_dir} {course_id} {assignment_id} {submission_id} {user_id}
        """
        script = dedent(script)
        # print(s)
            # {unit_tests} {config['pipeline']['input']}
        with open(slurm_script_path, "w") as f:
            f.write(script)

    def execute(self, s: Submission):
        """
        Run given script in the command line. 
        """
        slurm_script_path = self.get_slurm_script_path(s)
        print(slurm_script_path)
        result = subprocess.run(["sbatch", slurm_script_path.absolute()])
        subprocess.run(["squeue"]) # demo purposes
        return result

    # def get_slurm_script(self, s: Submission) -> Path:
    #     """
    #     Retrieve an assignment's associated SLURM script.
    #     If a SLURM script doesn't exist, generate one based on
    #     the configuration file.
    #     """
    #     name = f"autograde-{s.course_id}-{s.assignment_id}"
    #     slurm_script_path = SLURM_DIR / name
    #     return slurm_script_path

    def deploy(self, s: Submission, test_dir: Path):
        """
        Given a submission:
            1. Write SLURM script
            2. Deploy it
        """
        # make folder
        # self.download_attachments(s)
        # retrieve test script
        self.generate_slurm_script(s, test_dir)
        self.execute(s)
        # 2023b2_cp222/bin/test_first_assignment first_assignment_done.zip
        # run test script on assignment
        # return True if successful
           
# TEMPORARY FOR DEBUGGING
 # ID for CP222: 43491
    # # ID for Recall JAVA: 155997
    # # ID of submission: 3331124
    # # ID of user: 24366
# It would be a good idea to have a program that generates a base configuration file for you?
if __name__ == "__main__":
    sr = SLURMRunner('testing/downloads')
    course = canvas.get_course(43491)
    assignment = course.get_assignment(155997)
    submission = assignment.get_submissions()[0]
    print(submission)
    sr.slurm_deploy(submission)

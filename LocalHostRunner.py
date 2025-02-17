from pathlib import Path
import subprocess
import sys

from canvasapi.submission import Submission
from ConfigHandler import get_config_handler
from settings import PROGRAM_DIR

LOG_DIR = PROGRAM_DIR / "logs"

class LocalHostRunner():
    def __init__(self):
        self.ch = get_config_handler()

    def get_output_path(self, s: Submission) -> Path:
        return LOG_DIR / f"localhost-autograde-{s.course_id}-{s.assignment_id}-attempt{s.attempt}.out"

    def execute(self, s: Submission, test_dir: Path):
        # different arguments than SLURMRunner.execute()...
        course_id = s.course_id
        assignment_id = s.assignment_id
        submission_id = s.id
        user_id = s.user_id
        cmd = f"python3 test_runner.py {test_dir} {course_id} {assignment_id} {submission_id} {user_id}"
        path = self.get_output_path(s)
        print("Executing", cmd)
        with open(path, "w") as out:
            result = subprocess.run(cmd.split(" "), stdout=out)
        return result

    def deploy(self, s: Submission, test_dir: Path):
        self.execute(s, test_dir)
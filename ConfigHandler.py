from pathlib import Path

from canvasapi import course
from slugify import slugify
import tomlkit

from CanvasHelper import canvas

CONFIG_DIR=Path("/home/i_wagenvoord")

class ConfigHandler():
    """
    Parses configuration files which will dictate how student 
    submissions are tested and graded.
    `autograder.toml` provides a mapping of Canvas course IDs to their
    corresponding configuration files. 
    """
    def __init__(self):
        self.config_file_path = self.get_config_file_path()
        if not self.config_file_path.exists():
            self.generate_autograder_config()

    def get_config_file_path(self) -> Path:
        """ Return absolute path of `autograder.toml`. """
        path = CONFIG_DIR / "autograder.toml" 
        return path

    def generate_autograder_config(self):
        """
        Generate a config file for the entire Autograder program. 
        """
        doc = tomlkit.document()
        doc.add(tomlkit.comment("Autograder uses this to map from Canvas course IDs to course config files."))
        doc.add(tomlkit.nl())
        doc["course-configs"] = tomlkit.table()
        with open(self.config_file_path, "wb") as f:
            tomlkit.dumps(doc, f)

    def add_course_to_autograder_config(self):
        doc = tomlkit.load(self.config_file_path)
        course_id = self.course_id
        fname = f"{slugify(course.name)}-{course_id}.toml"
        doc["course-configs"][course_id] = fname
        with open(self.config_file_path, "wb") as f:
            tomlkit.dump(doc, f)

    def get_course_config_path(self, course: course) -> Path:
        """
        Retrieve corresponding course configuration file using course ID.
        """
        doc = tomlkit.load(self.config_file_path)
        fname = doc["course-configs"][course.id]
        return CONFIG_DIR / fname

    def generate_course_config(self, course: course):
        """
        Generate configuration file for a given course.
        """
        config_path = self.get_course_config_path(course)

        s = f"""
        # AUTOGRADING CONFIGURATION FOR {course.name}
        [default]
        course_id = {course.id}
        course_name = "{course.name}"
        module_name = ""
        unit_test_dir = ""
        """
        doc = tomlkit.parse(s)
        assignment_ids = [a.id for a in course.get_assignments()]
        for assignment_id in assignment_ids:
            doc.add(str(assignment_id), tomlkit.table()) 

        with open(config_path, "wb") as f:
            tomlkit.dump(doc, f)
        

    def read_assignment_config(self, assign_id):
        """
        Read associated course file and return appropriate assignment config
        """
        pass

    def get_autograded_assignments(self, course_id):
        """
        Return IDs of assignments to be autograded. 
        """

if __name__ == "__main__":
    course = canvas.get_course(43491)
    ch = ConfigHandler()
    ch.generate_course_config(course)

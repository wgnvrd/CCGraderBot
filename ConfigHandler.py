from pathlib import Path
from textwrap import dedent

from canvasapi import course
from slugify import slugify
import tomlkit

from CanvasHelper import canvas

# CONFIG_DIR = Path("/home/i_wagenvoord/autograder/")
CONFIG_DIR = Path("/home/i_wagenvoord/autograding/config_files")

if not CONFIG_DIR.exists():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

class ConfigHandler():
    """
    Parses configuration files which will dictate how student 
    submissions are tested and graded.
    `autograder.toml` provides a mapping of Canvas course IDs to their
    corresponding configuration files. 
    Automatically generates templates for files.
    """
    def __init__(self):
        self.config_file_path = self.get_config_file_path()
        print(self.config_file_path)
        if not self.config_file_path.exists():
            print("Generating autograder.toml")
            self.generate_autograder_config()

    def get_config_file_path(self) -> Path:
        """ Return absolute path of `autograder.toml`. """
        path = CONFIG_DIR / "autograder.toml" 
        return path

    def get_config_file(self):
        """ Get the config file as a TOMLDocument """
        with open(self.config_file_path, "r") as f:
            doc = tomlkit.load(f)
        return doc

    def get_course_config_file(self, course_id: int):
        path = self.get_course_config_path(course_id)
        with open(path, "r") as f:
            doc = tomlkit.load(f)
        return doc

    def generate_autograder_config(self):
        """
        Generate a config file for the entire Autograder program. 
        """
        doc = tomlkit.document()
        doc.add(tomlkit.comment("Autograder uses this to map from Canvas course IDs to course config files."))
        doc.add(tomlkit.nl())
        doc.add("course-configs", tomlkit.table())
        with open(self.config_file_path, "w") as f:
            s = tomlkit.dumps(doc)
            f.write(s)
            # tomlkit.dump(doc, f)

    def add_course_to_autograder_config(self, course: course):
        doc = self.get_config_file()
        fname = f"{slugify(course.name)}-{course.id}.toml"
        doc["course-configs"].add(str(course.id), fname)
        with open(self.config_file_path, "w") as f:
            tomlkit.dump(doc, f)

    def get_course_config_path(self, course_id: int) -> Path:
        """
        Retrieve corresponding course configuration file using course ID.
        """
        doc = self.get_config_file()
        # if str(course.id) not in doc["course-configs"]: 
        #     self.add_course_to_autograder_config(course)
        # doc = self.get_config_file()
        fname = doc["course-configs"][str(course_id)]

        return CONFIG_DIR / fname

    def generate_course_config(self, course: course):
        """
        Generate configuration file for a given course. If the file already exists, update with any new assignments.
        """
        config_path = self.get_course_config_path(course.id)
        if not config_path.exists():
            s = f"""
            # AUTOGRADING CONFIGURATION FOR {course.name}
            [default]
            course-id = {course.id}
            course-name = "{course.name}"
            module-name = ""
            unit-test-dir = ""
            """
            s = dedent(s)
            doc = tomlkit.parse(s)
            for a in course.get_assignments():
                doc.add(str(a.id), {
                        "assignment-name": a.name,
                        "pipeline": tomlkit.table()
                    }) 
            with open(config_path, "w") as f:
                 tomlkit.dump(doc, f)
        else:
            # TODO: If config file already exists, just add new assignments that aren't yet in the file?
            pass

    def get_course_defaults(self, course_id: int):
        doc = self.get_course_config_file(course_id)
        return dict(doc)["default"]

    def get_assignment_config(self, course_id: int, assign_id: int):
        """
        Read associated course file and return appropriate assignment config
        """
        doc = self.get_course_config_file(course_id)
        return dict(doc)[str(assign_id)]

ch = ConfigHandler()
def get_config_handler() -> ConfigHandler:
    return ch
    
if __name__ == "__main__":
    course = canvas.get_course(43491)
    ch = ConfigHandler()
    ch.generate_course_config(course)
    print(ch.get_assignment_config(course, 155997))
    print(ch.get_course_defaults(course))

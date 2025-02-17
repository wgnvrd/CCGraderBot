from pathlib import Path
from textwrap import dedent

from canvasapi import course
from slugify import slugify
import tomlkit

from CanvasHelper import canvas
from CanvasHelper import get_course_url, get_assignment_url
from settings import PROGRAM_DIR

CONFIG_DIR = PROGRAM_DIR / "config_files"

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

        self.assignment_mappings = {}

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
        with open(CONFIG_DIR / path, "r") as f:
            doc = tomlkit.load(f)
        return doc

    def generate_autograder_config(self):
        """
        Generate a config file for the entire Autograder program. 
        """
        doc = tomlkit.document()
        doc.add(tomlkit.comment("Autograder uses this to map from Canvas course IDs to course config files."))
        doc.add(tomlkit.nl())
        doc.add("course_configs", tomlkit.table())
        with open(self.config_file_path, "w") as f:
            s = tomlkit.dumps(doc)
            f.write(s)
            # tomlkit.dump(doc, f)

    def add_course_to_autograder_config(self, course_id: int):
        course = canvas.get_course(course_id)
        doc = self.get_config_file()
        fname = f"{slugify(course.name)}-{course.id}.toml"
        doc["course_configs"].add(str(course.id), fname)
        with open(self.config_file_path, "w") as f:
            tomlkit.dump(doc, f)

    def get_course_config_path(self, course_id: int) -> Path:
        """
        Retrieve corresponding course configuration file using course ID.
        """
        doc = self.get_config_file()
        # if str(course.id) not in doc["course_configs"]: 
        #     self.add_course_to_autograder_config(course)
        # doc = self.get_config_file()
        fname = doc["course_configs"][str(course_id)]

        return CONFIG_DIR / fname
    def check_active(self,  course_id, assign_id):
        if course_id not in self.assignment_mappings:
            self.parse_assignment_configs(course_id)
        if assign_id not in self.assignment_mappings[course_id]:
            return False
        doc = self.get_assignment_config(course_id, assign_id)
        # What should happen if "active" key isn't included?
        return "active" in doc and doc["active"]

    def generate_course_config(self, course_id: int):
        """
        Generate configuration file for a given course. If the file already exists, update with any new assignments.
        """
        course = canvas.get_course(course_id)
        # check if course file already listed in autograder.toml
        doc = type(self.get_config_file())
        if course_id not in doc['course_configs']:
            self.add_course_to_autograder_config(course_id)

        # Retrieve the path of the configuration file from autograder.toml
        config_path = self.get_course_config_path(course_id)

        # If the file doesn't exist, generate it using a template.
        if not config_path.exists():
            s = f"""
            # AUTOGRADING CONFIGURATION FOR {course.name}
            [meta]
            course_name = "{course.name}"
            course_id = {course.id} 
            url = "{get_course_url(course.id)}"

            [course]
            lua_module = ""
            unit_test_dir = ""
            """
            s = dedent(s)
            doc = tomlkit.parse(s)
            for a in course.get_assignments():
                assignment_name = slugify(a.name)
                doc.add(assignment_name, {
                        "id": a.id,
                        "url": get_assignment_url(course.id, a.id),
                        "active": False,
                        "input": "",
                        "modules": tomlkit.table()
                        
                    })
            with open(config_path, "w") as f:
                 tomlkit.dump(doc, f)
            return True
        else:
            return False

    def update_meta(self):
        """ If the id of an assignment or course is different, update the metadata. """
        pass

    def get_course_settings(self, course_id: int):
        doc = self.get_course_config_file(course_id)
        return dict(doc)["course"]

    def parse_assignment_configs(self, course_id: int):
        """ Get hashmap of id mappings to their corresponding assignment configurations. """
        doc = self.get_course_config_file(course_id)
        assignments = dict(doc)
        del assignments["meta"]
        del assignments["course"]
        mappings = {v['id']: v for v in dict(assignments).values() if 'id' in v}
        self.assignment_mappings.update({course_id: mappings})

    def get_assignment_config(self, course_id: int, assignment_id: int):
        """
        Read associated course file and return appropriate assignment config
        """
        # doc = self.get_course_config_file(course_id)
        # return dict(doc)[str(assign_id)]
        if course_id not in self.assignment_mappings:
            self.parse_assignment_configs(course_id)
        return self.assignment_mappings[course_id][assignment_id]

ch = ConfigHandler()
def get_config_handler() -> ConfigHandler:
    return ch
    
if __name__ == "__main__":
    course = canvas.get_course(43491)
    ch = ConfigHandler()
    ch.generate_course_config(course)
    print(ch.get_assignment_config(course, 155997))
    print(ch.get_course_settings(course))

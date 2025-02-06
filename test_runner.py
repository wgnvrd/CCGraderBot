from typing import List, ClassVar
from pathlib import Path

from UnzipDirectory import UnzipDirectory
from ValidateDirectory import ValidateDirectory
from test_module import TestModule
from test_input_wrapper import TestInputWrapper

class TestRunner():
    """
    Initializes and runs pipeine based on assignment configuration.
    """
    def __init__(self, test_folder: Path, config: dict):
        self.config: dict = config
        self.map: dict = {
            "ValidateDirectory": ValidateDirectory,
            "UnzipDirectory": UnzipDirectory
        }
        self.pipeline: List[TestModule] = []
        self.score = 0
        self.feedback = 0

    def build_pipeline(self):
        """
        Convert configuration of modules to a list of TestModules and store
        it in self.pipeline.
        """
        # start by moving this to init
        pipeline_config: dict = self.config['pipeline']
        self.input = TestInputWrapper(self.test_folder / self.pipeline['input'])

        for module_config in pipeline_config: 
            test_module_class: ClassVar[TestModule] = self.map[module_config['type']]
            del module_config['type']
            test_module: TestModule = test_module_class(**module_config)
            self.pipeline += test_module

    def run(self):
        for test_module in self.pipeline:
            test_module.run(self.input)
            self.score += test_module.get_score()
            self.feedback += test_module.feedback()
            self.feedback += "/n"


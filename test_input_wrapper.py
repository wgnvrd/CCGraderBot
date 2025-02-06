from pathlib import Path

class TestInputWrapper():
    """
    Keeps track of path to input. This is used as input to test modules which
    then modify the path here.  
    """
    def __init__(self, path: Path):
        self.path: Path = Path(path)

    def set_path(self, path: Path):
        self.path= path
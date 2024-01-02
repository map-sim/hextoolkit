from forum import example_config as example_controls
from diagram import example_config as example_diagram

from diagram import Diagram
from forum import Forum

class Engine:
    processes = {
        "A": None,
        "B": None,
        "C": None,
        "AB": {"A": 1.0, "B": 1.0},
        "BC": {"B": 1.0, "C": 1.0},
        "AC": {"A": 1.0, "C": 1.0},
        "ABC": {"A": 1.0, "B": 1.0, "C": 1.0},
        "<consumption>": "AB",
        "<development>": "BC",
        "<industrial>": "AC",
        "<science>": "ABC"
    }

    def __init__(self, diagram_config, controls_config):
        self.diagram = Diagram()
        self.forum = Forum()
        self.diagram.load_from_json(diagram_config)
        self.forum.load_from_json(controls_config)
        self.step = 0

    def run(self):
        print(f"============\nrun {self.step}...")
        for node in self.diagram.values():
            node.run()
        self.step += 1

if __name__ == "__main__":
    engine = Engine(example_diagram, example_controls)
    engine.run()
    engine.run()

from diagram import Diagram


class World:
    constants = {
        "<science>-factor": 1.0,
        "<industrial>-factor": 1.0,
        "<consumption>-factor": 1.0,
        "<development>-factor": 1.0,
        "base-build-capacity": 10.0,
        "base-node-capacity": 1000.0
    }
    technologies = [
        ("production", "A"),
        ("production", "B"),
        ("production", "C"),
        ("mixing", "ABC"),
        ("mixing", "AB"),
        ("mixing", "BC"),
        ("mixing", "AC")
    ]
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

    def __init__(self):
        self.controls = []
        self.diagram = Diagram()

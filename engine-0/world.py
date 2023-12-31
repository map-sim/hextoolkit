from diagram import Diagram


class Engine:
    constants = {
        "<science>-factor": 1.0,
        "<industry>-factor": 1.0,
        "<consumption>-factor": 1.0,
        "<development>-factor": 1.0,
        "base-build-popacity": 10.0,
        "base-node-popacity": 1000.0
    }
    technologies = [
        ("production", "A"), ("production", "B"), ("production", "C"),
        ("mixing", "ABC"), ("mixing", "AB"), ("mixing", "BC"), ("mixing", "AC"),
        ("army", "unit-size"), ("army", "offensive"), ("army", "defence")
    ]
    buildings = [
        ("productor", "A"), ("productor", "B"), ("productor", "C"),
        ("mixer", "AB"), ("mixer", "BC"), ("mixer", "AC"), ("mixer", "ABC"),
        ("military", None), ("transport", None), ("management", None), ("residence", None),
        ("effector", "<science>"), ("effector", "<development>")
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
        "<industry>": "AC",
        "<science>": "ABC"
    }

    def __init__(self):
        self.controls = []
        self.diagram = Diagram()

class Node(dict):
    __obligatory = {
        "name", "buildable", "navigable",
        "availability", "population"}
    __optional_dicts = {
        "support", "sources",
        "buildings", "assets"}
    __names = set()

    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return self.name != other.name
    def __hash__(self):
        return hash(self.name)

    def __init__(self, config, diagram):
        dict.__init__(self)
        self.diagram = diagram
        for key in self.__obligatory:
            assert key in config, f"no {key} in node config"
        assert config["name"] not in self.__names, config["name"] 
        self.__names.add(config["name"])
        for k, v in config.items():
            setattr(self, k, v)
        for key in self.__optional_dicts:
            if key not in config: setattr(self, key, {})            
        print(self)

    def eval_pop_capacity():
        bn = self.diagram.constants["base-node-pop-capacity"]
        bb = self.diagram.constants["base-build-pop-capacity"]
        capacity = bn + bb *  self.buildings.get("residence", 0)
        return capacity

    def __str__(self):
        out = "[NODE]--------------------"
        out += f"\nname: {self.name}"
        if self.navigable: out += "*"
        out += f"\npopulation: {self.population}"
        return out + "\n--------------------[NODE]"

    def run(self):
        print(f"run {self.name}...")
    
class Diagram(dict):
    constants = {
        "<science>-factor": 1.0,
        "<industrial>-army-factor": 1.0,
        "<industrial>-glory-factor": 1.0,
        "<consumption>-factor": 1.0,
        "<development>-factor": 1.0,
        "base-build-pop-capacity": 10.0,
        "base-node-pop-capacity": 1000.0
    }
    buildings = [
        "product A", "product B", "product C",
        "mixer AB", "mixer BC", "mixer AC", "mixer ABC",
        "military", "transport", "science", "residence",
        "emporium", "glory", "management", "development"
    ]

    def __init__(self):
        dict.__init__(self)

    def load_from_json(self, config):
        assert "nodes" in config
        assert "links" in config
        for n in config["nodes"]:
            node = Node(n, self)
            self[node.name] = node
        for f, t, v in config["links"]:
            self[f][t] = v

example_config = {
    "nodes": [
        {
            "name": "A1",
            "buildable": 0.9,
            "buildings":{
                "residence": 10},
            "navigable": False,
            "availability": 0.5,
            "population": 720},
        {
            "name": "B2",
            "buildable": 0.8,
            "buildings":{
                "residence": 10},
            "navigable": False,
            "availability": 0.55,
            "population": 520},
        {
            "name": "C3",
            "buildable": 0.0,
            "navigable": True,
            "availability": 0.95,
            "population": 0},
        {
            "name": "D4",
            "buildable": 0.07,
            "buildings":{
                "residence": 5},
            "navigable": True,
            "availability": 0.9,
            "population": 20}
    ],
    "links": [
        ["A1", "B2", 0.5],
        ["A1", "C3", 0.2],
        ["B2", "A1", 0.6],
        ["B2", "C3", 0.25],
        ["C3", "A1", 0.2],
        ["C3", "B2", 0.25],
        ["C3", "D4", 0.98],
        ["D4", "C3", 0.95]
    ]
}

if __name__ == "__main__":
    diagram = Diagram()
    diagram.load_from_json(example_config)
    print(diagram)

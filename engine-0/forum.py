class Control:
    __names = set()
    __obligatory = {
        "name", "capital", "staff",
        "technologies", "units"
    }

    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return self.name != other.name
    def __hash__(self):
        return hash(self.name)

    def __init__(self, config):
        for key in self.__obligatory:
            assert key in config, f"no {key} in node config"
        assert config["name"] not in self.__names, config["name"] 
        self.__names.add(config["name"])
        for k, v in config.items():
            setattr(self, k, v)
        print(self)

    def __str__(self):
        out = "[CONTROL]--------------------"
        out += f"\nname: {self.name}"
        out += f"\ncapital: {self.capital}"
        staff = sum(self.staff.values())
        out += f"\nstaff: {staff}"
        return out + "\n--------------------[CONTROL]"

class Forum(dict):
    constants = {
        "maximum-unit-size": 5000
    }

    technologies = [
        "production A", "production B", "production C",
        "mixing ABC", "mixing AB", "mixing BC", "mixing AC",
        "army unit-size", "army offensive", "army defence"
    ]

    def __init__(self):
        dict.__init__(self)

    def load_from_json(self, config):
        for c in config:
            control = Control(c)
            self[control.name] = control

example_config = [
    {
        "name": "Aaa",
        "capital": "A1",
        "glory": 0.0,
        "technologies":{
            "army unit-size": 0.12
        },
        "units": ["A1", ],
        "staff": {
            "A1": 120,
            "B2": 10,
            "D4": 5
        }},
    {
        "name": "Bbb",
        "capital": "B2",
        "glory": 0.0,
        "technologies":{
            "army unit-size": 0.1
        },
        "units": [],
        "staff": {
            "A1": 10,
            "B2": 100,
            "D4": 15
        }}
]

if __name__ == "__main__":
    forum = Forum()
    forum.load_from_json(example_config)
    print(forum)

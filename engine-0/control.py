class Control:
    __names = set()
    __obligatory = {
        "name", "capital"
    }
    __optional_dicts = {
        "technologies", "units", "agents"
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
        for key in self.__optional_dicts:
            if key not in config: setattr(self, key, {})            
        print(self)

    def __str__(self):
        out = "[CONTROL]--------------------"
        out += f"\nname: {self.name}"
        out += f"\ncapital: {self.capital}"
        return out + "\n--------------------[CONTROL]"

if __name__ == "__main__":
    aa = Control({
        "name": "Aaa",
        "capital": "A1"})
    bb = Control({
        "name": "Bbb",
        "capital": "B2"})

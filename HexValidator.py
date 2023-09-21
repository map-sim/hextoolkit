import math
from TerrWindow import TerrGraph

class TypeValidator:
    types = {}
    def validate_types(self, prefix, data):
        for key, val in data.items():
            assert key in self.types, key
            if type(self.types[key]) in (tuple, list):
                assert type(val) in self.types[key]
            else: assert type(val) is self.types[key], key
        print(f"{prefix} validate_types... OK")

class ConfigValidator(TypeValidator):
    types = {
        "window-title": str,
        "window-size": (tuple, list),
        "window-offset": (tuple, list),
        "window-zoom": (int, float),
        "move-sensitive": (int, float)
    }
    def __init__(self, config):
        self.validate_types("config", config)
        
class LibraryValidator(TypeValidator):
    types = {
        "settings": dict,
        "objects": dict,
        "terrains": dict,
        "resources": dict,
        "players": dict,
        "technologies": list
    }

    def __init__(self, library):
        self.library = library
        self.validate_types("library", library)
        assert self.library["players"], "no player"
        assert self.library["settings"], "no setting"
        assert self.library["terrains"], "no terrain"
        assert self.library["technologies"], "no technology"
        assert self.library["resources"], "no resource"
        assert self.library["objects"], "no object"

class MapValidator(TypeValidator):
    types = {
        "iteration": int,
        "difficulty": int,
        "terrains": list,
        "objects": dict,
        "players": dict,
        "links": dict
    }
    def __init__(self, library, battlefield):
        self.terr_graph = TerrGraph(battlefield)
        self.library = library

        self.validate_types("map", battlefield)
        self.validate_links(battlefield)

    def validate_links(self, battlefield):
        for (src, sink), good in battlefield["links"].items():
            ox, oy = self.terr_graph.transform_to_oxy(src)
            ex, ey = self.terr_graph.transform_to_oxy(sink)
            d = math.sqrt((ox-ex)**2 + (oy-ey)**2)
            obj = battlefield["objects"][src]
            libobj = self.library["objects"][obj["name"]]
            if "range" in libobj:
                r = libobj["range"]
                if good == "hit": r *= 2
                elif good == "dev": r *= 2
                assert d <= r, f"{src} -- {sink} >> {good}"
        print(f"map validate_links... OK")

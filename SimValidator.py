import math

class TypeValidator:
    types = {}
    def validate_types(self, prefix, data):
        for key, val in data.items():
            assert key in self.types, key
            if type(self.types[key]) in (tuple, list):
                assert type(val) in self.types[key]
            else: assert type(val) is self.types[key]
        print(f"{prefix} validate_types...")

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
        "objects": dict,
        "terrains": dict,
        "resources": dict,
        "players": dict
    }

    def __init__(self, library):
        self.library = library
        self.validate_types("library", library)

        assert self.library["terrains"], "no terrain"
        assert self.library["players"], "no player"

class MapValidator(TypeValidator):
    types = {
        "difficulty": int,
        "iteration": int,
        "terrains": list,
        "objects": list,
        "players": dict,
        "links": list
    }
    def __init__(self, library, battlefield):
        self.library = library
        self.validate_types("map", battlefield)
        self.validate_terrains(battlefield)
        self.validate_intervals(battlefield)
        
    def validate_intervals(self, battlefield):
        print("map validate_intervals...")
        for n, obj1 in enumerate(battlefield["objects"]):
            for k, obj2 in enumerate(battlefield["objects"]):
                if k == n: continue
                d2 = (obj1["xy"][0] - obj2["xy"][0]) ** 2
                d2 += (obj1["xy"][1] - obj2["xy"][1]) ** 2
                d = math.sqrt(d2)
                iv1 = self.library["objects"][obj1["obj"]]["interval"]
                iv2 = self.library["objects"][obj2["obj"]]["interval"]
                info = f"wrong dist: {obj1['xy']}/{obj1['obj']} -- {obj2['xy']}/{obj2['obj']}"
                assert d >= max([iv1, iv2]), info

    def validate_terrains(self, battlefield):
        for row in battlefield["terrains"]:
            assert row[1] in self.library["terrains"]
        print("map validate_terrains...")
        
class SimValidator:
    def validate_config(self, config):
        ConfigValidator(config)
    def validate_library(self, library):
        LibraryValidator(library)
    def validate_map(self, library, battlefield):
        MapValidator(library, battlefield)

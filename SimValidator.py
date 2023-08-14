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
        "players": dict
    }

    def __init__(self, library):
        self.library = library
        self.validate_types("library", library)

        assert self.library["terrains"], "no terrain"
        assert self.library["players"], "no player"
        
class MapValidator(TypeValidator):
    types = {
        "iteration": int,
        "radiation": (int, float),
        "objects": list,
        "terrains": list
    }
    def __init__(self, library, battlefield):
        self.library = library
        self.validate_types("map", battlefield)
        self.validate_terrains(battlefield)
        
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

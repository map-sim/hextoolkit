from TerrWindow import TerrGraph

class TypeValidator:
    types = {}
    def validate_types(self, config):
        for key, val in config.items():
            assert key in self.types, key
            if type(self.types[key]) in (tuple, list):
                assert type(val) in self.types[key]
            else: assert type(val) is self.types[key]
        print("validate_types...")

class ConfigValidator(TypeValidator):
    types = {
        "window-title": str,
        "window-size": (tuple, list),
        "window-offset": (tuple, list),
        "window-zoom": (int, float),
        "move-sensitive": (int, float),
        "max-selection-d2": (int, float)
    }

    def __init__(self, config):
        self.validate_types(config)

class LibraryValidator(TypeValidator):
    types = {
        "technologies": (list, tuple),
        "objects": dict,
        "resources": dict,
        "settings": dict,
        "terrains": dict,
        "players": dict
    }

    def __init__(self, library):
        self.validate_types(library)
        self.library = library

    def validate_distance2(self, name, d2, xy, xy2):
        assert name in self.library["objects"]
        r2 = self.library["objects"][name]["radius"] ** 2
        assert d2 >= r2, f"{name} ({xy}) -- {xy2}"

    def validate_buildable(self, terr):
        assert self.library["terrains"][terr]["buildable"], terr

class BattlefieldValidator(TypeValidator):
    types = {
        "iteration": int,
        "objects": list,
        "resources": dict,
        "terrains": list
    }
    
    def __init__(self, libval, battlefield):
        self.validate_types(battlefield)
        self.libval = libval

        objects = battlefield["objects"]
        resources = battlefield["resources"]
        self.validate_object_types(objects)
        self.validate_object_distribution(battlefield)
        self.validate_mineshafts(objects, resources)
        
    def validate_object_types(self, objects):
        for name, x, y, player, hp, *rest in objects:            
            assert type(player) is str
            assert type(name) is str
            assert type(hp) is float
            assert type(x) is int
            assert type(y) is int
        print("validate_object_types...")

    def validate_object_distribution(self, battlefield):
        graph_terr, tmp_list = TerrGraph(battlefield), []
        for name, x, y, *rest in battlefield["objects"]:
            for x2, y2 in tmp_list:
                d2 = (x2-x) **2 + (y2-y) **2
                self.libval.validate_distance2(name, d2, (x, y), (x2, y2))
            tmp_list.append((x, y))
            terr, _ = graph_terr.check_terrain(x, y)
            self.libval.validate_buildable(terr)
        print("validate_object_distribution...")

    def validate_mineshafts(self, objects, resources):
        for name, x, y, *rest in objects:            
            if name not in ("mineshaft", "drill"): continue
            assert (x, y) in resources, f"no resources defined in: {x}, {y}"
        print("validate_mineshafts...")

def validate(config, library, battlefield):
    libval = LibraryValidator(library)
    BattlefieldValidator(libval, battlefield)
    ConfigValidator(config)

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

        assert self.library["players"], "no player"
        assert self.library["terrains"], "no terrain"
        assert self.library["resources"], "no resource"
        self.validate_objects_ranges()
        
    def validate_objects_ranges(self):
        for obj in self.library["objects"]:
            if "range" in obj: assert obj["range"] > 0.0
            if "free-range" in obj: assert obj["free-range"] > 0.0
            if "free-range" in obj and "range" in obj:
                assert obj["free-range"] <= obj ["range"]
        print("validate_objects_ranges...")
        
    def validate_distance2(self, name, d2, xy, xy2):
        assert name in self.library["objects"]
        r2 = self.library["objects"][name]["radius"] ** 2
        assert d2 >= r2, f"{name} ({xy}) -- {xy2}"

    def validate_tech_exists(self, tech):
        assert tech in self.library["technologies"], tech

    def validate_buildable(self, terr):
        assert self.library["terrains"][terr]["buildable"], terr

class BattlefieldValidator(TypeValidator):
    types = {
        "iteration": int,
        "ratiation": (int, float),
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
        self.validate_object_params(objects)
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

    def validate_object_params(self, objects):
        for name, _, _, _, _, *rest in objects:            
            if name == "laboratory":
                tech = rest[0]
                if tech is None: continue
                self.libval.validate_tech_exists(tech)
            if name == "launcher":
                xy, found = rest[0], False                
                if xy is None: continue
                for _, x2, y2, _, _, *rest in objects:
                    if xy == (x2, y2): found = True
                assert found, f"{name}, --> {xy}"
            if name in ("radiator", "barrier", "observer",
                        "repeater", "developer", "transmitter"):
                switch = rest[0]
                assert switch in (False, True), f"{name}: switch: {switch}"
        print("validate_object_params...")

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
    if config is not None: ConfigValidator(config)
    libval = LibraryValidator(library)
    BattlefieldValidator(libval, battlefield)

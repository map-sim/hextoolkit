class TypeValidator:
    types = {}
    def validate_types(self, config):
        for key, val in config.items():
            assert key in self.types
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
        "move-sensitive": (int, float)
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

class BattlefieldValidator(TypeValidator):
    types = {
        "objects": list,
        "resorces": list,
        "terrains": list
    }

    def __init__(self, libval, battlefield):
        self.validate_types(battlefield)
        self.libval = libval

        objects = battlefield["objects"]
        self.validate_object_distribution(objects)
            
    def validate_object_distribution(self, objects):
        tmp_list = []
        for name, x, y, *rest in objects:            
            for x2, y2 in tmp_list:
                d2 = (x2-x) **2 + (y2-y) **2
                self.libval.validate_distance2(name, d2, (x, y), (x2, y2))
            tmp_list.append((x, y))
        print("validate_object_distribution...")

def validate(config, library, battlefield):
    libval = LibraryValidator(library)
    BattlefieldValidator(libval, battlefield)
    ConfigValidator(config)

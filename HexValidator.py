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
        self.validate_range_links(battlefield)
        self.validate_src_sink_links(battlefield)

    def validate_range_links(self, battlefield):
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
        print(f"map validate_range_links... OK")

    def validate_src_sink_links(self, battlefield):
        for (src, sink), good in battlefield["links"].items():
            obj_sink = battlefield["objects"][sink]
            obj_src = battlefield["objects"][src]
            if good == "hit" or good == "dev": pass
            elif obj_src["name"] == "mine" and obj_sink["name"] == "store": pass
            elif obj_src["name"] == "store" and obj_sink["name"] == "store": pass
            elif obj_src["name"] == "mixer" and obj_sink["name"] == "store": pass
            elif obj_src["name"] == "store" and obj_sink["name"] == "mixer": pass
            elif obj_src["name"] == "store" and obj_sink["name"] == "lab": pass
            elif obj_src["name"] == "store" and obj_sink["name"] == "send": pass
            elif obj_src["name"] == "store" and obj_sink["name"] == "devel": pass
            elif obj_src["name"] == "store" and obj_sink["name"] == "hit": pass
            else: raise ValueError("src-sink")
        print(f"map validate_src_sink_links... OK")

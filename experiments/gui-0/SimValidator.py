import math

class TypeValidator:
    types = {}
    def validate_types(self, prefix, data):
        for key, val in data.items():
            assert key in self.types, key
            if type(self.types[key]) in (tuple, list):
                assert type(val) in self.types[key]
            else: assert type(val) is self.types[key]
        print(f"{prefix} validate_types... OK")

class ConfigValidator(TypeValidator):
    types = {
        "window-title": str,
        "window-size": (tuple, list),
        "window-offset": (tuple, list),
        "window-zoom": (int, float),
        "selection-radius": (int, float),
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
        self.validate_links(battlefield)
        self.validate_works_in_progress(battlefield)
        self.validate_store_capacity(battlefield)

    def validate_store_capacity(self, battlefield):
        for obj in battlefield["objects"]:
            if obj["name"] != "store": continue            
            player = obj["own"]
            compress = "resource-compresion" in battlefield["players"][player]["technologies"]
            if compress: assert len(obj["goods"]) <= 6
            else: assert len(obj["goods"]) <= 4
        print("map validate_store_capacity... OK")

    def validate_works_in_progress(self, battlefield):
        for obj in battlefield["objects"]:
            if obj["cnt"] <= 0:
                if "work" in obj: assert not obj["work"], "obj works under construction"
                if "out" in obj: assert obj["work"] is None, "obj works under construction"
        print("map validate_works_in_progress... OK")
        
    def validate_intervals(self, battlefield):
        for n, obj1 in enumerate(battlefield["objects"]):
            for k, obj2 in enumerate(battlefield["objects"]):
                if k == n: continue
                d2 = (obj1["xy"][0] - obj2["xy"][0]) ** 2
                d2 += (obj1["xy"][1] - obj2["xy"][1]) ** 2
                d = math.sqrt(d2)
                iv1 = self.library["objects"][obj1["name"]]["interval"]
                iv2 = self.library["objects"][obj2["name"]]["interval"]
                info = f"wrong dist: {obj1['xy']}/{obj1['name']} -- {obj2['xy']}/{obj2['name']}"
                assert d >= max([iv1, iv2]), info
        print("map validate_intervals... OK")

    def validate_terrains(self, battlefield):
        for row in battlefield["terrains"]:
            if row[0] == "grid": continue
            assert row[1] in self.library["terrains"]
        print("map validate_terrains... OK")

    def validate_links(self, battlefield):
        counters = {}
        for g, xy1, xy2 in battlefield["links"]:
            assert xy1 != xy2, "link other to other"
            try: counters[g, xy1, xy2] += 1
            except KeyError: counters[g, xy1, xy2] = 1

            o_is, e_is = False, False
            for obj in battlefield["objects"]:
                if xy1 == obj["xy"]:  o_is = True
                if xy2 == obj["xy"]:  e_is = True
            assert o_is and e_is, f"broken link: {g}, {xy1}, {xy2}"
        for oe, c in counters.items():
            assert c == 1, f"{oe} counter = {c}"
        
        for g, xy1, xy2 in battlefield["links"]:
            d2 = (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2
            for obj in battlefield["objects"]:
                if xy1 == obj["xy"]: break
            for obj2 in battlefield["objects"]:
                if xy2 == obj2["xy"]: break
                
            objdef = self.library["objects"][obj["name"]]
            obj2def = self.library["objects"][obj2["name"]]
            r = objdef["range"] if objdef["range"] > 0 else obj2def["range"]
            if g in ["hit", "devel"]: r *= 2
            info = f"range {g}, {xy1}{obj['name']} -- {xy2}{obj2['name']} < {r}"
            assert math.sqrt(d2) <= r, info 
        print("map validate_links... OK")
            
class SimValidator:
    def validate_config(self, config):
        ConfigValidator(config)
    def validate_library(self, library):
        LibraryValidator(library)
    def validate_map(self, library, battlefield):
        MapValidator(library, battlefield)


import gi, os, copy, math, random
from pprint import pformat

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from HexValidator import ConfigValidator
from HexValidator import LibraryValidator
from HexValidator import MapValidator
from HexPainter import HexPainter
from TerrWindow import TerrWindow
from TerrWindow import TerrGraph

def status_print(msg):
    def wrapper(func):
        def inner(*args, **kwargs): 
            ret = func(*args, **kwargs)
            print(f"status of {msg}: {ret}")
            return ret
        return inner
    return wrapper

class HexRunner:
    def __init__(self, library, battlefield):
        self.graph_terr = TerrGraph(battlefield)
        self.battlefield = battlefield
        self.library = library
        self.links_from = {}
        self.links_to = {}
    
        for f, t in battlefield["links"].keys():
            try: self.links_to[t].append(f)
            except KeyError: self.links_to[t] = [f]
            try: self.links_from[f].append(t)
            except KeyError: self.links_from[f] = [t]

    def run(self):
        self.battlefield["iteration"] += 1
        self.run_mines()

    def get_available_capacity(self, obj):
        flag_rcompress = self.check_technology(obj, "resource-compresion")
        capacity = 6 if flag_rcompress else 4
        return capacity - len(obj["goods"])

    def run_mines(self):
        for vex, obj in self.battlefield["objects"].items():
            if obj["name"] != "mine": continue
            if obj["out"] is None: continue
            if vex not in self.links_from: continue
            
            terr = self.graph_terr.get_hex_terr(vex)
            resources = self.library["terrains"][terr]["resources"]
            base_chance = resources.get(obj["out"], 0.0)            
            chances = [base_chance] 
            if self.check_technology(obj, "advanced-mining"):
                chances += [0.5 * base_chance]
            no = self.rand_to_count(chances)

            destinations = []
            for vex2 in self.links_from[vex]:
                good = self.battlefield["links"][vex, vex2]
                if good != obj["out"]: continue
                obj2 = self.battlefield["objects"][vex2]
                if obj2["name"] != "store": continue
                if self.get_available_capacity(obj2):
                    destinations.append(obj2)
            if not destinations: continue
            # destix = list(range(len(destinations)))
            for _ in range(no):
                obj2i = random.randint(0, len(destinations)-1) #     random.shuffle(destix)
                obj2 = destinations[obj2i]
                obj2["goods"].append(obj["out"])
                if not self.get_available_capacity(obj2):
                    destinations.pop(obj2i)
                    if not destinations: break

    def rand_to_count(self, chances):
        count = 0
        for chance in chances:
            if random.uniform(0, 1) < chance:
                count += 1
        return count

    def check_technology(self, obj_or_own, tech):
        assert tech in self.library["technologies"], f"{tech} not tech"
        if isinstance(obj_or_own, str): own = obj_or_own
        else: own = obj_or_own["own"]
        pconf = self.battlefield["players"][own]
        return tech in pconf["technologies"]

class HexWindow(TerrWindow):
    def __init__(self, config, library, battlefield):
        TerrWindow.__init__(self, config, library, battlefield)
        self.validate(); self.show_all(); self.state = {}
        self.state["game-index"] = None
        self.state["selected-player"] = None
        self.state["selected-good"] = None
        self.state["selected-terr"] = None
        self.state["selected-obj"] = None
        self.state["saved-games"] = []
        self.control_panel = None

        self.graph_terr = TerrGraph(battlefield)
        self.painter = HexPainter(config, library, battlefield)
        self.config_backup = copy.deepcopy(config)
        self.draw_content()

    def on_click(self, widget, event):
        TerrWindow.on_click(self, widget, event)
        ox, oy = self.get_click_location(event)
        vex, xyo = self.graph_terr.transform_to_vex(ox, oy)
        terr = self.graph_terr.get_hex_terr(vex)
        if event.button == 1:
            self.painter.set_selection(vex, xyo)
            obj = self.battlefield["objects"].get(vex)
            good = self.painter.check_resource(obj, ox, oy)
            self.state["selected-good"] = good
            self.control_panel.refresh_good_label()
            self.control_panel.refresh_selection_label(terr, obj)
            self.draw_content()
        elif event.button == 3 and self.painter.selected_vex is not None:
            obj = self.battlefield["objects"].get(vex)
            if obj is None: return
            lkey = (self.painter.selected_vex, vex)
            if lkey not in self.battlefield["links"]:
                if self.state["selected-good"] is None: return
                self.set_link(*lkey, self.state["selected-good"])
            else: del self.battlefield["links"][lkey]
            self.draw_content()
        else:
            self.state["selected-terr"] = terr
            self.control_panel.refresh_terr_label()
            obj = self.battlefield["objects"].get(vex)
            if obj: self.state["selected-obj"] = obj["name"]
            self.control_panel.refresh_obj_label()
            if obj: self.state["selected-player"] = obj["own"]
            self.control_panel.refresh_player_label()    

    def set_link(self, ivex, ovex, good):
        if ivex == ovex: return
        ox, oy = self.graph_terr.transform_to_oxy(ivex)
        ex, ey = self.graph_terr.transform_to_oxy(ovex)
        dist = math.sqrt((ox-ex)**2 + (oy-ey)**2)
        obj = self.battlefield["objects"][ivex]
        libobj = self.library["objects"][obj["name"]]
        if "range" not in libobj : return
        obj_range = libobj["range"]
        if good == "hit": obj_range *= 2
        elif good == "dev": obj_range *= 2
        if dist > obj_range: return
        self.battlefield["links"][ivex, ovex] = good

    def set_terrain(self):
        if self.state["selected-terr"] is None: return
        if self.painter.selected_vex is None: return
        terr = self.state["selected-terr"]
        vex = self.painter.selected_vex
        self.graph_terr.vex_dict[vex] = terr
        self.painter.terr_graph.vex_dict[vex] = terr
        row = "vex", terr, vex, self.graph_terr.grid_radius
        self.battlefield["terrains"].insert(-1, row)
        print("Insert:", row)
        self.draw_content()

    def switch_terrain(self): self.switch_item("terrains", "selected-terr")
    def switch_player(self): self.switch_item("players", "selected-player")
    def switch_good(self): self.switch_item("resources", "selected-good")
    def switch_object(self): self.switch_item("objects", "selected-obj")        
    def switch_item(self, key, state):
        items = list(sorted(self.library[key].keys()))
        if key == "resources": items += ["dev", "hit"]
        if self.state[state] is not None:
            i =  items.index(self.state[state])
            i += 1; i %= len(items)
            self.state[state] = items[i]
        else: self.state[state] = items[0]
        print(f"{key}:", self.state[state])
        if key == "resources": self.control_panel.refresh_good_label()
        elif key == "players": self.control_panel.refresh_player_label()
        elif key == "terrains": self.control_panel.refresh_terr_label()
        elif key == "objects": self.control_panel.refresh_obj_label()
        else: raise KeyError(key)

    def change_player(self):
        vex = self.painter.selected_vex
        if self.state["selected-player"] is None: return
        if vex not in self.battlefield["objects"]: return
        obj = self.battlefield["objects"][vex]
        obj["own"] = self.state["selected-player"]
        self.draw_content()
    def change_armor(self):
        vex = self.painter.selected_vex
        if vex not in self.battlefield["objects"]: return
        obj = self.battlefield["objects"][vex]
        if obj["name"] == "nuke": return
        obj["armor"] = not obj.get("armor", False)
        self.draw_content()
    def change_hp(self):
        vex = self.painter.selected_vex
        if vex not in self.battlefield["objects"]: return
        obj = self.battlefield["objects"][vex]
        objlib = self.library["objects"][obj["name"]]
        length = objlib["modules"]; obj["cnt"] += 1
        if obj["cnt"] > length:
            obj["cnt"] = -length
        self.draw_content()

    def change_good(self, obj, advance):
        if obj["cnt"] <= 0: obj["out"] = None; return
        rnames, tab = sorted(self.library["resources"].keys()), []
        for rname in rnames:
            conf = self.library["resources"][rname]
            if not advance and "process" not in conf: tab.append(rname)
            elif advance and "process" in conf: tab.append(rname)
        if obj["out"] == tab[-1]:
            self.state["selected-good"] = obj["out"] = None
        elif obj["out"] is not None:
            i = (tab.index(obj["out"]) + 1) % len(tab)
            self.state["selected-good"] = obj["out"] = tab[i]
        else: self.state["selected-good"] = obj["out"] = tab[0]
        self.control_panel.refresh_good_label()
        
    def change_object(self):        
        if self.painter.selected_vex is None: return
        if self.painter.selected_vex not in self.battlefield["objects"]: return
        obj = self.battlefield["objects"][self.painter.selected_vex]
        if "work" in obj and obj["cnt"] > 0: obj["work"] = not obj["work"]        
        elif "work" in obj and obj["cnt"] <= 0: obj["work"] = False
        elif "out" in obj and obj["cnt"] <= 0: obj["out"] = None
        elif obj["name"] == "mixer": self.change_good(obj, advance=True)
        elif obj["name"] == "mine": self.change_good(obj, advance=False)
        self.draw_content()

    @status_print("new-object")
    def add_object(self):
        vex = self.painter.selected_vex
        if vex is None: return False
        default_terr = self.graph_terr.default_vex_terr
        terr = self.graph_terr.vex_dict.get(vex, default_terr)
        if not self.library["terrains"][terr]["buildable"]: return False
        if self.state["selected-player"] is None: return False
        if self.state["selected-obj"] is None: return False
        obj = self.battlefield["objects"].get(vex)
        if obj is not None: return False
        name = self.state["selected-obj"]
        interval = self.library["objects"][name]["interval"]
        xyo = self.graph_terr.transform_to_oxy(vex)
        for vex2, obj in self.battlefield["objects"].items():
            xy = self.graph_terr.transform_to_oxy(vex2)
            d = math.sqrt((xyo[0]-xy[0])**2 + (xyo[1]-xy[1])**2)
            r = self.library["objects"][obj["name"]]["interval"]
            print(r, interval, "??", d)
            if d < max([r, interval]): return False
        self.battlefield["objects"][vex] = {}
        owner = self.state["selected-player"]
        self.battlefield["objects"][vex]["name"] = name
        self.battlefield["objects"][vex]["own"] = owner
        cnt = self.library["objects"][name]["modules"]
        self.battlefield["objects"][vex]["cnt"] = cnt
        if name == "mine" or name == "mixer":
            self.battlefield["objects"][vex]["out"] = None
        elif name == "nuke" or name == "post": pass
        else: self.battlefield["objects"][vex]["work"] = False        
        if name != "nuke" and name != "post":
            self.battlefield["objects"][vex]["armor"] = False
        elif name == "post":
            self.battlefield["objects"][vex]["armor"] = True
        if name == "store":
            self.battlefield["objects"][vex]["goods"] = []
        self.draw_content()
        return True

    def del_object(self):
        vex = self.painter.selected_vex
        if vex is None: return
        for i, o in list(self.battlefield["links"].keys()):
            if vex in (i, o): del self.battlefield["links"][i, o]
        del self.battlefield["objects"][vex]
        self.draw_content()

    def on_press(self, widget, event):
        if isinstance(event, str): key_name = event
        else: key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Return":
            print("##> Run")
            HexRunner(self.library, self.battlefield).run()
            self.control_panel.refresh_run_label()
            self.draw_content()
            
        elif key_name == "Escape":
            print("##> Esc / reset")
            self.config["window-offset"] = self.config_backup["window-offset"]
            self.config["window-zoom"] = self.config_backup["window-zoom"]
            self.painter.set_selection(None, None)
            self.state["selected-player"] = None
            self.state["selected-good"] = None
            self.state["selected-terr"] = None
            self.state["selected-obj"] = None
            self.control_panel.refresh_all_labels()
            self.draw_content()
        elif key_name == "grave": 
            self.painter.set_selection(None, None)
            self.control_panel.refresh_selection_label()
            self.draw_content()
        elif key_name == "T": self.set_terrain()
        elif key_name == "t": self.switch_terrain()
        elif key_name == "o": self.switch_object()
        elif key_name == "g": self.switch_good()
        elif key_name == "p": self.switch_player()
        elif key_name == "n": self.add_object()
        elif key_name == "d": self.del_object()
        elif key_name == "y": self.change_object()
        elif key_name == "x": self.change_player()
        elif key_name == "a": self.change_armor()
        elif key_name == "m": self.change_hp()
        elif key_name == "s": self.save_lib_and_map()
        elif key_name == "l": self.load_lib_and_map()
        elif key_name == "v": self.validate()
        elif key_name == "f":
            self.painter.switch_network()
            self.draw_content()
        elif key_name in ("comma", "less"):
            length = len(self.state["saved-games"])
            if self.state["game-index"] is None:
                if length > 0: self.state["game-index"] = -1
            else: self.state["game-index"] -= 1
            if self.state["game-index"] is not None:
                self.state["game-index"] %= length
                print("Snapshot:", self.state["game-index"])
                self.control_panel.refresh_snapshot_label()
        elif key_name in ("period", "greater"):
            length = len(self.state["saved-games"])
            if self.state["game-index"] is None:
                if length > 0: self.state["game-index"] = 0
            else: self.state["game-index"] += 1
            if self.state["game-index"] is not None:
                self.state["game-index"] %= length
                print("Snapshot:", self.state["game-index"])
                self.control_panel.refresh_snapshot_label()
        else: TerrWindow.on_press(self, widget, event)

    def load_lib_and_map(self):
        if self.state["game-index"] is None: return
        if not self.state["saved-games"]: return
        i = self.state["game-index"]
        print("Try to load snapshot:", i)
        self.battlefield, self.library = self.state["saved-games"][i]
        self.painter = HexPainter(self.config, self.library, self.battlefield)
        self.graph_terr = TerrGraph(self.battlefield)
        self.draw_content()

    def save_lib_and_map(self):
        cnt, libname, mapname = 0, "lib", "map"
        flib = lambda c: f"{libname}-{c}.txt"
        fmap = lambda c: f"{mapname}-{c}.txt"
        while os.path.exists(flib(cnt)): cnt += 1
        while os.path.exists(fmap(cnt)): cnt += 1
        with open(flib(cnt), "w") as fd:
            fd.write(pformat(self.library))
        print("Save library:", flib(cnt))
        with open(fmap(cnt), "w") as fd:
            fd.write(pformat(self.battlefield))
        print("Save battlefield:", fmap(cnt))
        library =  copy.deepcopy(self.library)
        battlefield = copy.deepcopy(self.battlefield)
        self.state["saved-games"].append((battlefield, library))
        self.state["game-index"] = len(self.state["saved-games"]) - 1
        self.control_panel.refresh_snapshot_label()

    def validate(self):        
        ConfigValidator(self.config)
        LibraryValidator(self.library)
        MapValidator(self.library, self.battlefield)
        
def run_example():
    import ast, sys
    from HexControl import HexControl
    from HexSamples import library_0
    from HexSamples import battlefield_0
    # from HexSamples import battlefield_1
    example_config = {
        "window-title": "MainMap",
        "window-size": (1800, 780),
        "window-offset": (840, 125),
        "window-zoom": 15.0,
        "move-sensitive": 50
    }

    if len(sys.argv) >= 2:
        print("try to load map", sys.argv[1])
        with open(sys.argv[1], "r", encoding="utf-8") as fd:
            battlefield_0 = ast.literal_eval(fd.read())
    if len(sys.argv) >= 3:
        print("try to load lib", sys.argv[2])
        with open(sys.argv[2], "r", encoding="utf-8") as fd:
            library_0 = ast.literal_eval(fd.read())
    win = HexWindow(example_config, library_0, battlefield_0)
    win.control_panel = HexControl(win)
    
    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

# broadwayd :5
# http://127.0.0.1:8085/
# GDK_BACKEND=broadway BROADWAY_DISPLAY=:5 python3 ...
if __name__ == "__main__": run_example()

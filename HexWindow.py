
import gi, os, copy, math
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
        terr = self.graph_terr.get_hex_terr((vex, xyo))
        if event.button == 1:
            self.painter.set_selection(vex, xyo)
            default_terr = self.graph_terr.default_vex_terr
            terr = self.graph_terr.vex_dict.get(vex, default_terr)
            obj = self.battlefield["objects"].get(vex)
            self.control_panel.refresh_selection_label(terr, obj)
            good = self.painter.check_resource(obj, ox, oy)
            self.state["selected-good"] = good            
            self.control_panel.refresh_good_label()
            if obj: self.state["selected-obj"] = obj["name"]
            self.control_panel.refresh_obj_label()
            if obj: self.state["selected-player"] = obj["own"]
            self.control_panel.refresh_player_label()
            self.state["selected-terr"] = terr
            self.control_panel.refresh_terr_label()
            self.draw_content()

    def set_terrain(self):
        if self.state["selected-terr"] is None: return
        if self.painter.selected_vex is None: return
        terr = self.state["selected-terr"]
        vex = self.painter.selected_vex
        self.graph_terr.vex_dict[vex] = terr
        row = "vex", terr, vex, self.graph_terr.grid_radius
        self.battlefield["terrains"].insert(-2, row)
        print("Insert:", row)
        self.draw_content()

    def switch_terrain(self): self.switch_item("terrains", "selected-terr")
    def switch_player(self): self.switch_item("players", "selected-player")
    def switch_object(self): self.switch_item("objects", "selected-obj")        
    def switch_good(self): self.switch_item("resources", "selected-good")

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
        print(obj)
        obj["own"] = self.state["selected-player"]
        print(obj)
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

    def on_press(self, widget, event):
        if isinstance(event, str): key_name = event
        else: key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Escape":
            print("##> mode: navi & zoom reset")
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
        elif key_name == "n": self.add_object()
        elif key_name == "p": self.switch_player()
        elif key_name == "x": self.change_player()
        elif key_name == "s": self.save_lib_and_map()
        elif key_name == "l": self.load_lib_and_map()
        elif key_name == "v": self.validate()
        
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

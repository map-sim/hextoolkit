
import gi, os, copy
from pprint import pformat

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from HexPainter import HexPainter
from TerrWindow import TerrWindow
from TerrWindow import TerrGraph


class HexWindow(TerrWindow):
    def __init__(self, config, library, battlefield):
        TerrWindow.__init__(self, config, library, battlefield)
        self.show_all(); self.state = {}
        self.state["game-index"] = None
        self.state["saved-games"] = []
        self.state["selected-terr"] = None
        self.control_panel = None

        self.graph_terr = TerrGraph(battlefield)
        self.painter = HexPainter(config, library, battlefield)
        self.config_backup = copy.deepcopy(config)
        self.draw_content()

    def on_click(self, widget, event):
        TerrWindow.on_click(self, widget, event)
        ox, oy = self.get_click_location(event)
        vex, xyo = self.graph_terr.transform_to_vex(ox, oy)
        if event.button == 1:
            self.painter.set_selection(vex, xyo)
            self.control_panel.refresh_vex_label()
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

    def switch_terrain(self):
        terrs = list(sorted(self.library["terrains"].keys()))
        if self.state["selected-terr"] is not None:
            i =  terrs.index(self.state["selected-terr"])
            i += 1; i %= len(terrs)
            self.state["selected-terr"] = terrs[i]
        else: self.state["selected-terr"] = terrs[0]
        print("Terrain:", self.state["selected-terr"])
        
    def on_press(self, widget, event):
        if isinstance(event, str): key_name = event
        else: key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Escape":
            print("##> mode: navi & zoom reset")
            self.config["window-offset"] = self.config_backup["window-offset"]
            self.config["window-zoom"] = self.config_backup["window-zoom"]
            self.painter.set_selection(None, None)
            self.control_panel.refresh_vex_label()
            self.draw_content()
        elif key_name == "T": self.set_terrain()
        elif key_name == "t": self.switch_terrain()
        elif key_name == "s": self.save_lib_and_map()
        elif key_name == "l": self.load_lib_and_map()
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

def run_example():
    import ast, sys
    from HexControl import HexControl
    from HexSamples import library_0
    from HexSamples import battlefield_0
    example_config = {
        "window-title": "MainMap",
        "window-size": (1800, 820),
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

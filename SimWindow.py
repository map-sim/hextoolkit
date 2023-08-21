from SimValidator import SimValidator
from SimPainter import SimPainter
from TerrWindow import TerrWindow

import gi, os, copy, math
from pprint import pformat

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class SimGraph:
    max_d2 = 64
    def __init__(self, library, battlefield):
        self.battlefield =  battlefield
        self.library = library
        
    def find_next_object(self, x, y):
        index, min_d2 = None, math.inf
        for i, obj in enumerate(self.battlefield["objects"]):
            d2 = (obj["xy"][0] - x) ** 2 + (obj["xy"][1] - y) ** 2
            if d2 > self.max_d2: continue
            if d2 < min_d2: min_d2, index = d2, i
        return index

class SimWindow(TerrWindow):
    def __init__(self, config, library, battlefield):
        provider = Gtk.CssProvider()
        provider.load_from_data(b""".main-label {
        background-color: rgba(255, 255, 255, .75);
        padding: 10px 10px;}""")

        self.mode_label = Gtk.Label()
        style = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        self.mode_label.get_style_context().add_provider(provider, style)
        self.mode_label.get_style_context().add_class("main-label")
        
        self.mode = "navi"
        self.set_mode_label("navi")
        self.show_info = False

        TerrWindow.__init__(self, config, library, battlefield)
        self.graphs = {"sim": SimGraph(library, battlefield), "terr": self.graph}
        self.fix.put(self.mode_label, 0, 0)
        self.show_all()

        self.painter = SimPainter(config, library, battlefield)
        self.config_backup = copy.deepcopy(config)
        self.draw_content()

    def set_mode_label(self, text):
        large_font_span = "<span size='25000'>"
        text = large_font_span + f"{text}</span>"
        self.mode_label.set_markup(text)

    def update_info(self):
        content = "<span size='25000'>admin: info</span><span size='15000'>"
        for key, val in self.config.items():
            content += f"\nconfig {key} --> {val}"
            print(f"config {key}", "-->", val)
        print("window width", "-->", self.width)
        content += f"\nwindow width --> {self.width}"
        print("window height", "-->", self.height)
        content += f"\nwindow height --> {self.height}"
        self.set_mode_label(content + "</span>")

    def on_scroll(self, widget, event):
        TerrWindow.on_scroll(self, widget, event)
        if self.show_info: self.update_info()
        
    def on_click(self, widget, event):
        TerrWindow.on_click(self, widget, event)
        if self.mode == "navi":
            ox, oy = self.get_click_location(event)
            index = self.graphs["sim"].find_next_object(ox, oy)
            self.painter.set_selected_object(index)
            self.draw_content()

            terr, tmplist = self.graphs["terr"].check_terrain(ox, oy), []
            content = "<span size='25000'>navi: click</span><span size='15000'>"
            content += f"\n----------------\nterrain-type: {terr[0]}"
            content += f"\nterrain-shape: {terr[1][0]}"
            if terr[1][2]: content += f"\nterrain-points: {terr[1][2]}"
            if index is not None:
                obj = self.battlefield["objects"][index]
                content += f"\n----------------\n{obj['obj']}{obj['xy']}"
                content += f" -- Player: {obj['own']}\n"
                for k, v in obj.items():
                    if k in ("obj", "xy", "own"): continue
                    if k == "armor": tmplist += [f"{k}: {'yes' if v else 'no'}"]
                    elif k == "work": tmplist += [f"{k}: {'yes' if v else 'no'}"]
                    elif k == "goods": tmplist += [f"{k}: {', '.join(v)}"]
                    else: tmplist += [f"{k}: {v}"]
            content += " | ".join(tmplist)
            self.set_mode_label(content + "</span>")

    def on_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Escape":
            print("##> mode: navi & zoom reset")
            self.config["window-offset"] = self.config_backup["window-offset"]
            self.config["window-zoom"] = self.config_backup["window-zoom"]
            self.set_mode_label("navi")
            self.mode = "navi"
            self.show_info = False
            self.draw_content()
        elif key_name == "F1":
            print("##> mode: navi")
            self.show_info = False
            self.set_mode_label("navi")
            self.mode = "navi"
            self.draw_content()
        elif key_name == "F2":
            print("##> pointer mode: admin")
            self.set_mode_label("admin")
            self.mode = "admin"
            self.show_info = False
            self.draw_content()
        elif key_name == "i" and self.mode == "admin":
            self.show_info = not self.show_info
            if not self.show_info: self.set_mode_label("admin")
        elif key_name == "c" and self.mode == "admin":
            self.set_mode_label("admin: check")
            validator = SimValidator()
            validator.validate_config(self.config)
            validator.validate_library(self.library)
            validator.validate_map(self.library, self.battlefield)
            self.show_info = False
        elif key_name == "y" and self.mode in ("admin", "navi"):
            if self.painter.selected_index is not None:
                obj = self.battlefield["objects"][self.painter.selected_index]
                if "work" in obj: obj["work"] = True
                if obj["obj"] == "mine":
                    raws = [k for k, v in self.library["resources"].items() if "process" not in v]
                    if obj["out"] is not None:
                        i = (raws.index(obj["out"]) + 1) % len(raws)
                        obj["out"] = raws[i]
                    else: obj["out"] = raws[0]
                if obj["obj"] == "mixer":
                    cmpl = [k for k, v in self.library["resources"].items() if "process" in v]
                    if obj["out"] is not None:
                        i = (cmpl.index(obj["out"]) + 1) % len(cmpl)
                        obj["out"] = cmpl[i]
                    else: obj["out"] = cmpl[0]
                self.draw_content()
        elif key_name == "n" and self.mode in ("admin", "navi"):
            if self.painter.selected_index is not None:
                obj = self.battlefield["objects"][self.painter.selected_index]
                if "targets" in obj: obj["targets"] = []
                if "target" in obj: obj["target"] = None
                if "work" in obj: obj["work"] = False
                if "out" in obj: obj["out"] = None
                self.draw_content()
        elif key_name == "s" and self.mode == "admin":
            self.set_mode_label("admin: save")
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
            self.show_info = False
        else: TerrWindow.on_press(self, widget, event)
        if self.show_info: self.update_info()

def run_example():
    example_config = {
        "window-title": "mode-window",
        "window-size": (1800, 820),
        "window-offset": (840, 125),
        "window-zoom": 15.0,
        "move-sensitive": 50
    }
    
    import ast, sys
    from SimExamples import library0
    from SimExamples import battlefield0

    if len(sys.argv) >= 2:
        print("try to load map", sys.argv[1])
        with open(sys.argv[1], "r", encoding="utf-8") as fd:
            battlefield0 = ast.literal_eval(fd.read())
    if len(sys.argv) >= 3:
        print("try to load lib", sys.argv[2])
        with open(sys.argv[2], "r", encoding="utf-8") as fd:
            library0 = ast.literal_eval(fd.read())
    
    validator = SimValidator()
    validator.validate_library(library0)
    validator.validate_config(example_config)
    validator.validate_map(library0, battlefield0)
    SimWindow(example_config, library0, battlefield0)

    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

# broadwayd :5
# GDK_BACKEND=broadway BROADWAY_DISPLAY=:5 python3 ...
# http://127.0.0.1:8085/
if __name__ == "__main__": run_example()

from TerrWindow import TerrPainter
from TerrWindow import TerrWindow

import gi, os, copy
from pprint import pformat

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class ModePainter(TerrPainter):
    def __init__(self, config, library, battlefield):
        self.terr_painter = TerrPainter(config, library, battlefield)
        self.battlefield =  battlefield
        self.library = library
        self.config = config
        
    def draw(self, context):
        self.terr_painter.draw(context)

class ModeWindow(TerrWindow):

    def __init__(self, config, library, battlefield):
        self.mode_label = Gtk.Label()
        self.set_mode_label("navi")
        self.mode = "navi"

        TerrWindow.__init__(self, config, library, battlefield)
        self.fix.put(self.mode_label, 0, 0)
        self.show_all()

        self.painter = ModePainter(config, library, battlefield)
        self.config_backup = copy.deepcopy(config)

    def set_mode_label(self, text):
        large_font_span = "<span size='35000'>"
        text = large_font_span + f"{text}</span>"
        self.mode_label.set_markup(text)

    def on_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)

        if key_name == "Escape":
            print("##> mode: navi & zoom reset")
            self.config["window-offset"] = self.config_backup["window-offset"]
            self.config["window-zoom"] = self.config_backup["window-zoom"]
            self.set_mode_label("navi")
            self.mode = "navi"
            self.draw_content()
        elif key_name == "F1":
            print("##> pointer mode: admin")
            self.set_mode_label("admin")
            self.mode = "admin"
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
        else: return TerrWindow.on_press(self, widget, event)

def run_example():
    example_config = {
        "window-title": "mode-window",
        "window-size": (1800, 820),
        "window-offset": (750, 400),
        "window-zoom": 0.366,
        "move-sensitive": 50
    }
    
    import ast, sys
    from MapExamples import library1
    from MapExamples import battlefield1

    if len(sys.argv) >= 2:
        print("try to load map", sys.argv[1])
        with open(sys.argv[1], "r", encoding="utf-8") as fd:
            battlefield1 = ast.literal_eval(fd.read())
    if len(sys.argv) >= 3:
        print("try to load lib", sys.argv[2])
        with open(sys.argv[2], "r", encoding="utf-8") as fd:
            library1 = ast.literal_eval(fd.read())
    
    ModeWindow(example_config, library1, battlefield1)

    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()

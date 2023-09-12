
import gi, os, copy#, math
from pprint import pformat

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from TerrWindow import TerrWindow
from TerrWindow import TerrPainter

class HexPainter(TerrPainter):
    def __init__(self, config, library, battlefield):
        self.terr_painter = TerrPainter(config, library, battlefield)
    def draw(self, context):
        self.terr_painter.draw(context)

class HexWindow(TerrWindow):
    def __init__(self, config, library, battlefield):
        TerrWindow.__init__(self, config, library, battlefield)
        self.show_all()

        self.painter = HexPainter(config, library, battlefield)
        self.config_backup = copy.deepcopy(config)
        self.draw_content()

    def on_press(self, widget, event):
        if isinstance(event, str): key_name = event
        else: key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Escape":
            print("##> mode: navi & zoom reset")
            self.config["window-offset"] = self.config_backup["window-offset"]
            self.config["window-zoom"] = self.config_backup["window-zoom"]
            self.draw_content()
        elif key_name == "s":
            self.save_lib_and_map()
        else: TerrWindow.on_press(self, widget, event)

    def save_lib_and_map(self):
        # self.set_mode_label("navi: save")
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

class HexControlWindow(Gtk.Window):
    def __init__(self, main_window):
        Gtk.Window.__init__(self, title="Control")
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.main_window = main_window
        
        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button_esc = Gtk.Button.new_with_mnemonic("_ESC")
        button_esc.connect("clicked", self.on_click_esc)
        hbox.pack_start(button_esc, True, True, 0)
        
        self.show_all()

    def on_click_esc(self, button):
        self.main_window.on_press(None, "Escape")

def run_example():
    example_config = {
        "window-title": "MainMap",
        "window-size": (1800, 820),
        "window-offset": (840, 125),
        "window-zoom": 15.0,
        "move-sensitive": 50
    }

    import ast, sys
    from HexSamples import library_0
    from HexSamples import battlefield_0

    if len(sys.argv) >= 2:
        print("try to load map", sys.argv[1])
        with open(sys.argv[1], "r", encoding="utf-8") as fd:
            battlefield_0 = ast.literal_eval(fd.read())
    if len(sys.argv) >= 3:
        print("try to load lib", sys.argv[2])
        with open(sys.argv[2], "r", encoding="utf-8") as fd:
            library_0 = ast.literal_eval(fd.read())

    win = HexWindow(example_config, library_0, battlefield_0)
    HexControlWindow(win)
    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

# broadwayd :5
# GDK_BACKEND=broadway BROADWAY_DISPLAY=:5 python3 ...
# http://127.0.0.1:8085/
if __name__ == "__main__": run_example()

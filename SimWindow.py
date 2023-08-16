from SimValidator import SimValidator
from TerrWindow import TerrPainter
from TerrWindow import TerrWindow

import gi, os, copy
from pprint import pformat

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

import math
TWO_PI = 2 * math.pi
        
class SimPainter(TerrPainter):
    def __init__(self, config, library, battlefield):
        self.terr_painter = TerrPainter(config, library, battlefield)
        self.battlefield =  battlefield
        self.library = library
        self.config = config

    def draw_polygon(self, context, color, points):
        context.set_source_rgba(*color)
        start_x, start_y = points[-1]
        context.move_to (start_x, start_y)
        for point in points:    
            stop_x, stop_y = point
            context.line_to (stop_x, stop_y)
        context.fill()
        context.stroke()

    def calc_render_params(self, xloc, yloc):
        xoffset, yoffset = self.config["window-offset"]
        zoom = self.config["window-zoom"]
        xloc, yloc = xloc * zoom, yloc * zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        return xloc, yloc

    def draw_mixer_0(self, context, xyloc, color, modules, params):
        xloc, yloc = self.calc_render_params(*xyloc)
        r = 24 * self.config["window-zoom"]
        
        ob_color = 0, 0, 0, 1

        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        context.set_source_rgba(*color)
        context.arc(xloc, yloc, 3*r/4, 0, TWO_PI)
        context.fill()

        w = 4 * self.config["window-zoom"]
        context.set_line_width(w)
        
        rr = 2*r/3
        context.set_source_rgba(*ob_color)
        xi0, yi0 = xloc - rr, yloc - rr 
        xe0, ye0 = xloc + rr, yloc + rr
        context.move_to(xi0, yi0)
        context.line_to(xe0, ye0) 
        context.stroke()
        xi0, yi0 = xloc - rr, yloc + rr 
        xe0, ye0 = xloc + rr, yloc - rr
        context.move_to(xi0, yi0)
        context.line_to(xe0, ye0) 
        context.stroke()

        #xc = xloc + 16 * self.config["window-zoom"]
        #yc = yloc + 16 * self.config["window-zoom"]
        # self.draw_control(context, xc, yc, ob_color, resource)

        r = 8 * self.config["window-zoom"]
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        if params[0] is None: color2 = (0.0, 0.0, 0.0)
        else: color2 = self.library["resources"][params[0]]["color"]
            
        r = 5 * self.config["window-zoom"]
        context.set_source_rgba(*color2)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        
    def draw_store_0(self, context, xyloc, color, modules, params):
        xloc, yloc = self.calc_render_params(*xyloc)
        r = 20 * self.config["window-zoom"]
        rr = 14 * self.config["window-zoom"]

        w = 4 * self.config["window-zoom"]
        context.set_line_width(w)

        ob_color = 0, 0, 0, 1
        context.set_source_rgba(*ob_color)
        points = [(xloc-r, yloc-r), (xloc-r, yloc+r),
                  (xloc+r, yloc+r), (xloc+r, yloc-r)]
        self.draw_polygon(context, ob_color, points)
        points = [(xloc-rr, yloc-rr), (xloc-rr, yloc+rr),
                  (xloc+rr, yloc+rr), (xloc+rr, yloc-rr)]
        self.draw_polygon(context, color, points)

        context.set_source_rgba(*ob_color)
        xi0, yi0 = xloc - r, yloc 
        xe0, ye0 = xloc + r, yloc
        context.move_to(xi0, yi0)
        context.line_to(xe0, ye0) 
        context.stroke()

        xi1, yi1 = xloc, yloc - r
        xe1, ye1 = xloc, yloc + r
        context.move_to(xi1, yi1)
        context.line_to(xe1, ye1) 
        context.stroke()

        #xc = xloc + 16 * self.config["window-zoom"]
        #yc = yloc + 16 * self.config["window-zoom"]
        # self.draw_control(context, xc, yc, ob_color, resource)

    def draw(self, context):
        self.terr_painter.draw(context)
        for  xyloc, obj, player, modules, *params in self.battlefield["objects"]:
            shape = self.library["objects"][obj]["shape"]
            color = self.library["players"][player]["color"]

            if shape == "store-0": self.draw_store_0(context, xyloc, color, modules, *params)
            elif shape == "mixer-0": self.draw_mixer_0(context, xyloc, color, modules, *params)
            else: raise ValueError(f"Not supported object: {obj}")

class SimWindow(TerrWindow):

    def __init__(self, config, library, battlefield):
        self.mode_label = Gtk.Label()
        self.set_mode_label("navi")
        self.mode = "navi"

        TerrWindow.__init__(self, config, library, battlefield)
        self.fix.put(self.mode_label, 0, 0)
        self.show_all()

        self.painter = SimPainter(config, library, battlefield)
        self.config_backup = copy.deepcopy(config)
        self.draw_content()

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

        elif key_name == "i" and self.mode == "admin":
            for key, val in self.config.items():
                print(f"config {key}", "-->", val)
            print("window width", "-->", self.width)
            print("window height", "-->", self.height)
        elif key_name == "c" and self.mode == "admin":
            self.set_mode_label("admin: check")
            validator = SimValidator()
            validator.validate_config(self.config)
            validator.validate_library(self.library)
            validator.validate_map(self.library, self.battlefield)
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
if __name__ == "__main__": run_example()

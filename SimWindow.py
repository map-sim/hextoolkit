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

class SimObject:
    black_color = 0, 0, 0, 1

    def __init__(self, config, library, context, xyloc, player, modules):
        self.config, self.library = config, library
        self.color = self.library["players"][player]["color"]
        self.xy = self.__calc_render_xy(*xyloc)
        self.context = context
        self.modules = modules
        self.xyloc = xyloc

    def __calc_render_xy(self, xloc, yloc):
        zoom = self.config["window-zoom"]
        xloc, yloc = xloc * zoom, yloc * zoom
        xoffset, yoffset = self.config["window-offset"]
        return xloc + xoffset, yloc + yoffset

    def _draw_line(self, xy0, xy1, color, width=None):
        if width is not None: self.context.set_line_width(width)
        self.context.set_source_rgba(*color)
        xy0  = self.xy[0] + xy0[0], self.xy[1] + xy0[1]
        xy1  = self.xy[0] + xy1[0], self.xy[1] + xy1[1]
        self.context.move_to(*xy0)
        self.context.line_to(*xy1) 
        self.context.stroke()
    
    def _draw_polygon(self, points, color, width=None):
        if width is not None: self.context.set_line_width(width)
        self.context.set_source_rgba(*color)
        start_x, start_y = points[-1]
        self.context.move_to (self.xy[0] + start_x, self.xy[1] + start_y)
        for point in points:    
            stop_x, stop_y = point
            self.context.line_to (self.xy[0] + stop_x, self.xy[1] + stop_y)
        self.context.fill()
        self.context.stroke()

    def _draw_resource(self, xy, resource):
        xy = self.xy[0] + xy[0], self.xy[1] + xy[1]
        r = 0.34 * self.config["window-zoom"]
        self.context.set_source_rgba(*self.black_color)
        self.context.arc(*xy, r, 0, TWO_PI)
        self.context.fill()

        if resource is None: color2 = self.black_color
        else: color2 = self.library["resources"][resource]["color"]
        self.context.set_source_rgba(*color2)
        rr = 0.18 * self.config["window-zoom"]
        self.context.arc(*xy, rr, 0, TWO_PI)
        self.context.fill()

class SimMixer_0(SimObject):
    def __init__(self, config, library, context, xyloc, player, modules, resource):
        SimObject.__init__(self, config, library, context, xyloc, player, modules)
        self.resource = resource

    def draw(self):
        r = 1 * self.config["window-zoom"]
        self.context.set_source_rgba(*self.black_color)
        self.context.arc(*self.xy, r, 0, TWO_PI)
        self.context.fill()
        self.context.set_source_rgba(*self.color)
        self.context.arc(*self.xy, 3*r/4, 0, TWO_PI)
        self.context.fill()

        w = 0.15 * self.config["window-zoom"]
        self.context.set_line_width(w)
        
        rr = r * 2/3 
        self.context.set_source_rgba(*self.black_color)
        xi0, yi0 = self.xy[0] - rr, self.xy[1] - rr 
        xe0, ye0 = self.xy[0] + rr, self.xy[1] + rr
        self.context.move_to(xi0, yi0)
        self.context.line_to(xe0, ye0) 
        self.context.stroke()
        xi1, yi1 = self.xy[0] - rr, self.xy[1] + rr 
        xe1, ye1 = self.xy[0] + rr, self.xy[1] - rr
        self.context.move_to(xi1, yi1)
        self.context.line_to(xe1, ye1) 
        self.context.stroke()

        self._draw_resource((0, 0), self.resource)

class SimStore_0(SimObject):
    cells = [(-0.43, -0.84), (0.43, -0.84), (-0.43, 0),
             (0.43, 0), (-0.43, 0.84), (0.43, 0.84)]    
    def __init__(self, config, library, context, xyloc, player, modules, resources):
        SimObject.__init__(self, config, library, context, xyloc, player, modules)
        self.resources = resources

    def draw(self):
        r = 0.82 * self.config["window-zoom"]
        rr = 0.66 * self.config["window-zoom"]
        w = 0.1 * self.config["window-zoom"]
     
        self.context.set_line_width(w)
        self.context.set_source_rgba(*self.black_color)
        pts0 = [(-r, -1.5*r), (-r, +1.5*r), (+r, +1.5*r), (+r, -1.5*r)]
        pts1 = [(-rr, -1.5*rr), (-rr, +1.5*rr), (+rr, +1.5*rr), (+rr, -1.5*rr)]
        self._draw_polygon(pts0, self.black_color)
        self._draw_polygon(pts1, self.color)

        self._draw_line((-r, -0.42*r), (+r, -0.42*r), self.black_color)
        self._draw_line((-r, +0.42*r), (+r, +0.42*r), self.black_color)
        self._draw_line((0, -1.45*r), (0, +1.45*r), self.black_color)
        for i, resource in enumerate(self.resources):
            xyloc = r * self.cells[i][0], r * self.cells[i][1]
            self._draw_resource(xyloc, resource)

class SimPainter(TerrPainter):
    def __init__(self, config, library, battlefield):
        self.terr_painter = TerrPainter(config, library, battlefield)
        self.battlefield =  battlefield
        self.library = library
        self.config = config
        
    def draw(self, context):
        self.terr_painter.draw(context)
        for  xyloc, obj, player, modules, *params in self.battlefield["objects"]:
            shape = self.library["objects"][obj]["shape"]

            if shape == "mixer-0": SimMixer_0(self.config, self.library, context, xyloc, player, modules, params[0]).draw()
            elif shape == "store-0": SimStore_0(self.config, self.library, context, xyloc, player, modules, params[0]).draw()
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

        elif key_name == "i" and self.mode == "navi":
            print(self.config)
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
        "window-offset": (840, 125),
        "window-zoom": 36.0,
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

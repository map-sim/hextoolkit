#!/usr/bin/python3

import gi, math
from BaseWindow import BaseWindow
from TerrWindow import TerrWindow
from TerrWindow import TerrPainter
from TerrWindow import TerrGraph

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

TWO_PI = 2 * math.pi

class ObjectPainter(TerrPainter):
    def __init__(self, config, library, battlefield):
        self.terr_painter = TerrPainter(config, library, battlefield)
        self.battlefield =  battlefield
        self.library = library
        self.config = config

    def calc_render_params(self, xloc, yloc):
        xoffset, yoffset = self.config["window-offset"]
        zoom = self.config["window-zoom"]
        xloc, yloc = xloc * zoom, yloc * zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        return xloc, yloc

    def draw_drill_0(self, context, xloc, yloc, color, hp):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 16 * self.config["window-zoom"]
        
        context.set_source_rgba(*self.config["color-object"])
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        context.set_source_rgba(*color)
        context.arc(xloc, yloc, 2*r/3, 0, TWO_PI)
        context.fill()

    def draw_mineshaft_0(self, context, xloc, yloc, color, hp):
        self.draw_drill_0(context, xloc, yloc, color, hp)
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 25 * self.config["window-zoom"]
        w = 4 * self.config["window-zoom"]
        
        context.set_source_rgba(*self.config["color-object"])
        context.set_line_width(w)
        
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

    def draw(self, context):
        self.terr_painter.draw(context)
        for obj, xloc, yloc, player, hp, *params in self.battlefield["objects"]:
            shape = self.library["objects"][obj]["shape"]
            color = self.library["players"][player]["color"]
            if shape == "drill-0": self.draw_drill_0(context, xloc, yloc, color, hp)
            elif shape == "mineshaft-0": self.draw_mineshaft_0(context, xloc, yloc, color, hp)
            else: raise ValueError(f"Not supported object: {obj}")

class ObjectWindow(TerrWindow):
    def __init__(self, config, library, battlefield):
        self.painter = ObjectPainter(config, library, battlefield)
        self.graph = TerrGraph(battlefield)
        
        self.battlefield =  battlefield
        self.library = library
        self.config = config

        title = config["window-title"]
        width, height = config["window-size"]
        BaseWindow.__init__(self, title, width, height)

def run_example():
    example_config = {
        "window-title": "terr-window",
        "window-size": (1800, 820),
        "window-offset": (750, 400),
        "window-zoom": 0.566,
        "move-sensitive": 50,
        "color-object": (0.0, 0.0, 0.0)
    }

    from MapExamples import library0
    from MapExamples import battlefield0
    ObjectWindow(example_config, library0, battlefield0)

    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()

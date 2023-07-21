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

    def get_object_color(self, hp): 
        v = 0.8 * (1.0 - hp)
        if v > 1.0: v = 1.0
        return [v, v, v]

    def draw_polygon(self, context, color, points):
        context.set_source_rgba(*color)
        start_x, start_y = points[-1]
        context.move_to (start_x, start_y)
        for point in points:    
            stop_x, stop_y = point
            context.line_to (stop_x, stop_y)
        context.fill()
        context.stroke()

    def draw_control(self, context, xloc, yloc, color, resource):
        r = 8 * self.config["window-zoom"]
        context.set_source_rgba(*color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        try: color2 = self.library["resources"][resource]["color"]
        except KeyError: color2 = color

        r = 5 * self.config["window-zoom"]
        context.set_source_rgba(*color2)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

    def calc_render_params(self, xloc, yloc):
        xoffset, yoffset = self.config["window-offset"]
        zoom = self.config["window-zoom"]
        xloc, yloc = xloc * zoom, yloc * zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        return xloc, yloc

    def draw_drill_0(self, context, xloc, yloc, color, hp):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 16 * self.config["window-zoom"]

        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        context.set_source_rgba(*color)
        context.arc(xloc, yloc, 2*r/3, 0, TWO_PI)
        context.fill()

    def draw_mineshaft_0(self, context, xloc, yloc, color, hp, params):
        self.draw_drill_0(context, xloc, yloc, color, hp)
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 25 * self.config["window-zoom"]
        w = 4 * self.config["window-zoom"]

        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
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

        xc = xloc + 12 * self.config["window-zoom"]
        yc = yloc + 12 * self.config["window-zoom"]
        self.draw_control(context, xc, yc, ob_color, params[0])
        
    def draw_input_0(self, context, xloc, yloc, color, hp, params):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 18 * self.config["window-zoom"]
        
        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        xo, yo = xloc, yloc - r/20
        points = [(xo, yo-r/5), (xo + r*0.8, yo - r/2),
                  (xo, yo+r), (xo - r*0.8, yo - r/2)]
        self.draw_polygon(context, color, points)

        xc = xloc + 16 * self.config["window-zoom"]
        yc = yloc + 10 * self.config["window-zoom"]
        self.draw_control(context, xc, yc, ob_color, params[0])

    def draw_output_0(self, context, xloc, yloc, color, hp, params):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 18 * self.config["window-zoom"]

        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        xo, yo = xloc, yloc + r/20
        points = [(xo, yo+r/5), (xo + r*0.8, yo + r/2),
                  (xo, yo-r), (xo - r*0.8, yo + r/2)]
        self.draw_polygon(context, color, points)

        xc = xloc + 16 * self.config["window-zoom"]
        yc = yloc - 10 * self.config["window-zoom"]
        self.draw_control(context, xc, yc, ob_color, params[0])

    def draw_mixer_0(self, context, xloc, yloc, color, hp, params):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 24 * self.config["window-zoom"]
        
        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        context.set_source_rgba(*color)
        context.arc(xloc, yloc, 3*r/4, 0, TWO_PI)
        context.fill()

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

        xc = xloc + 16 * self.config["window-zoom"]
        yc = yloc + 16 * self.config["window-zoom"]
        self.draw_control(context, xc, yc, ob_color, params[0])

    def draw_store_0(self, context, xloc, yloc, color, hp, params):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 20 * self.config["window-zoom"]
        rr = 14 * self.config["window-zoom"]

        ob_color = self.get_object_color(hp)
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

        xc = xloc + 16 * self.config["window-zoom"]
        yc = yloc + 16 * self.config["window-zoom"]
        self.draw_control(context, xc, yc, ob_color, params[0])

    def draw_barrier_0(self, context, xloc, yloc, color, hp, params):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 24 * self.config["window-zoom"]
        rr = 20 * self.config["window-zoom"]
        rrr = 10 * self.config["window-zoom"]

        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()
        context.set_source_rgba(*color)
        context.arc(xloc, yloc, rr, 0, TWO_PI)
        context.fill()
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, rrr, 0, TWO_PI)
        context.fill()
        
        resource = self.library["objects"]["barrier"]["fuel"]
        xc = xloc + 16 * self.config["window-zoom"]
        yc = yloc + 16 * self.config["window-zoom"]
        self.draw_control(context, xc, yc, ob_color, resource)

    def draw_radiator_0(self, context, xloc, yloc, color, hp, params):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 24 * self.config["window-zoom"]
        rr = 8 * self.config["window-zoom"]
        
        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        context.set_source_rgba(*color)
        context.arc(xloc + 5*rr/3, yloc, rr, 0, TWO_PI)
        context.fill()
        context.arc(xloc - 5*rr/3, yloc, rr, 0, TWO_PI)
        context.fill()
        context.arc(xloc, yloc + 5*rr/3, rr, 0, TWO_PI)
        context.fill()
        context.arc(xloc, yloc - 5*rr/3, rr, 0, TWO_PI)
        context.fill()

        resource = self.library["objects"]["radiator"]["fuel"]
        xc = xloc + 16 * self.config["window-zoom"]
        yc = yloc + 16 * self.config["window-zoom"]
        self.draw_control(context, xc, yc, ob_color, resource)
        
    def draw_launcher_0(self, context, xloc, yloc, color, hp, params):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 24 * self.config["window-zoom"]
        rr = 10 * self.config["window-zoom"]
        rrr = 20 * self.config["window-zoom"]
        
        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        points = [(xloc-rrr, yloc-rr), (xloc+rrr, yloc-rr), (xloc, yloc+rrr)]
        self.draw_polygon(context, color, points)
        points = [(xloc-rrr, yloc+rr), (xloc+rrr, yloc+rr), (xloc, yloc-rrr)]
        self.draw_polygon(context, color, points)

        resource = self.library["objects"]["launcher"]["fuel"]
        xc = xloc + 16 * self.config["window-zoom"]
        yc = yloc + 16 * self.config["window-zoom"]
        self.draw_control(context, xc, yc, ob_color, resource)

    def draw_laboratory_0(self, context, xloc, yloc, color, hp, params):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 24 * self.config["window-zoom"]
        rr = 14 * self.config["window-zoom"]

        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        points = [(xloc-rr, yloc-rr), (xloc-rr, yloc+rr), (xloc, yloc)]
        self.draw_polygon(context, color, points)
        points = [(xloc+rr, yloc-rr), (xloc+rr, yloc+rr), (xloc, yloc)]
        self.draw_polygon(context, color, points)

        resource = self.library["objects"]["laboratory"]["fuel"]
        xc = xloc + 16 * self.config["window-zoom"]
        yc = yloc + 16 * self.config["window-zoom"]
        self.draw_control(context, xc, yc, ob_color, resource)

    def draw_developer_0(self, context, xloc, yloc, color, hp, params):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 24 * self.config["window-zoom"]
        rr = 36 * self.config["window-zoom"]

        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        xo, yo = xloc, yloc +rr/5
        points = [(xo, yo), (xo + 2*rr/5, yo - rr/4),
                  (xo, yo+rr/4), (xo - 2*rr/5, yo - rr/4)]
        self.draw_polygon(context, color, points)
        xo, yo = xloc, yloc - rr/5
        points = [(xo, yo), (xo + 2*rr/5, yo - rr/4),
                  (xo, yo+rr/4), (xo - 2*rr/5, yo - rr/4)]
        self.draw_polygon(context, color, points)

        resource = self.library["objects"]["developer"]["fuel"]
        xc = xloc + 16 * self.config["window-zoom"]
        yc = yloc + 16 * self.config["window-zoom"]
        self.draw_control(context, xc, yc, ob_color, resource)

    def draw_repeater_0(self, context, xloc, yloc, color, hp):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 14 * self.config["window-zoom"]
        rr = 24 * self.config["window-zoom"]

        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
        points = [(xloc-r, yloc-r), (xloc+r, yloc-r),
                  (xloc+r, yloc+r), (xloc-r, yloc+r)]
        self.draw_polygon(context, ob_color, points)
        context.fill()

        xo, yo = xloc, yloc +rr/5
        points = [(xo, yo), (xo + 2*rr/5, yo - rr/4),
                  (xo, yo+rr/4), (xo - 2*rr/5, yo - rr/4)]
        self.draw_polygon(context, color, points)
        xo, yo = xloc, yloc - rr/5
        points = [(xo, yo), (xo + 2*rr/5, yo - rr/4),
                  (xo, yo+rr/4), (xo - 2*rr/5, yo - rr/4)]
        self.draw_polygon(context, color, points)

    def draw_transmitter_0(self, context, xloc, yloc, color, hp, params):
        xloc, yloc = self.calc_render_params(xloc, yloc)
        r = 24 * self.config["window-zoom"]
        rr = 36 * self.config["window-zoom"]

        ob_color = self.get_object_color(hp)
        context.set_source_rgba(*ob_color)
        context.arc(xloc, yloc, r, 0, TWO_PI)
        context.fill()

        xo, yo = xloc, yloc - rr/5
        points = [(xo, yo), (xo + 2*rr/5, yo + rr/4),
                  (xo, yo - rr/4), (xo - 2*rr/5, yo + rr/4)]
        self.draw_polygon(context, color, points)
        xo, yo = xloc, yloc + rr/5
        points = [(xo, yo), (xo + 2*rr/5, yo + rr/4),
                  (xo, yo - rr/4), (xo - 2*rr/5, yo + rr/4)]
        self.draw_polygon(context, color, points)

        resource = self.library["objects"]["transmitter"]["fuel"]
        xc = xloc + 16 * self.config["window-zoom"]
        yc = yloc + 16 * self.config["window-zoom"]
        self.draw_control(context, xc, yc, ob_color, resource)
        
    def draw(self, context):
        self.terr_painter.draw(context)
        for obj, xloc, yloc, player, hp, *params in self.battlefield["objects"]:
            shape = self.library["objects"][obj]["shape"]
            color = self.library["players"][player]["color"]
            if shape == "drill-0": self.draw_drill_0(context, xloc, yloc, color, hp)
            elif shape == "mineshaft-0": self.draw_mineshaft_0(context, xloc, yloc, color, hp, params)
            elif shape == "output-0": self.draw_output_0(context, xloc, yloc, color, hp, params)
            elif shape == "input-0": self.draw_input_0(context, xloc, yloc, color, hp, params)
            elif shape == "store-0": self.draw_store_0(context, xloc, yloc, color, hp, params)
            elif shape == "mixer-0": self.draw_mixer_0(context, xloc, yloc, color, hp, params)
            elif shape == "launcher-0": self.draw_launcher_0(context, xloc, yloc, color, hp, params)
            elif shape == "radiator-0": self.draw_radiator_0(context, xloc, yloc, color, hp, params)
            elif shape == "barrier-0": self.draw_barrier_0(context, xloc, yloc, color, hp, params)
            elif shape == "laboratory-0": self.draw_laboratory_0(context, xloc, yloc, color, hp, params)
            elif shape == "transmitter-0": self.draw_transmitter_0(context, xloc, yloc, color, hp, params)
            elif shape == "developer-0": self.draw_developer_0(context, xloc, yloc, color, hp, params)
            elif shape == "repeater-0": self.draw_repeater_0(context, xloc, yloc, color, hp)
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
        "move-sensitive": 50
    }

    from MapExamples import library0
    from MapExamples import battlefield0
    ObjectWindow(example_config, library0, battlefield0)

    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()

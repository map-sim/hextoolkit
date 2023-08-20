import math
from TerrWindow import TerrPainter

TWO_PI = 2 * math.pi

class SimObject:
    black_color = 0, 0, 0, 1
    black2_color = 0.3, 0.3, 0.3, 1
    black3_color = 0.3, 0.3, 0.3, 0.75

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
    
    def _draw_center(self):
        r = 0.05 * self.config["window-zoom"]
        self.context.set_source_rgba(1, 1, 1)
        self.context.arc(*self.xy, r, 0, TWO_PI)
        self.context.fill()
        
    def _draw_hp_box(self, offset, status):
        w = 0.133 * self.config["window-zoom"]
        dx, dy = offset
        self.context.set_line_width(w)
        pts0 = [(-3.125*w+dx, -2.125*w+dy), (-3.125*w+dx, 2.125*w+dy),
                (3.125*w+dx, 2.125*w+dy), (3.125*w+dx, -2.125*w+dy)]
        self._draw_polygon(pts0, self.black3_color)
        pts0 = [(-3*w+dx, -2*w+dy), (-3*w+dx, 2*w+dy), (3*w+dx, 2*w+dy), (3*w+dx, -2*w+dy)]
        self._draw_polygon(pts0, self.black2_color)
        pts0 = [(-2*w+dx, -1*w+dy), (-2*w+dx, 1*w+dy), (2*w+dx, 1*w+dy), (2*w+dx, -1*w+dy)]
        if status: self._draw_polygon(pts0, self.color)
        else: self._draw_polygon(pts0, self.black_color)
    def _draw_modules(self, building, offset):
        w = 0.133 * self.config["window-zoom"]
        all_madules = self.library["objects"][building]["modules"]
        dx, dy = offset
        for i in range(all_madules):
            iv = int(i % 4) 
            ih = int(i / 4) 
            offset = dx + 6.25 * w * ih, dy - 4.25 * w * iv
            self._draw_hp_box(offset, i < self.modules)

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

class SimNuke_0(SimObject):
    def __init__(self, config, library, context, xyloc, player, modules):
        SimObject.__init__(self, config, library, context, xyloc, player, modules)

    def draw(self):
        r = 1.5 * self.config["window-zoom"]
        rr = 0.65 * self.config["window-zoom"]
        self.context.set_source_rgba(*self.black_color)
        self.context.arc(*self.xy, r, 0, TWO_PI)
        self.context.fill()
        self.context.set_source_rgba(*self.color)
        self.context.arc(*self.xy, 4*r/5, 0, TWO_PI)
        self.context.fill()

        x0, y0 = self.xy[0] - 0.88*rr, self.xy[1] - 0.88*rr
        self.context.set_source_rgba(*self.black_color)
        self.context.arc(x0, y0, rr, 0, TWO_PI)
        self.context.fill()
        self.context.set_source_rgba(*self.color)
        self.context.arc(x0, y0, 3*rr/4, 0, TWO_PI)
        self.context.fill()
        x1, y1 = self.xy[0] + 0.88*rr, self.xy[1] - 0.88*rr
        self.context.set_source_rgba(*self.black_color)
        self.context.arc(x1, y1, rr, 0, TWO_PI)
        self.context.fill()
        self.context.set_source_rgba(*self.color)
        self.context.arc(x1, y1, 3*rr/4, 0, TWO_PI)
        self.context.fill()
        x2, y2 = self.xy[0] - 0.88*rr, self.xy[1] + 0.88*rr
        self.context.set_source_rgba(*self.black_color)
        self.context.arc(x2, y2, rr, 0, TWO_PI)
        self.context.fill()
        self.context.set_source_rgba(*self.color)
        self.context.arc(x2, y2, 3*rr/4, 0, TWO_PI)
        self.context.fill()
        x3, y3 = self.xy[0] + 0.88*rr, self.xy[1] + 0.88*rr
        self.context.set_source_rgba(*self.black_color)
        self.context.arc(x3, y3, rr, 0, TWO_PI)
        self.context.fill()
        self.context.set_source_rgba(*self.color)
        self.context.arc(x3, y3, 3*rr/4, 0, TWO_PI)
        self.context.fill()

        self._draw_modules("nuke", (0.6 * r, 0.8 * r))
        self._draw_center()

class SimMine_0(SimObject):
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

        self._draw_modules("mixer", (0.95 * r, 0.3 * r))
        self._draw_resource((0, 0), self.resource)
        self._draw_center()

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

        w = 0.25 * self.config["window-zoom"]
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

        self._draw_modules("mixer", (0.95 * r, 0.3 * r))
        self._draw_resource((0, 0), self.resource)
        self._draw_center()

        
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
        self._draw_modules("store", (1.25 * r, 0.3 * r))
        self._draw_center()

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

            if shape == "nuke-0": SimNuke_0(self.config, self.library, context, xyloc, player, modules).draw()
            elif shape == "mine-0": SimMine_0(self.config, self.library, context, xyloc, player, modules, params[0]).draw()
            elif shape == "mixer-0": SimMixer_0(self.config, self.library, context, xyloc, player, modules, params[0]).draw()
            elif shape == "store-0": SimStore_0(self.config, self.library, context, xyloc, player, modules, params[0]).draw()
            else: raise ValueError(f"Not supported object: {obj}")

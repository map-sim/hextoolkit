import math, cairo

TWO_PI = 2 * math.pi
SQRT3 = math.sqrt(3)

class AbstractPainter:
    def __init__(self, saver):
        self.saver = saver

    def draw_base(self, context, color):
        context.set_source_rgba(*color)
        width, height = self.saver.settings["window-size"]
        context.rectangle(0, 0, width, height)
        context.fill()

    def draw_polygon(self, context, color, points):
        self.design_closed_lines(context, color, points)
        context.fill(); context.stroke()

    def design_closed_lines(self, context, color, points):
        xoffset, yoffset = self.saver.settings["window-offset"]
        zoom = self.saver.settings["window-zoom"]
        context.set_source_rgba(*color)

        start_x, start_y = points[-1]
        start_x, start_y = start_x*zoom, start_y*zoom
        start_x, start_y = start_x + xoffset, start_y + yoffset
        context.move_to (start_x, start_y)
        for point in points:    
            stop_x, stop_y = point
            stop_x, stop_y = stop_x*zoom, stop_y*zoom
            stop_x, stop_y = stop_x + xoffset, stop_y + yoffset
            context.line_to (stop_x, stop_y)
    
    def design_hex(self, context, color, xy):
        r = self.saver.settings.get("hex-radius")
        x, y = xy; h = 0.5 * r * SQRT3
        points = [(x, y+r), (x+h, y+r/2), (x+h, y-r/2),
                  (x, y-r), (x-h, y-r/2), (x-h, y+r/2)]
        self.design_closed_lines(context, color, points)

    @staticmethod
    def vex_to_loc(xy, r):        
        x, y = xy; yc = 1.5 * y * r
        if y % 2 == 0: xc = x * r * SQRT3
        else: xc = (x + 0.5) * r * SQRT3
        return xc, yc

    def translate_xy(self, x, y):
        zoom = self.saver.settings["window-zoom"]
        xoffset, yoffset = self.saver.settings["window-offset"]
        return x*zoom + xoffset, y*zoom + yoffset
        

class ObjPainter(AbstractPainter):
    def draw(self, context):
        for shape, *params in self.saver.markers:
            if shape == "vex": self.draw_vex(context, *params)
            elif shape == "cursor": self.draw_cursor(context, *params)
            elif shape == "link":
                if self.saver.settings["show-links"]:
                    self.draw_link(context, *params, link=True)
            elif shape == "arr":
                if self.saver.settings["show-arrows"]:
                    self.draw_link(context, *params, link=False)
            elif shape == "dash":
                if self.saver.settings["show-dashes"]:
                    self.draw_dash(context, *params)
            else: raise ValueError(f"Not supported shape: {shape}")

    def draw_dash(self, context, control, *vexes):
        def inner_point(x, y, r, c):
            context.set_source_rgba(*c)
            context.arc(x, y, r, 0, TWO_PI)
            context.fill()
        def inner_bi(xo, yo, xe, ye, r, c, r2):
            x2 = xo + float(xe - xo) / 2
            y2 = yo + float(ye - yo) / 2
            inner_point(x2, y2, r, c)
            d2 = (xo - xe) ** 2 + (yo - ye) ** 2
            if d2 > 30 * r2**2:
                inner_bi(xo, yo, x2, y2, r, c, r2)
                inner_bi(x2, y2, xe, ye, r, c, r2)
        def inner(w, r, c, r2):
            xe, ye = None, None
            for n, vex in enumerate(vexes):
                loc = ObjPainter.vex_to_loc(vex, rh)
                xo, yo = self.translate_xy(*loc)
                if n == 0: xe, ye = xo, yo; continue
                inner_bi(xo, yo, xe, ye, r, c, r2)
                inner_point(xe, ye, r, c)
                xe, ye = xo, yo
            inner_point(xe, ye, r, c)

        zoom = self.saver.settings["window-zoom"]
        rh = self.saver.settings.get("hex-radius", 1.0)
        color = self.saver.controls[control]["marker-color"]    
            
        inner(rh*zoom/5, rh*zoom/6.5, (1.0, 1.0, 1.0), rh*zoom/5)
        inner(rh*zoom/7, rh*zoom/8, (0.0, 0.0, 0.0), rh*zoom/5)
        inner(rh*zoom/9, rh*zoom/9.5, color, rh*zoom/5)

    def draw_link(self, context, control, *vexes, link=False):
        def inner_point(x, y, r, c):
            context.set_source_rgba(*c)
            context.arc(x, y, r, 0, TWO_PI)
            context.fill()
        def inner_line(xo, yo, xe, ye, w, c):        
            context.set_source_rgba(*c)
            context.set_line_width(w)
            context.move_to(xo, yo)
            context.line_to(xe, ye)
            context.stroke()
        def inner(w, r, c):
            xe, ye = None, None
            for n, vex in enumerate(vexes):
                loc = ObjPainter.vex_to_loc(vex, rh)
                xo, yo = self.translate_xy(*loc)
                if n == 0: xe, ye = xo, yo; continue
                inner_line(xo, yo, xe, ye, w, c)
                inner_point(xe, ye, r, c)
                xe, ye = xo, yo
            if link: inner_point(xe, ye, r, c)

        zoom = self.saver.settings["window-zoom"]
        rh = self.saver.settings.get("hex-radius", 1.0)
        color = self.saver.controls[control]["marker-color"]    
        inner(rh*zoom/5, rh*zoom/6.5, (1.0, 1.0, 1.0))
        inner(rh*zoom/7, rh*zoom/8, (0.0, 0.0, 0.0))
        inner(rh*zoom/9, rh*zoom/9.5, color)
        
    def draw_vex(self, context, control, xy):
        try: color = self.saver.controls[control]["marker-color"]
        except KeyError: color = self.saver.settings["marker-color"]
        color2 = tuple([*color, 0.2])
        r = self.saver.settings.get("hex-radius", 1.0)
        xc, yc = AbstractPainter.vex_to_loc(xy, r)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        zoom = self.saver.settings["window-zoom"]
        thickness = self.saver.settings["base-thickness"]
        context.set_line_width(thickness * zoom)
        self.design_hex(context, color2, (xc, yc))
        context.fill()
        self.design_hex(context, color, (xc, yc))
        context.stroke()

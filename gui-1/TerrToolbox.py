import math, cairo

SQRT3 = math.sqrt(3)
TWO_PI = 2 * math.pi
class TerrGraph:
    def __init__(self, saver):
        self.saver = saver
        self.default_vex_terr = None        
        self.grid_radius = self.saver.settings.get("hex-radius", 1.0)
        self.vex_dict = {}

        base_counter = 0
        for shape, *params in self.saver.landform:
            terr = params[0]
            if shape == "base":
                self.default_vex_terr = terr
                base_counter += 1
        assert base_counter <= 1, "base"
        for shape, *params in self.saver.landform:
            if shape != "vex": continue
            terr, xy = params[0], tuple(params[1])
            self.vex_dict[xy] = terr

    def get_hex_terr(self, xy):
        return self.vex_dict.get(xy, self.default_vex_terr)

    def transform_to_vex(self, xloc, yloc):
        h = SQRT3 * self.grid_radius / 2 
        ynorm = int(round(yloc / (1.5 * self.grid_radius)))
        yo = ynorm * 1.5 * self.grid_radius
        if ynorm % 2 == 1:
            xnorm = int(round((xloc - h) / (2 * h)))
            xo = xnorm * 2 * h + h
        else:
            xnorm = int(round(xloc / (2 * h)))
            xo = xnorm * 2 * h
        return (xnorm, ynorm), (xo, yo)

    def transform_to_oxy(self, vex):
        xhex, yhex = vex
        h = SQRT3 * self.grid_radius / 2 
        yo = yhex * 1.5 * self.grid_radius
        if yhex % 2 == 1: xo = xhex * 2 * h + h
        else: xo = xhex * 2 * h
        return xo, yo

    def check_in_polygon(self, xyloc, xypoints):
        # only if is convex polygon        
        (x, y), pos, neg = xyloc, 0, 0
        for index in range(len(xypoints)):
            x1, y1 = xypoints[index]
            if x == x1 and y == y1: return True
            index2 = (index + 1) % len(xypoints)
            x2, y2 = xypoints[index2]
            d = (x-x1)*(y2-y1) - (y-y1)*(x2-x1)
            if d > 0: pos += 1
            if d < 0: neg += 1
            if pos > 0 and neg > 0:
                return False
        return True
        
    def check_terrain(self, xloc, yloc):
        output_terr, output_row = None, None
        for shape, terr, *params in self.saver.landform:
            if shape == "base":
                output_terr = terr
                output_row = shape, terr
            elif shape == "rect":
                xo, yo = params[0], params[1]
                polygon = [(xo, yo), (xo+params[2], yo),
                           (xo+params[2], yo+params[3]), (xo, yo+params[3])]
                if self.check_in_polygon((xloc, yloc), polygon):
                    output_row = shape, terr, params
                    output_terr = terr
            elif shape == "polygon":
                if self.check_in_polygon((xloc, yloc), params):
                    output_row = shape, terr, params
                    output_terr = terr
            elif shape == "vex":
                r = self.grid_radius
                h = 0.5 * r * SQRT3
                x, y = TerrPainter.vex_to_loc(params[0], r)
                points = [(x, y+r), (x+h, y+r/2), (x+h, y-r/2),
                          (x, y-r), (x-h, y-r/2), (x-h, y+r/2)]                
                if self.check_in_polygon((xloc, yloc), points):
                    output_row = shape, terr, params
                    output_terr = terr
            elif shape == "grid": continue
            else: raise ValueError(f"not supported: {shape}")
        return output_terr, output_row


class AbstractPainter:
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

        
class TerrPainter(AbstractPainter):
    def __init__(self, saver):
        self.saver = saver

    def draw_vex(self, context, terrain, xy):
        color = self.saver.terrains[terrain]["color"]
        r = self.saver.settings.get("hex-radius", 1.0)
        xc, yc = AbstractPainter.vex_to_loc(xy, r)
        self.design_hex(context, color, (xc, yc))
        context.fill()

    def draw_base(self, context, terrain):
        color = self.saver.terrains[terrain]["color"]
        AbstractPainter.draw_base(self, context, color)

    def draw_grid(self, context, color, thickness):
        r = self.saver.settings.get("hex-radius", 1.0)
        w, h = self.saver.settings["window-size"]
        dx, dy = self.saver.settings["window-offset"]
        zoom = self.saver.settings["window-zoom"]

        xio = -int(round(dx / r / zoom / SQRT3)) - 1
        xie = int(round(xio +  w / r / zoom / SQRT3)) + 4
        yio = -int(round(dy / 1.5 / r / zoom) + 0.5) - 1 
        yie = int(round(yio + h / 1.5 / zoom)) + 4
        if (yie - yio) * (xie - xio) > 8000: return
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.set_line_width(thickness * zoom)
        for xi in range(xio, xie):
            for yi in range(yio, yie):
                xc, yc = TerrPainter.vex_to_loc((xi, yi), r)
                self.design_hex(context, color, (xc, yc))
        context.stroke()        
        
    def draw(self, context):
        for shape, *params in self.saver.landform:
            if shape == "base": self.draw_base(context, *params)
            elif shape == "vex": self.draw_vex(context, *params)
            elif shape == "grid": self.draw_grid(context, *params)
            else: raise ValueError(f"Not supported shape: {shape}")


class ObjPainter(AbstractPainter):
    def __init__(self, saver):
        self.saver = saver

    def translate_xy(self, x, y):
        zoom = self.saver.settings["window-zoom"]
        xoffset, yoffset = self.saver.settings["window-offset"]
        return x*zoom + xoffset, y*zoom + yoffset
        
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
                xo, yo = self.translate_xy(*TerrPainter.vex_to_loc(vex, rh))
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
                xo, yo = self.translate_xy(*TerrPainter.vex_to_loc(vex, rh))
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

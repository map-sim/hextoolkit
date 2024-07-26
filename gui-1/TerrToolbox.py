import math, cairo

from ObjPainter import AbstractPainter
from ObjPainter import SQRT3


class TerrPainter(AbstractPainter):        
    def draw(self, context):
        for shape, *params in self.saver.landform:
            if shape == "base": self.draw_base(context, *params)
            elif shape == "vex": self.draw_vex(context, *params)
            elif shape == "grid": self.draw_grid(context, *params)
            else: raise ValueError(f"Not supported shape: {shape}")

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

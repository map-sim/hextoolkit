import math, cairo

SQRT3 = math.sqrt(3)
class TerrPainter:    
    def __init__(self, saver):
        self.saver = saver

    @staticmethod
    def is_convex_polygon(polygon):
        """
        taken from:
        https://stackoverflow.com/questions/471962/how-do-i-efficiently-
        determine-if-a-polygon-is-convex-non-convex-or-complex
        """
        TWO_PI = 2 * math.pi
        try:
            if len(polygon) < 3: return False
            old_x, old_y = polygon[-2]
            new_x, new_y = polygon[-1]
            new_direction = math.atan2(new_y - old_y, new_x - old_x)
            angle_sum = 0.0
            for ndx, newpoint in enumerate(polygon):
                old_x, old_y, old_direction = new_x, new_y, new_direction
                new_x, new_y = newpoint
                new_direction = math.atan2(new_y - old_y, new_x - old_x)
                if old_x == new_x and old_y == new_y: return False
                angle = new_direction - old_direction
                if angle <= -math.pi: angle += TWO_PI
                elif angle > math.pi: angle -= TWO_PI
                if ndx == 0 and angle == 0.0: return False
                elif ndx == 0: orientation = 1.0 if angle > 0.0 else -1.0
                elif orientation * angle <= 0.0: return False	            
                angle_sum += angle
            return abs(round(angle_sum / TWO_PI)) == 1
        except (ArithmeticError, TypeError, ValueError):
            return False

    def draw_base(self, context, terrain):
        width, height = self.saver.settings["window-size"]
        color = self.saver.terrains[terrain]["color"]
        context.set_source_rgba(*color)
        context.rectangle(0, 0, width, height)
        context.fill()

    def draw_rect(self, context, terrain, xloc, yloc, wbox, hbox):
        zoom = self.saver.settings["window-zoom"]
        xoffset, yoffset = self.saver.settings["window-offset"]
        color = self.saver.terrains[terrain]["color"]
        context.set_source_rgba(*color)
        xloc, yloc = xloc*zoom, yloc*zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        context.rectangle(xloc, yloc, wbox*zoom, hbox*zoom)
        context.fill()
        context.stroke()

    def _draw_closed_lines(self, context, color, points):
        xoffset, yoffset = self.saver.settings["window-offset"]
        zoom = self.saver.settings["window-zoom"]
        if not TerrPainter.is_convex_polygon(points):
            print("WARNING! Polygon is not convex!")
            color = 1, 0, 0, 1
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
    def draw_polygon(self, context, terrain, points):
        color = self.saver.terrains[terrain]["color"]
        self._draw_closed_lines(context, color, points)
        context.fill()
        context.stroke()
    def _draw_hex(self, context, terrain, xy, r=1.0):
        x, y = xy; h = 0.5 * r * SQRT3    
        points = [(x, y+r), (x+h, y+r/2), (x+h, y-r/2),
                  (x, y-r), (x-h, y-r/2), (x-h, y+r/2)]
        return self.draw_polygon(context, terrain, points)

    def _draw_skeleton(self, context, color, thickness, points):
        self._draw_closed_lines(context, color, points)
        zoom = self.saver.settings["window-zoom"]
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.set_line_width(thickness*zoom)

    @staticmethod
    def _vex_to_loc(xy, r):        
        x, y = xy; yc = 1.5 * y * r
        if y % 2 == 0: xc = x * r * SQRT3
        else: xc = (x + 0.5) * r * SQRT3
        return xc, yc

    def draw_vex(self, context, terrain, xy):
        r = self.saver.settings.get("hex-radius", 1.0)
        xc, yc = TerrPainter._vex_to_loc(xy, r)
        self._draw_hex(context, terrain, (xc, yc), r)
    def draw_gex(self, context, color, thickness, xy):
        r = self.saver.settings.get("hex-radius", 1.0)
        xc, yc = TerrPainter._vex_to_loc(xy, r)
        h = 0.5 * r * SQRT3
        points = [(xc, yc+r), (xc+h, yc+r/2), (xc+h, yc-r/2),
                  (xc, yc-r), (xc-h, yc-r/2), (xc-h, yc+r/2)]
        self._draw_skeleton(context, color, thickness, points)

    def draw_grid(self, context, color, thickness=0.5):
        r = self.saver.settings.get("hex-radius", 1.0)
        w, h = self.saver.settings["window-size"]
        dx, dy = self.saver.settings["window-offset"]
        zoom = self.saver.settings["window-zoom"]

        xio = -int(round(dx / r / zoom / SQRT3)) - 1
        xie = int(round(xio +  w / r / zoom / SQRT3)) + 4
        yio = -int(round(dy / 1.5 / r / zoom) + 0.5) - 1 
        yie = int(round(yio + h / 1.5 / zoom)) + 4
        if (yie - yio) * (xie - xio) > 8000: return                
        for xi in range(xio, xie):
            for yi in range(yio, yie):
                self.draw_gex(context, color, thickness, (xi, yi))
        context.stroke()        
        
    def draw(self, context):
        for shape, *params in self.saver.landform:
            if shape == "base": self.draw_base(context, *params)
            elif shape == "vex": self.draw_vex(context, *params)
            elif shape == "grid": self.draw_grid(context, *params)
            elif shape == "rect": self.draw_rect(context, *params)
            elif shape == "polygon": self.draw_polygon(context, *params)
            else: raise ValueError(f"Not supported shape: {shape}")

class TerrGraph:
    # def __init__(self, battlefield):
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
            terr, xy = params[0], params[1]
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
                x, y = TerrPainter._vex_to_loc(params[0], r)
                points = [(x, y+r), (x+h, y+r/2), (x+h, y-r/2),
                          (x, y-r), (x-h, y-r/2), (x-h, y+r/2)]                
                if self.check_in_polygon((xloc, yloc), points):
                    output_row = shape, terr, params
                    output_terr = terr
            elif shape == "grid": continue
            else: raise ValueError(f"not supported: {shape}")
        return output_terr, output_row


import gi, os, copy, math, cairo
from pprint import pformat

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from TerrWindow import TerrWindow
from TerrWindow import TerrPainter
from TerrWindow import TerrGraph

TWO_PI = 2 * math.pi

class SimPoint:
    def _calc_render_xy(self, xloc, yloc):
        zoom = self.config["window-zoom"]
        xloc, yloc = xloc * zoom, yloc * zoom
        xoffset, yoffset = self.config["window-offset"]
        return xloc + xoffset, yloc + yoffset

class SimObject(SimPoint):
    black_color = 0.45, 0.45, 0.45, 1
    black2_color = 0.5, 0.5, 0.5, 1
    black3_color = 0.5, 0.5, 0.5, 0.75
    not_oper_color = 0.8, 0.8, 0.8, 1
    color_armor =  1, 1, 1, 1

    def __init__(self, config, library, context, xy, own, cnt):
        self.config, self.library = config, library
        self.color = self.library["players"][own]["color"]
        self.xy = self._calc_render_xy(*xy)
        self.context = context
        self.modules = cnt
        self.xyloc = xy

    def _draw_line(self, xy0, xy1, color, width=None):
        if width is not None: self.context.set_line_width(width)
        self.context.set_line_cap(cairo.LINE_CAP_ROUND)
        self.context.set_source_rgba(*color)
        xy0  = self.xy[0] + xy0[0], self.xy[1] + xy0[1]
        xy1  = self.xy[0] + xy1[0], self.xy[1] + xy1[1]
        self.context.move_to(*xy0)
        self.context.line_to(*xy1) 
        self.context.stroke()
    
    def _draw_center(self):
        # r = 0.05 * self.config["window-zoom"]
        # self.context.set_source_rgba(1, 1, 1)
        # self.context.arc(*self.xy, r, 0, TWO_PI)
        # self.context.fill()
        pass

    def _draw_hp_box(self, offset, status, oper, armor=False):
        w = 0.133 * self.config["window-zoom"]
        dx, dy = offset
        self.context.set_line_width(w)
        pts0 = [(-3.125*w+dx, -2.125*w+dy), (-3.125*w+dx, 2.125*w+dy),
                (3.125*w+dx, 2.125*w+dy), (3.125*w+dx, -2.125*w+dy)]
        self._draw_polygon(pts0, self.black3_color)
        pts0 = [(-3*w+dx, -2*w+dy), (-3*w+dx, 2*w+dy), (3*w+dx, 2*w+dy), (3*w+dx, -2*w+dy)]
        if oper: self._draw_polygon(pts0, self.black2_color)
        else: self._draw_polygon(pts0, self.not_oper_color)
        pts1 = [(-2*w+dx, -1*w+dy), (-2*w+dx, 1*w+dy), (2*w+dx, 1*w+dy), (2*w+dx, -1*w+dy)]
        if status: self._draw_polygon(pts1, self.color)
        elif armor: self._draw_polygon(pts1, self.color_armor)
        else: self._draw_polygon(pts1, self.black_color)

    def _draw_modules(self, building, offset):
        w = 0.133 * self.config["window-zoom"]
        all_madules = self.library["objects"][building]["modules"]
        dx, dy = offset
        for i in range(all_madules):
            iv = int(i % 4) 
            ih = int(i / 4) 
            offset = dx + 6.25 * w * ih, dy - 4.25 * w * iv
            if self.modules > 0: modules = self.modules
            else: modules = -self.modules
            self._draw_hp_box(offset, i < modules, self.modules > 0)
        if self.armor:
            offset = dx + 6.25 * w * ih, dy - 4.25 * w * (iv + 1)
            self._draw_hp_box(offset, None, True, armor=True)
            
    def _draw_polygon(self, points, color, width=None):
        if width is not None: self.context.set_line_width(width)
        self.context.set_line_cap(cairo.LINE_CAP_ROUND)
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

        if resource is True: color2 = 1, 1, 1, 1
        elif resource is None: color2 = self.black_color
        elif resource is False: color2 = self.black_color     
        else: color2 = self.library["resources"][resource]["color"]
        self.context.set_source_rgba(*color2)
        rr = 0.18 * self.config["window-zoom"]
        self.context.arc(*xy, rr, 0, TWO_PI)
        self.context.fill()

class SimNuke_0(SimObject):
    def __init__(self, config, library, context, oxy, xy, name, own, cnt):
        SimObject.__init__(self, config, library, context, oxy, own, cnt)
        self.armor = False

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

        self._draw_modules("nuke", (0.6 * r, 0.6 * r))
        self._draw_center()

class SimMine_0(SimObject):
    def __init__(self, config, library, context, oxy, xy, name, own, cnt, armor, out):
        SimObject.__init__(self, config, library, context, oxy, own, cnt)        
        self.resource = out
        self.armor = armor

    def draw(self):
        r = 1 * self.config["window-zoom"]
        self.context.set_source_rgba(*self.black_color)
        self.context.arc(*self.xy, r, 0, TWO_PI)
        self.context.fill()
        self.context.set_source_rgba(*self.color)
        self.context.arc(*self.xy, 3*r/4, 0, TWO_PI)
        self.context.fill()

        self._draw_modules("mixer", (0.95 * r, 0.5 * r))
        self._draw_resource((0, 0), self.resource)
        self._draw_center()

class SimMixer_0(SimObject):
    def __init__(self, config, library, context, oxy, xy, name, own, cnt, armor, out):
        SimObject.__init__(self, config, library, context, oxy, own, cnt)        
        self.resource = out
        self.armor = armor

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
        self._draw_line((-rr, rr), (rr, -rr), self.black_color)
        self._draw_line((rr, rr), (-rr, -rr), self.black_color)    
        self._draw_modules("mixer", (0.95 * r, 0.5 * r))
        self._draw_resource((0, 0), self.resource)
        self._draw_center()
        
class SimStore_0(SimObject):
    cells = [(-0.43, -0.84), (0.43, -0.84), (-0.43, 0),
             (0.43, 0), (-0.43, 0.84), (0.43, 0.84)]    
    def __init__(self, config, library, context, oxy, xy, name, own, cnt, armor, goods, work):
        SimObject.__init__(self, config, library, context, oxy, own, cnt)        
        self.resources = goods
        self.armor = armor
        self.work = work

    def draw(self):
        r = 0.65 * self.config["window-zoom"]
        rr = 0.5 * self.config["window-zoom"]
        w = 0.1 * self.config["window-zoom"]

        self.context.set_line_width(w)
        self.context.set_source_rgba(*self.black_color)
        pts0 = [(-r, -1.3*r), (-r, +1.3*r), (+r, +1.3*r), (+r, -1.3*r)]
        pts1 = [(-rr, -1.3*rr), (-rr, +1.3*rr), (+rr, +1.3*rr), (+rr, -1.3*rr)]
        self._draw_polygon(pts0, self.black_color)
        self._draw_polygon(pts1, self.color)

        rrr = 0.722 * self.config["window-zoom"]
        rrrr = 0.273 * self.config["window-zoom"]
        for i, resource in enumerate(self.resources):
            xyloc = r * self.cells[i][0], r * self.cells[i][1]
            self._draw_resource(xyloc, resource)
        self._draw_modules("store", (1.3 * r, 0.7 * r))
        self._draw_resource((-rrr, rrrr), self.work)
        self._draw_center()

class SimLab_0(SimObject):
    def __init__(self, config, library, context, oxy, xy, name, own, cnt, armor, work):
        SimObject.__init__(self, config, library, context, oxy, own, cnt)
        self.armor = armor
        self.work = work

    def draw(self):
        r = 1.25 * self.config["window-zoom"]
        rr = 0.6 * self.config["window-zoom"]
        pts = [(0, r), (r, 0), (0, -r), (-r, 0)]
        self._draw_polygon(pts, self.black_color)
        self.context.set_source_rgba(*self.color)
        self.context.arc(*self.xy, rr, 0, TWO_PI)
        self.context.fill()
        self._draw_modules("lab", (0.75 * r, 0.5 * r))
        self._draw_resource((-rr, rr), self.work)
        self._draw_center()

class SimHit_0(SimObject):
    def __init__(self, config, library, context, oxy, xy, name, own, cnt, armor, work):
        SimObject.__init__(self, config, library, context, oxy, own, cnt)
        self.armor = armor
        self.work = work

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
        
        rr, rrr = r * 4/3, 0.7 * r
        self._draw_line((-rr, 0), (rr, 0), self.black_color)
        self._draw_line((0, -rr), (0, rr), self.black_color)
        self._draw_modules("hit", (0.75 * r, 0.75 * r))
        self._draw_resource((-rrr, rrr), self.work)
        self._draw_center()

class SimDevel_0(SimObject):
    def __init__(self, config, library, context, oxy, xy, name, own, cnt, armor, work):
        SimObject.__init__(self, config, library, context, oxy, own, cnt)
        self.armor = armor
        self.work = work

    def draw(self):
        r = 1 * self.config["window-zoom"]
        rr = 0.6 * self.config["window-zoom"]
        rrr = 0.7 * self.config["window-zoom"]                
        self.context.set_source_rgba(*self.black_color)
        self.context.arc(*self.xy, r, 0, TWO_PI)
        self.context.fill()

        pts1 = [(0, 0.5*rr), (-rr, -rr), (+rr, -rr)]
        self._draw_polygon(pts1, self.color)
        pts2 = [(0, 1.5*rr), (-rr, 0), (+rr, 0)]
        self._draw_polygon(pts2, self.color)
     
        self._draw_modules("devel", (0.8 * r, 0.75 * r))
        self._draw_resource((-rrr, rrr), self.work)
        self._draw_center()

class SimSend_0(SimObject):
    def __init__(self, config, library, context, oxy, xy, name, own, cnt, armor, work):
        SimObject.__init__(self, config, library, context, oxy, own, cnt)
        self.armor = armor
        self.work = work

    def draw(self):
        r = 1 * self.config["window-zoom"]
        rr = 0.6 * self.config["window-zoom"]
        rrr = 0.7 * self.config["window-zoom"]
        self.context.set_source_rgba(*self.black_color)
        self.context.arc(*self.xy, r, 0, TWO_PI)
        self.context.fill()

        pts1 = [(0, -0.5*rr), (-rr, rr), (+rr, rr)]
        self._draw_polygon(pts1, self.color)
        pts2 = [(0, -1.5*rr), (-rr, 0), (+rr, 0)]
        self._draw_polygon(pts2, self.color)
     
        self._draw_modules("send", (0.8 * r, 0.5 * r))
        self._draw_resource((-rrr, -rrr), self.work)
        self._draw_center()

class SimPost_0(SimObject):
    def __init__(self, config, library, context, oxy, xy, name, own, cnt, armor):
        SimObject.__init__(self, config, library, context, oxy, own, cnt)
        self.armor = armor

    def draw(self):
        r = 0.5 * self.config["window-zoom"]
        rr = 0.3 * self.config["window-zoom"]
        self.context.set_source_rgba(*self.black_color)
        self.context.arc(*self.xy, r, 0, TWO_PI)
        self.context.fill()
        self.context.set_source_rgba(*self.color)
        self.context.arc(*self.xy, rr, 0, TWO_PI)
        self.context.fill()

        self._draw_modules("post", (r, 0.5 * r))
        self._draw_center()




        
class HexPainter: #(TerrPainter):
    def __init__(self, config, library, battlefield):
        self.terr_painter = TerrPainter(config, library, battlefield)
        self.terr_graph = TerrGraph(battlefield)

        self.battlefield =  battlefield
        self.library = library
        self.config = config

    def draw(self, context):
        self.terr_painter.draw(context)

        for obj in self.battlefield["objects"]:
            ox, oy = self.terr_graph.transform_to_oxy(*obj["xy"])
            
            shape = self.library["objects"][obj["name"]]["shape"]
            if shape == "nuke-0": SimNuke_0(self.config, self.library, context, (ox, oy), **obj).draw()
            elif shape == "lab-0": SimLab_0(self.config, self.library, context, (ox, oy), **obj).draw()
            elif shape == "hit-0": SimHit_0(self.config, self.library, context, (ox, oy), **obj).draw()
            elif shape == "mine-0": SimMine_0(self.config, self.library, context, (ox, oy), **obj).draw()
            elif shape == "mixer-0": SimMixer_0(self.config, self.library, context, (ox, oy), **obj).draw()
            elif shape == "store-0": SimStore_0(self.config, self.library, context, (ox, oy), **obj).draw()
            elif shape == "devel-0": SimDevel_0(self.config, self.library, context, (ox, oy), **obj).draw()
            elif shape == "send-0": SimSend_0(self.config, self.library, context, (ox, oy), **obj).draw()
            elif shape == "post-0": SimPost_0(self.config, self.library, context, (ox, oy), **obj).draw()
            else: raise ValueError(f"Not supported object: {obj['name']}")

        
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

#!/usr/bin/python3

import gi, cairo, copy
from BaseWindow import BaseWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class NaviPainter:
    def __init__(self, settings):
        self.settings = settings

    def draw_base(self, context, color):
        width, height = self.settings["window-size"]
        context.set_source_rgba(*color)
        context.rectangle(0, 0, width, height)
        context.fill()

    def draw_rect(self, context, params, color):
        zoom = self.settings["window-zoom"]
        xoffset, yoffset = self.settings["window-offset"]
        context.set_source_rgba(*color)
        xloc, yloc, wbox, hbox = params
        xloc, yloc = xloc*zoom, yloc*zoom
        xloc, yloc = xloc + xoffset, yloc + yoffset
        context.rectangle(xloc, yloc, wbox*zoom, hbox*zoom)
        context.fill()

    def draw(self, context):
        bcolor = self.settings["background-color"]
        self.draw_base(context, bcolor)

        fcolor = self.settings["foreground-color"]
        self.draw_rect(context, self.settings["primary-rect"], fcolor)
        self.draw_rect(context, self.settings["secondary-rect"], fcolor)
        
class NaviWindow(BaseWindow):
    def __init__(self, settings):
        self.painter = NaviPainter(settings)
        self.settings_backup = copy.deepcopy(settings)
        self.settings = settings

        title = settings["window-title"]
        width, height = settings["window-size"]
        BaseWindow.__init__(self, title, width, height)

    def init_window(self):
        self.surface = None
        self.draw_content()
        self.show_all()

    def on_press(self, widget, event):
        if isinstance(event, str): key_name = event
        else: key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Escape":
            print("##> move center & redraw")
            self.settings["window-offset"] = self.settings_backup["window-offset"]
            self.settings["window-zoom"] = self.settings_backup["window-zoom"]
            self.draw_content()
        elif key_name == "Up":
            print("##> move up & redraw")
            hop = self.settings["move-sensitive"]
            xoffset, yoffset = self.settings["window-offset"]
            self.settings["window-offset"] = xoffset, yoffset + hop
            self.draw_content()
        elif key_name == "Down":
            print("##> move down & redraw")
            hop = self.settings["move-sensitive"]
            xoffset, yoffset = self.settings["window-offset"]
            self.settings["window-offset"] = xoffset, yoffset - hop
            self.draw_content()
        elif key_name == "Left":
            print("##> move left & redraw")
            hop = self.settings["move-sensitive"]
            xoffset, yoffset = self.settings["window-offset"]
            self.settings["window-offset"] = xoffset + hop, yoffset
            self.draw_content()
        elif key_name == "Right":
            print("##> move right & redraw")
            hop = self.settings["move-sensitive"]
            xoffset, yoffset = self.settings["window-offset"]
            self.settings["window-offset"] = xoffset - hop, yoffset
            self.draw_content()
        elif key_name in ("minus", "KP_Subtract"):
            print("##> zoom out & redraw")
            self.settings["window-zoom"] *= 0.75
            self.draw_content()
        elif key_name in ("plus", "KP_Add"):
            print("##> zoom in & redraw")
            self.settings["window-zoom"] *= 1.25
            self.draw_content()
        else:
            print("not supported key:")
            if not isinstance(event, str):
                print("\tkey name:", Gdk.keyval_name(event.keyval))
                print("\tkey value:", event.keyval)
            else: print("\tkey name:", event)
        return True

    @BaseWindow.double_buffering
    def draw_content(self, context):
        self.painter.draw(context)
        context.stroke()

    def on_scroll(self, widget, event):
        xoffset, yoffset = self.settings["window-offset"]
        width, height = self.settings["window-size"]
        zoom = self.settings["window-zoom"]
        ox = (event.x - xoffset) / zoom
        oy = (event.y - yoffset) / zoom
        
        if event.direction == Gdk.ScrollDirection.DOWN:
            self.settings["window-zoom"] *= 0.75
        elif event.direction == Gdk.ScrollDirection.UP:
            self.settings["window-zoom"] *= 1.25

        zoom2 = self.settings["window-zoom"]
        xoffset = event.x - ox * zoom2
        yoffset = event.y - oy * zoom2
        self.settings["window-offset"] = xoffset, yoffset
        self.draw_content()
        return True

    def on_click(self, widget, event):
        xoffset, yoffset = self.settings["window-offset"]
        width, height = self.settings["window-size"]
        zoom = self.settings["window-zoom"]
        ox = (int(event.x) - xoffset) / zoom
        oy = (int(event.y) - yoffset) / zoom

        # cnts = event.get_click_count()
        print(f"({round(ox, 2)}, {round(oy, 2)})")
        return True

def run_example():
    example_settings = {
        "window-title": "navi-window",
        "window-size": (600, 400),
        "window-offset": (100, 50),
        "window-zoom": 1.333,
        "move-sensitive": 50,
        
        "primary-rect": (0, 0, 200, 100),
        "secondary-rect": (200, 100, 100, 50),
        "foreground-color": (1, 0, 0),
        "background-color": (1, 1, 1)
    }
    
    NaviWindow(example_settings)
    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()
        

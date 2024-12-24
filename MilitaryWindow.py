import gi, math

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from ObjPainter import AbstractPainter

class MilitaryWindow(Gtk.Window):

    def on_destroy(self, widget):
        self.main_window.military_window = None
        print("destroy")

    def on_clicked_delete(self, widget):
        vex = self.main_window.selected_vex
        uid = self.main_window.selected_unit
        units = self.main_window.saver.military.get(vex)
        if units[uid]["order"] == "transport":
            fvex = units[uid]["from"][0]
            funits = self.main_window.saver.military.get(fvex)
            tunit = funits[units[uid]["unit"]]
            if tunit["order"] == "landing":
                tunit["order"] = "defence"
                del tunit["progress"]
                del tunit["to"]
            else: print("warning: not expected order")
        del units[uid]
        self.main_window.draw_content()
        self.destroy()
        
    def on_clicked_next(self, widget):
        self.main_window.on_press(widget, "v")

    def __init__(self, main_window):
        Gtk.Window.__init__(self, title="unit-window")
        self.connect("destroy", self.on_destroy)
        self.main_window = main_window
        self.control_window = self.main_window.control_window

        self.box = Gtk.VBox(spacing=3)
        self.add(self.box)
        
        hbox = Gtk.HBox(spacing=3) 
        self.box.pack_start(hbox, False, True, 0)

        button = Gtk.Button(label="Delete-Unit")
        button.connect("clicked", self.on_clicked_delete)
        hbox.pack_start(button, False, True, 0)

        button = Gtk.Button(label="Next-Unit")
        button.connect("clicked", self.on_clicked_next)
        hbox.pack_start(button, False, True, 0)

        self.box.pack_start(Gtk.Separator(), False, True, 0)
        self.box.pack_start(Gtk.Separator(), False, True, 0)

        self.info = Gtk.Label(label="")
        self.box.pack_start(self.info, False, True, 0)        
        display_data = self.selected_military_view()
        self.info.set_yalign(0.0)

        self.set_title(f"unit-window")
        self.add_events(Gdk.EventMask.SCROLL_MASK)
        print("unit-window...")
        self.show_all()

    def selected_military_view(self):
        vex = self.main_window.selected_vex
        uid = self.main_window.selected_unit
        info = f"selected unit: {uid}\n"
        info += f"selected vex: {vex}\n\n"
        if uid is not None:
            units = self.main_window.saver.military.get(vex)
            if units is not None:
                unit = units[uid]
                info += f"unit ({uid}) from {len(units)}"
                info += f"\nhex: {vex}"
                info += f"\nowner: {unit['own']}"
                info += f"\ntype: {unit['type']}"
                info += f"\nsize: {unit['size']}"
                info += f"\nexp: {round(unit['exp'], 2)}"
                info += f"\nstate: {round(100*unit['state'])}%"
                info += f"\nstock basic: {round(100*unit['stock'][0])}%"
                info += f"\nstock main: {round(100*unit['stock'][1])}%"
                info += f"\norder: {unit['order']}"
                if "progress" in unit:
                    info += f"\nprogress: {round(100*unit['progress'])}"
                if "unit" in unit:
                    info += f"\nunit: {unit['unit']}"
                if "from" in unit:
                    source = "\n  > ".join(map(str, unit['from']))
                    info += f"\nfrom: {source}"
                if "to" in unit:
                    if isinstance(unit['to'], list):
                        target = "\n  > ".join(map(str, unit['to']))
                    else: target = str(unit['to'])
                    info += f"\nto: {target}"
                if "location" in unit:
                    location = "\n  < ".join(map(str, unit['location']))
                    info += f"\nlocation: {location}"

                unitdef = self.main_window.saver.units[unit['type']]
                radius = unitdef["action-perf"]["range"]
                self.mark_range(unit['own'], vex, radius)
            else:  info += "No units to select..."
        else: info += "No selected unit..."
        self.info.set_text(info)
        return info
        
    def mark_range(self, own, vex, radius):        
        if radius < 1: return
        r = self.main_window.saver.settings.get("hex-radius", 1.0)
        xo, yo = AbstractPainter.vex_to_loc(vex, r)
        
        self.main_window.saver.unmark_all_vexes()
        self.main_window.saver.markers.append(["vex", None, vex])
        for x in range(int(vex[0]-radius-3), int(vex[0]+radius+2)):
            for y in range(int(vex[1]-radius-3), int(vex[1]+radius+2)):
                if x == 0 and y == 0: continue 
                vex2 = vex[0] + x, vex[1] + y 
                xe, ye = AbstractPainter.vex_to_loc(vex2, r)                
                d = math.sqrt((xo-xe)**2 + (yo-ye)**2)
                if d > r * radius: continue
                self.main_window.saver.markers.append(["vex", own, vex2])
        self.main_window.draw_content()

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class MilitaryWindow(Gtk.Window):

    def on_destroy(self, widget):
        self.main_window.military_panel = None
        print("destroy")

    def on_clicked_delete(self, widget):
        print("--")
        
    def __init__(self, main_window):
        Gtk.Window.__init__(self, title="unit-window")
        self.connect("destroy", self.on_destroy)
        self.main_window = main_window
        self.control_panel = self.main_window.control_panel

        self.fix = Gtk.Fixed()
        self.add(self.fix)
        
        button = Gtk.Button(label="Delete-Unit")
        button.connect("clicked", self.on_clicked_delete)
        self.fix.put(button, 0, 3)

        self.info = Gtk.Label(label="")
        self.info.set_yalign(0.0)
        self.fix.put(self.info, 0, 40)
        display_data = self.selected_military_view()
        
        self.set_title(f"unit-window")
        self.add_events(Gdk.EventMask.SCROLL_MASK)
        print("unit-window...")
        self.show_all()

    def selected_military_view(self):
        vex = self.main_window.selected_vex
        uid = self.main_window.selected_unit
        info = f"selected unit: {uid}\n"
        info += f"selected vex: {vex}\n"
        info += "-" * 60 + "\n"
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
            else:  info += "No units to select..."
        else: info += "No selected unit..."
        self.info.set_text(info)
        return info
        

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class UnitWindow(Gtk.Window):

    def on_destroy(self, widget):
        self.main_window.unit_panel = None
        print("destroy")
        
    def __init__(self, main_window):
        Gtk.Window.__init__(self, title="unit-window")
        self.connect("destroy", self.on_destroy)
        self.main_window = main_window
        self.control_panel = self.main_window.control_panel

        self.fix = Gtk.Fixed()
        self.add(self.fix)

        vex = self.main_window.selected_vex
        unit_id = self.main_window.selected_unit
        display_data = f"selected vex: {vex}\n"
        display_data += f"selected unit: {unit_id}\n"
        display_data += "-------------------------\n"

        mview = self.control_panel.selected_military_view()
        display_data += mview
        
        #units = self.main_window.saver.military[vex]
        #unit = units[unit_id]
        
        self.info = Gtk.Label(label=display_data)
        self.info.set_yalign(0.0)
        self.fix.put(self.info, 0, 0)
        
        self.set_title(f"unit-window")
        self.add_events(Gdk.EventMask.SCROLL_MASK)
        print("unit-window...")
        self.show_all()

        

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class InfraWindow(Gtk.Window):

    def on_destroy(self, widget):
        self.main_window.infra_window = None
        print("destroy")

    def on_clicked_delete(self, widget): pass

    def on_clicked_next(self, widget):
        # self.info2.set_text("check order...")
        self.main_window.on_press(widget, "i")

    def __init__(self, main_window):
        Gtk.Window.__init__(self, title="infra-window")
        self.connect("destroy", self.on_destroy)
        self.main_window = main_window
        self.control_window = self.main_window.control_window

        self.box = Gtk.VBox(spacing=3)
        self.add(self.box)        


        hbox = Gtk.HBox(spacing=3) 
        self.box.pack_start(hbox, False, True, 0)

        button = Gtk.Button(label="Delete-Build")
        button.connect("clicked", self.on_clicked_delete)
        hbox.pack_start(button, False, True, 0)

        button = Gtk.Button(label="Next-Build")
        button.connect("clicked", self.on_clicked_next)
        hbox.pack_start(button, False, True, 0)

        self.box.pack_start(Gtk.HSeparator(), False, True, 0)
        self.box.pack_start(Gtk.HSeparator(), False, True, 0)
        
        
        self.info = Gtk.Label(label="")
        self.box.pack_start(self.info, False, True, 0)        
        self.selected_infra_view()
        self.info.set_yalign(0.0)

        
        # self.add_events(Gdk.EventMask.SCROLL_MASK)
        print("infra-window...")
        self.show_all()

    def selected_infra_view(self):
        if self.main_window.selected_infra is not None:
            info = "selected infra:"
            hex_xy = self.main_window.selected_infra[:2]
            index = self.main_window.selected_infra[2]
            buildings = self.main_window.saver.infra.get(hex_xy)
            if buildings is not None:
                infra = buildings[index]
                info = f"building ({index}) from {len(buildings)}"
                info += f"\nhex: {hex_xy}"
                info += f"\nowner: {infra['own']}"
                info += f"\ntype: {infra['type']}"
                info += f"\nstate: {round(100*infra['state'])}%"
                if "supply" in infra:
                    info += f"\nsuplly: {infra['supply']}"
                info += "\nstock:"
                for good in sorted(self.main_window.saver.goods.keys()):
                    val = infra["stock"].get(good, 0.0)
                    io = infra["io"].get(good, "off")
                    info += f"\n\t{good} [{io}] - {round(val, 2)}"
        else: info = "No selected infra..."
        self.info.set_text(info)
        return info

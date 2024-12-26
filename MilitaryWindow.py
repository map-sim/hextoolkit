import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class MilitaryWindow(Gtk.Window):

    def on_destroy(self, widget):
        self.main_window.military_window = None
        print("destroy")
    def on_press(self, widget, event):
        if isinstance(event, str): key_name = event
        else: key_name = Gdk.keyval_name(event.keyval)
        if key_name == "v":
            self.main_window.on_press(widget, "v")
        elif key_name == "q":
            self.main_window.on_press(widget, "q")
            self.destroy()
        else:
            print("not supported key:")
            if not isinstance(event, str):
                print("\tkey name:", Gdk.keyval_name(event.keyval))
                print("\tkey value:", event.keyval)
            else: print("\tkey name:", event)
        return True

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
        self.main_window.on_press(widget, "q")
        self.destroy()
        
    def on_clicked_next(self, widget):
        self.main_window.on_press(widget, "v")
    def on_clicked_order(self, widget):
        print("new order...")
        vex = self.main_window.selected_vex
        uid = self.main_window.selected_unit
        if vex is None: return
        if uid is None: return

        order_id = self.combo_order.get_active()
        if order_id == -1: return        
        order = self.order_list[order_id]

        units = self.main_window.saver.military.get(vex)
        if not units: return
        unit = units[uid]

        if "to" in unit: del unit["to"]
        if "from" in unit: del unit["from"]
        if "unit" in unit: del unit["unit"]
        if "progress" in unit: del unit["progress"]

        if order == "defence":
            unit["order"] = order
        else: print("not supported order")

    def __init__(self, main_window):
        Gtk.Window.__init__(self, title="unit-window")
        self.connect("destroy", self.on_destroy)
        self.connect("key-press-event",self.on_press)
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

        button = Gtk.Button(label="Set-Order")
        button.connect("clicked", self.on_clicked_order)
        hbox.pack_start(button, False, True, 0)

        self.box.pack_start(Gtk.HSeparator(), False, True, 0)
        self.box.pack_start(Gtk.HSeparator(), False, True, 0)

        hbox = Gtk.HBox(spacing=3) 
        self.box.pack_start(hbox, False, True, 0)

        self.info = Gtk.Label(label="")
        hbox.pack_start(self.info, False, True, 0)        
        display_data = self.selected_military_view()
        self.info.set_yalign(0.0)

        hbox.pack_start(Gtk.VSeparator(), False, True, 0)
        hbox.pack_start(Gtk.VSeparator(), False, True, 0)
        vbox = Gtk.VBox(spacing=3)
        hbox.pack_start(vbox, False, True, 0)        

        self.order_list = []
        corders = Gtk.ListStore(str)
        for order in sorted(self.main_window.saver.orders):
            corders.append([order]); self.order_list.append(order)
        vbox.pack_start(Gtk.Label(label="order:"), False, True, 0)
        self.combo_order = Gtk.ComboBox.new_with_model(corders)
        vbox.pack_start(self.combo_order, False, True, 0)
        renderer_text = Gtk.CellRendererText()
        self.combo_order.pack_start(renderer_text, True)
        self.combo_order.add_attribute(renderer_text, "text", 0)
        vbox.pack_start(Gtk.HSeparator(), False, True, 0)

        vbox.pack_start(Gtk.Label(label="from:"), False, True, 0)
        self.from_order = Gtk.Entry()
        vbox.pack_start(self.from_order, False, True, 0)
        
        vbox.pack_start(Gtk.Label(label="to:"), False, True, 0)
        self.to_order = Gtk.Entry()
        vbox.pack_start(self.to_order, False, True, 0)

        vbox.pack_start(Gtk.Label(label="unit:"), False, True, 0)
        self.unit_order = Gtk.Entry()
        vbox.pack_start(self.unit_order, False, True, 0)

        vbox.pack_start(Gtk.Label(label="progress:"), False, True, 0)
        self.progress_order = Gtk.Entry()
        vbox.pack_start(self.progress_order, False, True, 0)

        self.set_title(f"unit-window")
        self.add_events(Gdk.EventMask.SCROLL_MASK)
        print("unit-window...")
        self.show_all()

    def selected_military_view(self):
        self.main_window.saver.unmark_all_orders()    
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
                self.main_window.saver.mark_range(unit, vex)
                self.main_window.saver.mark_order(unit, vex)
                self.main_window.draw_content()
            else:  info += "No units to select..."
        else: info += "No selected unit..."
        self.info.set_text(info)
        return info
        
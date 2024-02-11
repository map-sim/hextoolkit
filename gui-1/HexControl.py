import gi, json

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from HexPlotter import HexPlotter

class HexControl(Gtk.Window):
    def on_press(self, widget, event):
        self.main_window.on_press(widget, event)
    def on_scroll(self, widget, event):
        self.main_window.on_scroll(widget, event)
    def on_clicked(self, widget):
        value = self.button_mapping[widget.get_label()]
        self.main_window.on_press(widget, value)
    def make_button(self, vbox, label, value):
        button = Gtk.Button(label=label)
        button.connect("clicked", self.on_clicked)
        self.button_mapping[button.get_label()] = value
        vbox.pack_start(button, False, True, 0)
        return button

    def __init__(self, main_window):
        Gtk.Window.__init__(self, title="Control")
        self.add_events(Gdk.EventMask.SCROLL_MASK)
        self.connect("scroll-event", self.on_scroll)
        self.connect("key-press-event",self.on_press)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.main_window = main_window
        self.button_mapping = {}

        mode = self.main_window.window_mode
        self.set_title(f"control ({mode})")
        
        self.plotter = HexPlotter(main_window.saver)
        self.__control_counter = 0
        self.__tech_counter = 0

        self.box = Gtk.Box(spacing=3)
        self.add(self.box)
        
        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)
        
        self.make_button(vbox, "Reset (ESC)", "Escape")
        self.make_button(vbox, "ZOOM in", "plus")
        self.make_button(vbox, "ZOOM out", "minus")
        self.make_button(vbox, "Move Up", "Up")
        self.make_button(vbox, "Move Down", "Down")
        self.make_button(vbox, "Move --->", "Right")
        self.make_button(vbox, "Move <---", "Left")
        
        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)

        for group in main_window.saver.stats.keys():
            self.button_mapping[f"Plot {group} (p)"] = "p"
        plabel = self.plotter.get_next_label()
        plot_but = self.make_button(vbox, plabel, "p")
        
        self.make_button(vbox, "Mode (tab)", "Tab")
        self.make_button(vbox, "Save (s)", "s")
        self.make_button(vbox, "Tech-Tree (t)", "t")
        self.make_button(vbox, "Control (c)", "c")
        self.make_button(vbox, "Un-Select (q)", "q")
        self.make_button(vbox, "S/H Markers (m)", "m")

        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)

        self.make_button(vbox, "Del Markers (d)", "d")
        self.box.pack_start(Gtk.VSeparator(), False, True, 0)
        
        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)
        if main_window.selected_vex is not None:
            x, y = main_window.selected_vex
            init_info = f"selected hex: {x} {y}"
            init_info += " " * (40 - len(init_info))
            terr = self.main_window.terr_graph.get_hex_terr((x, y))
            init_info += f"\nterrain: {terr}"
        else:  init_info = " " * 40
        self.info = Gtk.Label(label=init_info)
        self.info.set_max_width_chars(40)
        #self.info.set_line_wrap(True)
        self.info.set_yalign(0.0)
        self.info.set_selectable(True)
        vbox.pack_start(self.info, True, True, 3)
        self.plotter.set_controls(plot_but, self.info)
        self.show_all()

    def control_view(self):
        keys = list(self.main_window.saver.controls.keys())
        name = keys[self.__control_counter]
        cc = self.main_window.saver.controls[name]
        #cstr = json.dumps(cc, indent=2)
        bcolor = ", ".join(map(str, cc["base-color"]))
        mcolor = ", ".join(map(str, cc["marker-color"]))
        cnt = f"{self.__control_counter+1}/{len(keys)}"
        cstr = f"{cnt}. {name}:\nb-color: {bcolor}"
        cstr = f"{cstr}\nm-color: {mcolor}"
        ## TODO: more about control
        self.info.set_text(cstr)
        if self.main_window.window_mode == "edit": 
            self.__control_counter += 1
            if self.__control_counter >= len(keys):
                self.__control_counter = 0
    def tech_tree_view(self):
        tech_tree = self.main_window.saver.tech_tree; techstr = ""
        w = self.main_window.saver.settings["tech-batchsize"]
        offset = w * self.__tech_counter
        for n, (k, v) in enumerate(tech_tree.items()):
            if n >= offset + w: continue
            if n < offset: continue
            techstr += f"{k}:\n"
            techstr += f"\tcost: {v['cost']}\n"
            if "need" in v:
                techneed = " | ".join(v["need"])
                techstr += f"\tneed: {techneed}\n"
        self.__tech_counter += 1
        if self.__tech_counter > len(tech_tree) / w:
            self.__tech_counter = 0
        techstr = str(techstr[:-1])
        self.info.set_text(techstr)

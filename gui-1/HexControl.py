import gi, json

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from StatsPlotter import StatsPlotter

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
        self.button_mapping = {}

        self.main_window = main_window
        mode = self.main_window.window_mode
        self.set_title(f"control ({mode})")
        
        self.plotter = StatsPlotter(main_window.saver)
        self.__control_counter = 0
        self.__display_offset = 0
        
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
        self.make_button(vbox, "Exit (E)", "E")
        
        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)

        self.make_button(vbox, "Settings (x)", "x")
        self.make_button(vbox, "Terr-List (r)", "t")
        self.make_button(vbox, "Control (c)", "c")
        self.make_button(vbox, "Unit (u)", "u")
        self.make_button(vbox, "Infra (i)", "i")
        self.make_button(vbox, "Area Control (a)", "a")
        self.make_button(vbox, "Un-Select (q)", "q")
        self.make_button(vbox, "S/H Markers (m)", "m")

        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)

        for group in main_window.saver.stats.keys():
            self.button_mapping[f"Plot {group} (p)"] = "p"
        plabel = self.plotter.get_next_label()
        plot_but = self.make_button(vbox, plabel, "p")        
        self.make_button(vbox, "Save (s)", "s")
        self.make_button(vbox, "Next turn (n)", "n")
        self.make_button(vbox, "Mode (tab)", "Tab")
        self.make_button(vbox, "Remove Hex (R)", "R")
        self.make_button(vbox, "Change Terrain (T)", "T")
        self.make_button(vbox, "Terrain Dilation (D)", "D")
        self.make_button(vbox, "Toogle Infra Own (O)", "O")
        self.box.pack_start(Gtk.VSeparator(), False, True, 0)

        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)

        self.make_button(vbox, "<<", "Page_Up")
        self.make_button(vbox, "<", "comma")
        self.make_button(vbox, ">", "period")
        self.make_button(vbox, ">>", "Page_Down")
        self.box.pack_start(Gtk.VSeparator(), False, True, 0)
        
        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)

        self.display_content = self.get_init_info()
        display_data = self.get_display_data()        
        self.info = Gtk.Label(label=display_data)
        # self.info.set_max_width_chars(1000)
        self.info.set_yalign(0.0)
        self.info.set_selectable(True)
        vbox.pack_start(self.info, True, True, 3)
        self.plotter.set_controls(plot_but, self.info)

        self.welcome_view()
        self.show_all()

    def forward_display(self):
        w = self.main_window.saver.settings["display-length"]
        n = self.display_content.count("\n")
        if self.__display_offset + w < n: 
            self.__display_offset += 1
        display_data = self.get_display_data()
        self.info.set_text(display_data)        
    def backward_display(self):
        if self.__display_offset > 0: 
            self.__display_offset -= 1
        display_data = self.get_display_data()
        self.info.set_text(display_data)

    def down_display(self):
        w = self.main_window.saver.settings["display-length"]
        n = self.display_content.count("\n")
        if n <= w:
            self.__display_offset = 0
        elif self.__display_offset + w + w < n: 
            self.__display_offset += w
        else: self.__display_offset = n - w 
        display_data = self.get_display_data()
        self.info.set_text(display_data)        
    def up_display(self):
        w = self.main_window.saver.settings["display-length"]
        n = self.display_content.count("\n")
        if n <= w:
            self.__display_offset = 0
        elif self.__display_offset > w:
            self.__display_offset -= w
        else: self.__display_offset = 0
        display_data = self.get_display_data()
        self.info.set_text(display_data)

    def get_display_data(self):
        w = self.main_window.saver.settings["display-length"]
        lines = self.display_content.split("\n")
        o = self.__display_offset
        e = self.__display_offset + w
        if e + 1 >= len(lines):
            e = len(lines)
            return "\n".join(lines[o:e])
        else: return "\n".join(lines[o:e]) + "\n..."

    def get_init_info(self):
        if self.main_window.selected_vex is not None:
            x, y = self.main_window.selected_vex
            init_info = f"selected hex: ({x}, {y})"
            init_info += " " * (40 - len(init_info))
            terr = self.main_window.terr_graph.get_hex_terr((x, y))
            return init_info + f"\nterrain: {terr}"
        else: return " " * 40

    def selected_hex_view(self, hex_xy, hex_terr):
        info = f"selected hex: ({hex_xy[0]}, {hex_xy[1]})"
        info += f"\nterrain: {hex_terr}"
        infra = self.main_window.saver.infra.get(hex_xy, [])
        if infra: info += "\ninfrastructure:"
        for i, item in enumerate(infra):
            it = f"{item['type']} ({item['own']})"
            it += f" --> {100 * round(item['state'], 1)}%"
            info += f"\n {i}. {it}"
        units = self.main_window.saver.military.get(hex_xy, [])
        if units: info += "\nunits:"
        for i, item in enumerate(units):
            if item['type'] == "motorized": t = "motor"
            elif item['type'] == "mechanized": t = "mech"
            elif item['type'] == "supplying": t = "supp"
            else: t = item['type']
            it = f"{t}-{item['size']} ({item['own']})"
            it += f" --> {100 * round(item['state'], 1)}"
            it += f" / {100 * round(item['stock'][0], 1)}"
            it += f" / {100 * round(item['stock'][1], 1)}%"
            info += f"\n {i}. {it}"            
        self.info.set_text(info)

    def selected_unit_view(self):
        if self.main_window.selected_unit is not None:
            info = "selected unit:"
            hex_xy = self.main_window.selected_vex
            index = self.main_window.selected_unit
            units = self.main_window.saver.military.get(hex_xy)
            if units is not None:
                unit = units[index]
                info = f"unit ({index}) from {len(units)}"
                info += f"\nhex: {hex_xy}"
                info += f"\nowner: {unit['own']}"
                info += f"\ntype: {unit['type']}"
                info += f"\nsize: {unit['size']}"
                info += f"\nstate: {round(100*unit['state'], 2)}%"
                info += f"\nstock 1: {round(100*unit['stock'][0], 2)}%"
                info += f"\nstock 2: {round(100*unit['stock'][1], 2)}%"
                info += f"\norder: {unit['order']}"
                if "source" in unit:
                    source = " > ".join(map(str, unit['source']))
                    info += f"\nsource: {source}"
                if "target" in unit:
                    if isinstance(unit['target'], list):
                        target = " > ".join(map(str, unit['target']))
                    else: target = str(unit['target'])
                    info += f"\ntarget: {target}"
            else:  info = "No units to select..."
        else: info = "No selected unit..."
        self.info.set_text(info)
    def selected_infra_view(self):
        if self.main_window.selected_infra is not None:
            info = "selected infra:"
            hex_xy = self.main_window.selected_vex
            index = self.main_window.selected_infra
            buildings = self.main_window.saver.infra.get(hex_xy)
            if buildings is not None:
                infra = buildings[index]
                info = f"building ({index}) from {len(buildings)}"
                info += f"\nhex: {hex_xy}"
                info += f"\nowner: {infra['own']}"
                info += f"\ntype: {infra['type']}"
                info += f"\nstate: {round(100*infra['state'], 1)}%"
        else: info = "No selected infra..."
        self.info.set_text(info)

    def settings_view(self):
        self.__display_offset = 0
        setstr = "settings:\n" + "-" * 40 + "\n"
        for p, v in self.main_window.saver.settings.items():
            setstr += f"{p}: {v}\n"
        setstr += "-" * 40 + "\n"
        for i, data in self.main_window.saver.builds.items():
            for k, v in data.items():                
                setstr += f"{i}.{k}: {v}\n"
        setstr += "-" * 40 + "\n"
        for u, data in self.main_window.saver.units.items():
            for k, vs in data.items():
                if vs is None: vs = "-"
                if not isinstance(vs, (int, float, str)):
                    for p, v in vs.items():
                        setstr += f"{u}.{k}.{p}: {v}\n"
                else: setstr += f"{u}.{k}: {vs}\n"
        setstr += "-" * 40 + "\n"
        for u, data in self.main_window.saver.xsystem.items():
            for k, v in data.items():
                setstr += f"{u}.{k}: {v}\n"                
        self.display_content = setstr
        display_data = self.get_display_data()
        self.info.set_text(display_data)
        
    def terrains_view(self):
        self.__display_offset = 0
        terrstr = "terr-list:\n" + "-" * 40 + "\n"
        terr_list = self.main_window.saver.terrains
        for n, (k, v) in enumerate(terr_list.items()):
            info = "\n\tSlots " + str(v["slots"])
            if v["navigable"]: info += "\n\t+Navigable"
            if v["buildable"]: info += "\n\t+Buildable"
            info += "\n\tMobile " + str(v["mobile"])            
            terrstr += f"{n+1}. {k} {info} \n"
        self.display_content = terrstr
        display_data = self.get_display_data()
        self.info.set_text(display_data)
        
    def control_view(self):
        self.__display_offset = 0
        keys = list(self.main_window.saver.controls.keys())
        name = keys[self.__control_counter]

        cc = self.main_window.saver.controls[name]
        bcolor = ", ".join(map(str, cc["base-color"]))
        mcolor = ", ".join(map(str, cc["marker-color"]))
        ucolor = ", ".join(map(str, cc["unit-color"]))
        nstr = name + ":" + " " * (40 - len(name))
        cstr = f"{nstr}\n{'-' * 40}"
        pop = cc["population"]
        cstr = f"{cstr}\npopulation: {pop}"
        cstr = f"{cstr}\nb-color: {bcolor}"
        cstr = f"{cstr}\nm-color: {mcolor}"
        cstr = f"{cstr}\nu-color: {ucolor}"
        cstr = f"{cstr}\n{'-' * 40}"
        u = 0; i = 0; s = 0
        for units in self.main_window.saver.military.values():
            for unit in units:
                if unit["own"] == name: u += 1; s += unit["size"]
        cstr = f"{cstr}\nunits: {u}\narmy: {s}"
        for infra in self.main_window.saver.infra.values():
            for build in infra:
                if build["own"] == name: i += 1
        cstr = f"{cstr}\ninfra: {i}"
        self.display_content = cstr
        display_data = self.get_display_data()
        self.info.set_text(display_data)

        self.__control_counter += 1
        n = len(self.main_window.saver.controls)
        if self.__control_counter >= n:
            self.__control_counter = 0
        return name

    def welcome_view(self):
        self.__display_offset = 0
        content = "------------------------------"
        content += "-----------------------------"
        content += "\nWELCOME !!!" * 20
        self.display_content = content
        display_data = self.get_display_data()
        self.info.set_text(display_data)
        

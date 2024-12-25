import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from StatsPlotter import StatsPlotter

def as_str(vs):
    out = []
    for v in vs:
        if isinstance(v, (list, tuple)):
            out.append("-".join(map(str, v)))
        else: out.append(str(v))
    return out

class ControlWindow(Gtk.Window):
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
        self.connect("destroy", Gtk.main_quit)
        self.set_position(Gtk.WindowPosition.NONE)
        self.button_mapping = {}

        self.main_window = main_window
        mode = self.main_window.window_mode
        self.set_title(f"control ({mode})")
        
        self.plotter = StatsPlotter(main_window.saver)
        self.__control_counter = 0
        self.__display_offset = 0
        self.__unit_counter = 0
        
        self.box = Gtk.Box(spacing=3)
        self.add(self.box)
        
        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)
        
        self.make_button(vbox, "Reset - ESC", "Escape")
        self.make_button(vbox, "ZOOM in", "plus")
        self.make_button(vbox, "ZOOM out", "minus")
        self.make_button(vbox, "Move Up", "Up")
        self.make_button(vbox, "Move Down", "Down")
        self.make_button(vbox, "Move --->", "Right")
        self.make_button(vbox, "Move <---", "Left")
        self.make_button(vbox, "Exit - E", "E")
        self.make_button(vbox, "Save - S", "S")
        self.make_button(vbox, "S/H Markers - M", "M")
        for group in main_window.saver.stats.keys():
            self.button_mapping[f"Plot {group} - p"] = "p"
        plabel = self.plotter.get_next_label()
        plot_but = self.make_button(vbox, plabel, "p")        
        
        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)

        self.make_button(vbox, "Settings - x", "x")
        self.make_button(vbox, "List-Terrs - t", "t")
        self.make_button(vbox, "List-Goods - g", "g")
        self.make_button(vbox, "List-Builds - b", "b")
        self.make_button(vbox, "List-Orders - o", "o")
        self.make_button(vbox, "Switch-Unit - u", "u")
        self.make_button(vbox, "Switch-Control - c", "c")
        self.make_button(vbox, "Select-Unit - v", "v")
        self.make_button(vbox, "Select-Infra - i", "i")
        self.make_button(vbox, "Area Control - a", "a")
        self.make_button(vbox, "Un-Select - q", "q")

        vbox = Gtk.VBox(spacing=3)
        self.box.pack_start(vbox, False, True, 0)
        vbox.pack_start(Gtk.Separator(), False, True, 0)

        self.make_button(vbox, "Next turn (n)", "n")
        self.make_button(vbox, "Mode - TAB", "Tab")
        self.make_button(vbox, "Remove Hex - R", "R")
        self.make_button(vbox, "Change Terrain - T", "T")
        self.make_button(vbox, "Terrain Dilation - D", "D")
        self.make_button(vbox, "Toogle Infra Own - O", "O")
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
            if item is None: continue
            it = f"{item['type']} ({item['own']})"
            it += f" --> {round(100 * item['state'])}%"
            info += f"\n {i}. {it}"
        units = self.main_window.saver.military.get(hex_xy, [])
        if units: info += "\nunits:"
        for i, item in enumerate(units):
            if item['type'] == "motorized": t = "motor"
            elif item['type'] == "mechanized": t = "mech"
            elif item['type'] == "supplying": t = "supp"
            elif item['type'] == "helicopter": t = "h-copter"
            elif item['type'] == "engineering": t = "eng"
            elif item['type'] == "artillery": t = "art"
            elif item['type'] == "armored": t = "armor"
            elif item['type'] == "special": t = "spec"
            elif item['type'] == "cutter": t = "cut"
            else: t = item['type']
            o = item['order'][:5]
            it = f"{t}-{item['size']} ({item['own']}; {o})"
            it += f" %-> {round(100 * item['state'])}"
            it += f" / {round(100 * item['stock'][0])}"
            it += f" / {round(100 * item['stock'][1])}"
            info += f"\n {i}. {it}"            
        self.info.set_text(info)

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
    
    def settings_view(self):
        self.__display_offset = 0
        setstr = "settings:\n" + "-" * 40 + "\n"
        for p, v in self.main_window.saver.settings.items():
            setstr += f"{p}: {v}\n"
        setstr += "-" * 40 + "\nxsystem:\n" + "-" * 40 + "\n"
        for u, data in self.main_window.saver.xsystem.items():
            for k, v in data.items():
                setstr += f"{u}.{k}: {v}\n"                
            setstr += "-" * 40 + "\n"
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
            if v["costal"]: info += "\n\t+Costal"
            info += "\n\tMobile " + str(v["mobile"])            
            terrstr += f"{n+1}. {k} {info} \n"
        self.display_content = terrstr
        display_data = self.get_display_data()
        self.info.set_text(display_data)
    def goods_view(self):
        self.__display_offset = 0
        goodstr = "good-list:\n" + "-" * 40 + "\n"
        good_list = self.main_window.saver.goods
        for n, (k, v) in enumerate(good_list.items()):
            goodstr += f"{n+1}. {k}:\n"
            goodstr += f"\ttype: {v['type']}\n"
            goodstr += f"\tdrag: {v['drag']}\n"
        self.display_content = goodstr
        display_data = self.get_display_data()
        self.info.set_text(display_data)
    def orders_view(self):
        self.__display_offset = 0
        orderstr = "order-list:\n" + "-" * 40 + "\n"
        order_list = self.main_window.saver.orders
        for n, (k, vs) in enumerate(order_list.items()):
            orderstr += f"{n+1}. {k}:\n"
            orderstr += f"\t{', '.join(as_str(vs))}\n"
        self.display_content = orderstr
        display_data = self.get_display_data()
        self.info.set_text(display_data)
    def builds_view(self):
        self.__display_offset = 0
        buildstr = "build-list:\n" + "-" * 40 + "\n"
        build_list = self.main_window.saver.builds
        for n, (k, v) in enumerate(build_list.items()):
            buildstr += f"{n+1}. {k}:\n"
            buildstr += f"\tcost: {v['cost']}\n"
            buildstr += f"\tstrength: {v['strength']}\n"
            buildstr += f"\tpower: {v['power']}\n"
            if "no-power" in v:
                buildstr += f"\tno-power: {v['no-power']}\n"
            if "terrains" in v:
                et = ', '.join(v['terrains'])
                buildstr += f"\t+terrains: {et}\n"
        self.display_content = buildstr
        display_data = self.get_display_data()
        self.info.set_text(display_data)

    def unit_view(self):
        self.__display_offset = 0
        keys = list(sorted(self.main_window.saver.units.keys()))
        name = keys[self.__unit_counter]

        cc = self.main_window.saver.units[name]
        nstr = f"{name}:" + " " * (40 - len(name))
        cstr = f"{nstr}\n{'-' * 40}"
        for k, v in reversed(sorted(cc.items())):
            if k in ("action-cost", "action-perf"):
                cstr += f"\n{k}:"
                for kk, vv in sorted(v.items()):
                    if isinstance(vv, (list, tuple)):
                        vs = ", ".join(map(str, vv))
                        cstr += f"\n\t{kk}: {vs}"
                    else: cstr += f"\n\t{kk}: {vv}"
            else: cstr += f"\n{k}: {v}"
        self.display_content = cstr
        display_data = self.get_display_data()
        self.info.set_text(display_data)

        self.__unit_counter += 1
        n = len(self.main_window.saver.units)
        if self.__unit_counter >= n:
            self.__unit_counter = 0
        return name

    def control_view(self):
        self.__display_offset = 0
        keys = list(sorted(self.main_window.saver.controls.keys()))
        name = keys[self.__control_counter]

        cc = self.main_window.saver.controls[name]
        bcolor = ", ".join(map(str, cc["base-color"]))
        mcolor = ", ".join(map(str, cc["marker-color"]))
        ucolor = ", ".join(map(str, cc["unit-color"]))
        nstr = f"{name}:" + " " * (40 - len(name))
        cstr = f"{nstr}\n{'-' * 40}"
        pop = cc["population"]
        cstr = f"{cstr}\npopulation: {pop}"
        cstr = f"{cstr}\nb-color: {bcolor}"
        cstr = f"{cstr}\nm-color: {mcolor}"
        cstr = f"{cstr}\nu-color: {ucolor}"
        cstr = f"{cstr}\n{'-' * 40}"
        u = 0; i = 0; s = 0; sf = 0
        for units in self.main_window.saver.military.values():
            for unit in units:
                if unit["own"] == name: u += 1; s += unit["size"]
                if unit["own"] == name: sf += unit["size"] * unit["state"]
        cstr = f"{cstr}\nunits: {u}\narmy: {s}\nfiling: {round(100*sf/s)}%"
        for infra in self.main_window.saver.infra.values():
            for build in infra:
                if build is None: continue
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
        content = "WELCOME !!!\n"        
        content += 60 * "-" + "\n"
        content += f"project: Hex ToolKit\n"
        content += f"version: {self.main_window.saver.settings['version']}\n"
        content += "-----------------------------\n"
        ncontrols = len(self.main_window.saver.controls)
        cturn = self.main_window.saver.settings['current-turn']
        content += f"controls: {ncontrols}\n"
        content += f"current turn: {cturn}\n"
        self.display_content = content
        display_data = self.get_display_data()
        self.info.set_text(display_data)
        

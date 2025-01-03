#!/usr/bin/python3

import gi, copy

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

from BaseWindow import BaseWindow
from NaviWindow import NaviWindow
from TerrToolbox import TerrPainter
from TerrToolbox import TerrGraph
from NextTurn import NextTurn

from MilitaryWindow import MilitaryWindow
from InfraWindow import InfraWindow

from ObjPainter import ObjPainter
from UnitPainter import UnitPainter
from InfraPainter import InfraPainter


class HexWindow(NaviWindow):
    window_modes = ["view", "edit"]
    def __init__(self, saver):
        self.terr_graph = TerrGraph(saver)
        self.obj_painter = ObjPainter(self, saver)
        self.unit_painter = UnitPainter(self, saver)
        self.terr_painter = TerrPainter(self, saver)
        self.infra_painter = InfraPainter(self, saver)
        self.settings_backup = copy.deepcopy(saver.settings)

        self.saver = saver
        self.settings = saver.settings
        NextTurn(self.saver).init_stats()
        vex = saver.get_selected_vex()
        if vex is None: self.selected_vex = vex
        else: self.selected_vex = tuple(vex)
        self.selected_infra = None
        self.selected_unit = None
        self.selected_own = None
        self.military_window = None
        self.infra_window = None
        self.hex_buffer = []

        size = self.settings["window-size"]
        title = self.settings["window-title"]
        BaseWindow.__init__(self, title, *size)
        self.connect("destroy", Gtk.main_quit)
        self.window_mode = self.window_modes[0]
        title = f"main ({self.window_mode})"
        print(f"Start main window: {title}")
        self.set_title(title)

    @BaseWindow.double_buffering
    def draw_content(self, context):
        self.terr_painter.draw(context)
        self.infra_painter.draw(context)
        self.unit_painter.draw(context)
        self.obj_painter.draw(context)
        context.stroke()

    def get_click_location(self, event):
        xoffset, yoffset = self.settings["window-offset"]
        zoom = self.settings["window-zoom"]
        ox = (int(event.x) - xoffset) / zoom
        oy = (int(event.y) - yoffset) / zoom
        return ox, oy
    def on_click(self, widget, event):
        ox, oy = self.get_click_location(event)
        rox, roy = round(ox, 2), round(oy, 2)
        print("----")
        if event.button == 1:
            print(f"oriented-location: ({rox}, {roy})")
            hex_index_xy, _ = self.terr_graph.transform_to_vex(ox, oy)
            if self.window_mode == "edit":
                info = f"add => {hex_index_xy[0]},{hex_index_xy[1]} to\n"
                for n, vex in enumerate(self.hex_buffer):
                    info += f" => {vex[0]},{vex[1]}"
                    if n % 4 == 3: info += "\n"
                self.control_window.info.set_text(info)
                self.hex_buffer.append(hex_index_xy)
            else: self.select_infra(hex_index_xy)
        elif event.button == 3:
            terr, terr_obj = self.terr_graph.check_terrain(ox, oy)
            hex_index_xy, _ = self.terr_graph.transform_to_vex(ox, oy)
            hex_terr = self.terr_graph.get_hex_terr(hex_index_xy)            
            print(f"landform-terrain: {terr}")
            print(f"landform-object: {terr_obj}")
            print(f"hex-location: {hex_index_xy}")
            print(f"hex-terrain: {hex_terr}")
            if self.selected_vex != tuple(hex_index_xy):
                self.unselect_all(infra=False)
                self.selected_vex = tuple(hex_index_xy)
                self.saver.mark_only_one_vex(hex_index_xy)
                self.control_window.selected_hex_view(hex_index_xy, hex_terr)
                if self.saver.settings["show-markers"]:
                    self.saver.orders_to_markers(self.selected_vex, self.selected_own)
            else:
                self.saver.unmark_all_vexes()
                self.unselect_all(infra=False)
            self.draw_content()
        return True

    def reset_vex(self, vex):
        if vex in self.saver.infra:
            del self.saver.infra[vex]
        if vex in self.saver.military:
            del self.saver.military[vex]
        self.saver.remove_markers(vex)

    def set_vex_terrain(self, vex, terr):
        if vex in self.terr_graph.vex_dict:
            for i, item in enumerate(self.saver.landform):
                if item[0] == "vex" and tuple(item[2]) == vex:
                    self.saver.landform[i] = "vex", terr, vex
                    self.terr_graph.vex_dict[vex] = terr
                    break
        else:
            for i, item in enumerate(self.saver.landform):
                if item[0] == "grid": break
            self.saver.landform.insert(i, ("vex", terr, vex))
            self.terr_graph.vex_dict[vex] = terr
        self.reset_vex(vex)

    def unselect_all(self, infra=True):
        self.selected_own = None
        if infra:
            self.selected_infra = None
        self.selected_unit = None
        self.selected_vex = None
        if self.military_window is not None:
            self.military_window.destroy()
        if infra:
            if self.infra_window is not None:
                self.infra_window.destroy()
            
    def on_press(self, widget, event):
        if isinstance(event, str): key_name = event
        else: key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Tab":
            print(f"##> change mode from {self.window_mode}", end="")
            m = self.window_modes.index(self.window_mode)
            m = m + 1 if m < len(self.window_modes) - 1 else 0
            self.window_mode = self.window_modes[m]
            self.set_title(f"main-window ({self.window_mode})")
            self.control_window.set_title(f"control ({self.window_mode})")
            print(f" to { self.window_mode}")
        elif key_name == "E":
            print("##> exit")
            b = self.settings_backup["current-turn"]
            if self.settings["current-turn"] - b > 0:
                dir_name = self.saver.save_on_drive()
                print(f"save on drive in {dir_name}")
            Gtk.main_quit()
        elif key_name == "q":
            print("##> unselect vexes & redraw")
            self.control_window.info.set_text("")
            self.saver.settings["show-markers"] = False
            self.saver.unmark_all()
            self.unselect_all()
            self.draw_content()
        elif key_name == "M":
            print("##> show / hide markers")
            self.saver.orders_to_markers(self.selected_vex, self.selected_own)
            state = not self.saver.settings["show-markers"]
            self.saver.settings["show-markers"] = state
            self.draw_content()
        elif key_name == "a":
            print("##> area control markers")
            self.saver.unmark_all()
            self.unselect_all()
            
            out = self.saver.area_control_markers()
            self.control_window.info.set_text(out)
            self.control_window.display_content = out
            self.draw_content()
        elif key_name == "R":
            print("##> remove hex control (try to)")
            if self.window_mode == "edit" and self.selected_vex is not None:
                self.saver.remove_markers(self.selected_vex)
                if self.selected_vex in self.saver.military:
                    del self.saver.military[self.selected_vex]
                if self.selected_vex in self.saver.infra:
                    del self.saver.infra[self.selected_vex]                    
                self.draw_content()
            elif self.window_mode != "edit":
                print("No edit mode!")
            elif self.selected_vex is None:
                print("No selexted hex!")
        elif key_name == "T":
            print("##> change terrain (try to)")
            if self.window_mode == "edit" and self.selected_vex is not None:
                terr = self.terr_graph.get_hex_terr(self.selected_vex)
                terr_list = list(sorted(self.saver.terrains.keys()))
                it = terr_list.index(terr) + 1
                if it >= len(terr_list): it = 0
                new_terr = terr_list[it]
                self.set_vex_terrain(self.selected_vex, new_terr)
                self.draw_content(); print(new_terr)
            elif self.window_mode != "edit":
                print("No edit mode!")
            elif self.selected_vex is None:
                print("No selexted hex!")                
        elif key_name == "D":
            print("##> dilation (try to)")
            if self.window_mode == "edit" and self.selected_vex is not None:
                terr = self.terr_graph.get_hex_terr(self.selected_vex)
                selected_vexes = set()
                for item in self.saver.landform:
                    if item[0] == "vex" and item[1] == terr:
                        selected_vexes.add(item[2])
                total = len(selected_vexes)
                print(f"selected vexes: {total}")
                for vex in selected_vexes:
                    self.set_vex_terrain((vex[0]-1, vex[1]), terr)
                    self.set_vex_terrain((vex[0]+1, vex[1]), terr)
                    self.set_vex_terrain((vex[0], vex[1]+1), terr)
                    self.set_vex_terrain((vex[0], vex[1]-1), terr)
                    if vex[1] % 2:
                        self.set_vex_terrain((vex[0]+1, vex[1]+1), terr)
                        self.set_vex_terrain((vex[0]+1, vex[1]-1), terr)
                    else:
                        self.set_vex_terrain((vex[0]-1, vex[1]+1), terr)
                        self.set_vex_terrain((vex[0]-1, vex[1]-1), terr)
                self.draw_content()
            elif self.window_mode != "edit":
                print("No edit mode!")
            elif self.selected_vex is None:
                print("No selexted hex!")
        elif key_name == "O":
            if self.window_mode == "edit" and self.selected_infra is not None:
                vex = self.selected_infra[0], self.selected_infra[1]
                infra = self.saver.infra[vex][self.selected_infra[2]]
                n = list(sorted(self.saver.controls.keys())).index(infra["own"])
                n = (n+1) % len(self.saver.controls)
                infra["own"] = list(sorted(self.saver.controls.keys()))[n]
                self.draw_content()
            elif self.window_mode != "edit":
                print("No edit mode!")
            elif self.selected_infra is None:
                print("No selexted infra!")
        elif key_name == "S":
            print("##> save on drive ... ", end="")
            dir_name = self.saver.save_on_drive()
            info = f"save on drive in {dir_name}"
            self.control_window.info.set_text(info)
            print(dir_name)
        elif key_name == "period":
            self.control_window.forward_display()
        elif key_name == "comma":
            self.control_window.backward_display()
        elif key_name == "Page_Up":
            self.control_window.up_display()
        elif key_name == "Page_Down":
            self.control_window.down_display()
        elif key_name == "t":
            print("##> show terr list")
            self.control_window.terrains_view()
        elif key_name == "b":
            print("##> show build list")
            self.control_window.builds_view()
        elif key_name == "o":
            print("##> show order list")
            self.control_window.orders_view()
        elif key_name == "g":
            print("##> show stocks/googs list")
            self.control_window.goods_view()
        elif key_name == "x":
            print("##> show settings")
            self.control_window.settings_view()
        elif key_name == "u":
            print("##> show unit def")
            owner = self.control_window.unit_view()
        elif key_name == "c":
            print("##> show control def")
            owner = self.control_window.control_view()
            self.saver.unmark_all()
            self.unselect_all()
            self.selected_own = owner
            self.saver.area_control_markers(owner)
            self.saver.orders_to_markers(self.selected_vex, self.selected_own)
            self.draw_content()
        elif key_name == "p":
            print("##> show stat plot")
            if self.settings["current-turn"]:
                self.control_window.plotter.plot()
            else: print("no data to plot")
        elif key_name == "v":
            print("##> show/select next unit")
            if self.selected_vex is None:
                self.control_window.info.set_text("no selection...")
                print("no selection...")
                return True            
            units = self.saver.military.get(self.selected_vex)
            if units is None:
                self.control_window.info.set_text("no units...")
                print("no units...")
                return True
            self.saver.settings["show-markers"] = True
            if self.selected_unit is not None:
                i = (self.selected_unit + 1) % len(units)
                self.selected_unit = i                
            else: self.selected_unit = 0
            if self.military_window is None:
                if self.selected_unit is not None:                    
                    self.military_window = MilitaryWindow(self)
                else: print(" ... no military selected")
            else: self.military_window.selected_military_view()
            out = "select military... "
            out += f"\nhex ... {self.selected_vex}"
            out += f"\nunit ... {self.selected_unit}"            
            self.control_window.info.set_text(out)
        elif key_name == "i":
            print("##> show/select next infra")
            if self.selected_vex is None:
                self.control_window.info.set_text("no selection...")
                print("no selection..."); return True
            self.select_infra(self.selected_vex)
            out = "select infra... "
            out += f"\nhex ... {self.selected_vex}"
            out += f"\ninfra ... {self.selected_infra}"            
            self.control_window.info.set_text(out)
        elif key_name == "j":
            print("##> show selected infra")
            if self.infra_window is None:
                self.infra_window = InfraWindow(self)
            self.infra_window.selected_infra_view()

        elif key_name == "n":
            print("##> next turn")
            text = NextTurn(self.saver).execute()
            self.control_window.info.set_text(text)
        elif key_name == "Escape":
            NaviWindow.on_press(self, widget, event)
            self.control_window.welcome_view()
        elif key_name == "B":
            length = len(self.hex_buffer)
            info = f"BUFFER ({length}):\n"
            for n, vex in enumerate(self.hex_buffer):
                info += f" => {vex[0]},{vex[1]}"
                if n % 4 == 3: info += "\n"
            if length == 0: info += "buffer is empty"
            self.control_window.info.set_text(info)
        elif key_name == "C":
            length = len(self.hex_buffer)
            info = f"BUFFER ({length}):\n"
            info += "clear buffer..."
            self.hex_buffer = []
            self.control_window.info.set_text(info)
        else: NaviWindow.on_press(self, widget, event)
        return True

    def select_infra(self, hex_xy):
        print("##> show/select next infra")
        if self.selected_infra is not None:
            vex = self.selected_infra[0], self.selected_infra[1]
            if hex_xy != vex: self.selected_infra = None
        infra = self.saver.infra.get(hex_xy)
        if infra is None or len(infra) == 0:
            self.control_window.info.set_text("no infra...")
            # self.selected_infra = None
            for n, marker in reversed(list(enumerate(self.saver.markers))):
                if marker[0] == "inf": del self.saver.markers[n]
            #self.draw_content()
            #print("no infra..."); return True
            
        if self.selected_infra is not None:
            i = (self.selected_infra[2] + 1) % 6
            self.selected_infra = *hex_xy, i
            #while infra[self.selected_infra[2]] is None:
            #    i = (i + 1) % len(infra)
            #    self.selected_infra = *hex_xy, i
        else: self.selected_infra = *hex_xy, 0

        if self.infra_window is None:
            self.infra_window = InfraWindow(self)
        self.infra_window.selected_infra_view()
        
        for n, marker in reversed(list(enumerate(self.saver.markers))):
            if marker[0] == "inf": del self.saver.markers[n]
        marker = ["inf", None, self.selected_infra]
        self.saver.markers.append(marker)
        self.draw_content()
    
def run_example():
    import sys
    from SaveHandler import SaveHandler
    from ControlWindow import ControlWindow

    saver = SaveHandler()
    if len(sys.argv) == 1: saver.load_demo_0()
    else: saver.load_from_drive(sys.argv[1])
    win = HexWindow(saver)
    win.control_window = ControlWindow(win)

    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()

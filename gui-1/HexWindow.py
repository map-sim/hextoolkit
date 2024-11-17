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

from ObjPainter import ObjPainter
from UnitPainter import UnitPainter
from InfraPainter import InfraPainter

class HexWindow(NaviWindow):
    window_modes = ["view", "edit"]
    def __init__(self, saver):
        self.terr_graph = TerrGraph(saver)
        self.obj_painter = ObjPainter(saver)
        self.terr_painter = TerrPainter(saver)
        self.unit_painter = UnitPainter(saver)
        self.infra_painter = InfraPainter(saver)
        self.settings_backup = copy.deepcopy(saver.settings)

        self.saver = saver
        self.settings = saver.settings        
        self.selected_vex = tuple(saver.get_selected_vex())

        size = self.settings["window-size"]
        title = self.settings["window-title"]
        BaseWindow.__init__(self, title, *size)
        self.window_mode = self.window_modes[0]
        self.set_title(f"main-window ({self.window_mode})")

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
        elif event.button == 3:
            terr, terr_obj = self.terr_graph.check_terrain(ox, oy)
            hex_xyi, hex_xyo = self.terr_graph.transform_to_vex(ox, oy)
            hex_terr = self.terr_graph.get_hex_terr(hex_xyi)            
            print(f"landform-terrain: {terr}")
            print(f"landform-object: {terr_obj}")
            print(f"hex-location: {hex_xyi}")
            print(f"hex-terrain: {hex_terr}")

            ## hex selection
            self.selected_vex = tuple(hex_xyi)
            self.saver.select_only_one_vex(hex_xyi)
            if hex_xyi is not None:
                info = f"selected hex: {hex_xyi[0]} {hex_xyi[1]}"
                info += f"\nterrain: {terr}"
                self.control_panel.info.set_text(info)
            self.draw_content()
        return True

    def reset_vex(self, vex):
        if vex in self.saver.infra:
            del self.saver.infra[vex]
        if vex in self.saver.units:
            del self.saver.units[vex]
        self.saver.remove_links(vex)
        self.saver.remove_vectors(vex)
        self.saver.remove_dashes(vex)

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

    def on_press(self, widget, event):
        if isinstance(event, str): key_name = event
        else: key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Tab":
            print("##> change mode from", self.window_mode, end="")
            m = self.window_modes.index(self.window_mode)
            m = m + 1 if m < len(self.window_modes) - 1 else 0
            self.window_mode = self.window_modes[m]
            self.set_title(f"main-window ({self.window_mode})")
            self.control_panel.set_title(f"control ({self.window_mode})")
            print("to", self.window_mode)
        elif key_name == "q":
            print("##> unselect vexes & redraw")
            self.saver.unselect_all_vexes()
            self.control_panel.info.set_text("")
            self.selected_vex = None
            self.draw_content()
        elif key_name == "m":
            print("##> show / hide markers")
            state_l = not self.saver.settings["show-links"]
            state_a = not self.saver.settings["show-arrows"]
            state_d = not self.saver.settings["show-dashes"]
            self.saver.settings["show-links"] = state_l
            self.saver.settings["show-arrows"] = state_a
            self.saver.settings["show-dashes"] = state_d
            self.draw_content()
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
        elif key_name == "d":
            print("##> delete links/vectors (try to)")
            if self.window_mode == "edit":
                if self.selected_vex is not None:
                    self.saver.remove_links(self.selected_vex)
                    self.saver.remove_vectors(self.selected_vex)
                    self.saver.remove_dashes(self.selected_vex)
                    self.draw_content()
            else: print("No edit mode!")
        elif key_name == "s":
            print("##> save on drive ... ", end="")
            dir_name = self.saver.save_on_drive()
            info = f"save on drive in {dir_name}"
            self.control_panel.info.set_text(info)
            print(dir_name)
        elif key_name == "greater" or key_name == "period":
            self.control_panel.forward_display()
        elif key_name == "less" or key_name == "comma":
            self.control_panel.backward_display()
        elif key_name == "t":
            print("##> show terr list")
            self.control_panel.terrains_view()
        elif key_name == "c":
            print("##> show control")
            self.control_panel.control_view()
        elif key_name == "p":
            print("##> show stat plot")
            self.control_panel.plotter.plot()
        else: NaviWindow.on_press(self, widget, event)
        return True

def run_example():
    import sys
    from SaveHandler import SaveHandler
    from HexControl import HexControl

    saver = SaveHandler()
    if len(sys.argv) == 1: saver.load_demo_0()
    else: saver.load_from_drive(sys.argv[1])
    win = HexWindow(saver)
    win.control_panel = HexControl(win)

    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()

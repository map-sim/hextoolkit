#!/usr/bin/python3

import gi, copy
from BaseWindow import BaseWindow
from NaviWindow import NaviWindow
from TerrToolbox import TerrPainter
from TerrToolbox import TerrGraph
from TerrToolbox import ObjPainter

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class HexWindow(NaviWindow):
    def __init__(self, saver):
        self.terr_graph = TerrGraph(saver)
        self.obj_painter = ObjPainter(saver)
        self.terr_painter = TerrPainter(saver)
        self.settings_backup = copy.deepcopy(saver.settings)
        self.selected_vex = saver.get_selected_vex()
        self.settings = saver.settings
        self.saver = saver
        
        size = self.settings["window-size"]
        title = self.settings["window-title"]
        BaseWindow.__init__(self, title, *size)

    @BaseWindow.double_buffering
    def draw_content(self, context):
        self.terr_painter.draw(context)
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
            self.selected_vex = hex_xyi
            self.saver.select_only_one_vex(hex_xyi)
            if hex_xyi is not None:
                info = f"selected hex: {hex_xyi[0]} {hex_xyi[1]}"
                self.control_panel.info.set_text(info)
            self.draw_content()
        return True

    def on_press(self, widget, event):
        if isinstance(event, str): key_name = event
        else: key_name = Gdk.keyval_name(event.keyval)
        if key_name == "q":
            print("##> unselect vexes & redraw")
            self.saver.unselect_all_vexes()
            self.control_panel.info.set_text("")
            self.selected_vex = None
            self.draw_content()
        elif key_name == "s":
            print("##> save on drive ... ", end="")
            print(self.saver.save_on_drive())
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

#!/usr/bin/python3

import gi, copy
from BaseWindow import BaseWindow
from NaviWindow import NaviWindow
from TerrToolbox import TerrPainter
from TerrToolbox import TerrGraph

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class HexWindow(NaviWindow):
    def __init__(self, saver):
        self.settings = copy.deepcopy(saver.settings)
        self.terr_painter = TerrPainter(saver)
        self.terr_graph = TerrGraph(saver)
        self.config = saver.settings
        self.saver = saver

        size = self.settings["window-size"]
        title = self.settings["window-title"]
        BaseWindow.__init__(self, title, *size)

    @BaseWindow.double_buffering
    def draw_content(self, context):
        self.terr_painter.draw(context)
        context.stroke()

    def get_click_location(self, event):
        xoffset, yoffset = self.config["window-offset"]
        zoom = self.config["window-zoom"]
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
        return True
        
def run_example():
    from SaveHandler import SaveHandler
    saver = SaveHandler()
    saver.load_demo_0()
    
    HexWindow(saver)    
    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()

#!/usr/bin/python3

import gi, copy
from BaseWindow import BaseWindow
from NaviWindow import NaviWindow
from TerrPainter import TerrPainter

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class HexWindow(NaviWindow):
    def __init__(self, saver):
        self.settings = copy.deepcopy(saver.settings)
        self.terr_painter = TerrPainter(saver)
        self.config = saver.settings
        self.saver = saver

        size = self.settings["window-size"]
        title = self.settings["window-title"]
        BaseWindow.__init__(self, title, *size)

    @BaseWindow.double_buffering
    def draw_content(self, context):
        self.terr_painter.draw(context)
        context.stroke()

def run_example():
    from SaveHandler import SaveHandler
    saver = SaveHandler()
    saver.load_demo_0()
    
    HexWindow(saver)    
    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()

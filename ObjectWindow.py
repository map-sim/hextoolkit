#!/usr/bin/python3

import gi
from ObjectPainter import ObjectPainter
from BaseWindow import BaseWindow
from TerrWindow import TerrWindow
from TerrWindow import TerrGraph

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ObjectWindow(TerrWindow):
    def __init__(self, config, library, battlefield):
        self.painter = ObjectPainter(config, library, battlefield)
        self.graph = TerrGraph(battlefield)
        
        self.battlefield =  battlefield
        self.library = library
        self.config = config

        title = config["window-title"]
        width, height = config["window-size"]
        BaseWindow.__init__(self, title, width, height)

def run_example():
    example_config = {
        "window-title": "terr-window",
        "window-size": (1800, 820),
        "window-offset": (750, 400),
        "window-zoom": 0.566,
        "move-sensitive": 50
    }

    from MapExamples import library0
    from MapExamples import battlefield0
    from ObjectValidator import validate

    validate(example_config, library0, battlefield0)
    ObjectWindow(example_config, library0, battlefield0)

    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()

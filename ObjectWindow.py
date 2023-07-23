#!/usr/bin/python3

import gi, copy, copy, math
from ObjectPainter import ObjectPainter
from BaseWindow import BaseWindow
from TerrWindow import TerrWindow
from TerrWindow import TerrGraph

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk


class ObjectGraph:    
    def __init__(self, library, battlefield, graph_terr):
        self.terr_graph = graph_terr
        self.battlefield =  battlefield
        self.library = library

    def height_diff(self, xo, yo, xe, ye):
        to, _ = self.terr_graph.check_terrain(xo, yo)
        te, _ = self.terr_graph.check_terrain(xe, ye)
        ho = self.library["terrains"][to]["level"]
        he = self.library["terrains"][te]["level"]
        return ho - he

    def check_objects_connection(self, i1, i2):
        objects = self.battlefield["objects"]
        if i1 == i2: return None, None, None, None
        xo, yo = objects[i1][1], objects[i1][2]
        xe, ye = objects[i2][1], objects[i2][2]
        no, ne = objects[i1][0], objects[i2][0]
        po, pe = objects[i1][3], objects[i2][3]
        do = self.library["objects"][no].get("range", 0)
        if ((no == "store" and ne == "store") or
            (no == "mineshaft" and ne == "store") or
            (no == "store" and ne == "output") or
            (no == "store" and ne == "input") or
            (no == "output" and ne == "store") or
            (no == "input" and ne == "store") or
            (no == "mixer" and ne == "store")):
            ro, re = objects[i1][5], objects[i2][5]
            if ro is None: return None, None, None, None
            if re is None: return None, None, None, None
            if po != pe: return None, None, None, None
            if ro != re: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "input" and ne == "output":
            ro, re = objects[i1][5], objects[i2][5]
            if ro is None: return None, None, None, None
            if re is None: return None, None, None, None
            if ro != re: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)        
        elif no == "store" and ne == "mixer":
            ro, re = objects[i1][5], objects[i2][5]            
            if re is None: return None, None, None, None
            if ro not in self.library["resources"][re]["process"]:
                return None, None, None, None
            if po != pe: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif ((no == "store" and ne == "laboratory") or
              (no == "store" and ne == "barrier") or
              (no == "store" and ne == "developer") or
              (no == "store" and ne == "radiator") or
              (no == "store" and ne == "launcher") or
              (no == "store" and ne == "transmitter")):
            if po != pe: return None, None, None, None
            re = self.library["objects"][ne]["fuel"]
            ro, ze = objects[i1][5], objects[i2][5]
            if ro != re: return None, None, None, None
            if ro is None: return None, None, None, None
            if ze in (None, False): return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "developer" and ne == "repeater":
            if po != pe: return None, None, None, None
            if not objects[i2][5]: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "developer" or no == "repeater" or no == "barrier":
            if po != pe: return None, None, None, None
            if not objects[i1][5]: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "radiator":
            if po == pe: return None, None, None, None
            if not objects[i1][5]: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "launcher":
            te = objects[i1][5]
            if te is None: return None, None, None, None
            if te[0] != xe or te[1] != ye: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        return  None, None, None, None
    
    def find_all_connections(self, index):
        output_connections = []
        length = len(self.battlefield["objects"])
        dfr = self.library["settings"]["base-free-range"]
        hf = self.library["settings"]["base-height-factor"]        
        for i in range(length):
            distance, h, xyo, xye = self.check_objects_connection(index, i)
            if distance is None: continue
            free_range = dfr + h * hf
            row = xyo, xye, distance, free_range
            output_connections.append(row)
        return output_connections

class ObjectWindow(TerrWindow):
    def __init__(self, config, library, battlefield):
        self.painter = ObjectPainter(config, library, battlefield)
        self.selected_object_index = None
        self.pointer_mode = "Terr"

        self.graph_terr = TerrGraph(battlefield)
        self.graph_obj = ObjectGraph(library, battlefield, self.graph_terr)
        self.graph = self.graph_terr

        self.config_backup = copy.deepcopy(config)
        self.battlefield =  battlefield
        self.library = library
        self.config = config
        
        title = config["window-title"]
        width, height = config["window-size"]
        BaseWindow.__init__(self, title, width, height)

    def on_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Escape":
            print("##> move center & redraw")
            self.config["window-offset"] = self.config_backup["window-offset"]
            self.config["window-zoom"] = self.config_backup["window-zoom"]
            self.painter.connections = []
            self.draw_content()
        elif key_name == "F1":
            print("##> pointer mode: Terr")
            self.pointer_mode = "Terr"
            self.graph = self.graph_terr
            self.painter.connections = []
            self.draw_content()
        elif key_name == "F2":
            print("##> pointer mode: Obj")
            self.pointer_mode = "Obj"
            self.graph = self.graph_obj
            self.painter.connections = []
            self.draw_content()
        else: return TerrWindow.on_press(self, widget, event)

    def on_click_obj(self, widget, event):
        ox, oy = self.get_click_location(event)
        self.selected_object_index, min_d2 = None, math.inf
        max_d2 = self.config["max-selection-d2"] * self.config["window-zoom"]
        for i, (name, x, y, *params) in enumerate(self.battlefield["objects"]):
            d2 = (x-ox) **2 + (y-oy) **2
            if min_d2 <= d2: continue
            if d2 > self.config["max-selection-d2"]: continue
            self.selected_object_index, min_d2 = i, d2            
        if self.selected_object_index is None:
            self.painter.connections = []
            print("Selected Obj: -")
            self.draw_content(); return True
        else: print("Selected Obj:", self.battlefield["objects"][self.selected_object_index])
        links = self.graph_obj.find_all_connections(self.selected_object_index)
        self.painter.connections = links
        self.draw_content()
        return True

    def on_click(self, widget, event):
        if self.pointer_mode == "Terr":
            return TerrWindow.on_click(self, widget, event)
        elif self.pointer_mode == "Obj":
            return self.on_click_obj(widget, event)
        else: raise ValueError("on_click")
        
def run_example():
    example_config = {
        "window-zoom": 0.566,
        "window-title": "terr-window",
        "window-size": (1800, 820),
        "window-offset": (750, 400),
        "max-selection-d2": 400,
        "move-sensitive": 50,
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

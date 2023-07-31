#!/usr/bin/python3

import gi, copy, math, os, random
from pprint import pformat

from ObjectValidator import validate
from ObjectPainter import ObjectPainter
from BaseWindow import BaseWindow
from TerrWindow import TerrWindow
from TerrWindow import TerrGraph

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

    
class RunFrame(dict):
    def __init__(self, library, battlefield, graph):
        self.battlefield =  battlefield
        self.library = library
        self.graph = graph
        dict.__init__(self)

    def analyze_out_volumes(self):
        olen = len(self.battlefield["objects"])        
        for i in range(olen):
            print(">>", i)
        
    def analyze(self):
        self.analyze_out_volumes()

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

    def find_object(self, ox, oy, radius2):
        selected_object_index, min_d2 = None, math.inf
        for i, (name, x, y, *params) in enumerate(self.battlefield["objects"]):
            d2 = (x-ox) **2 + (y-oy) **2
            if min_d2 <= d2: continue
            if d2 > radius2: continue
            selected_object_index, min_d2 = i, d2            
        return selected_object_index
    
    def generate_resource(self, x, y):
        out_dict = {}
        if self.library["settings"]["resourcing-method"] == "asymptotic-random":
            assert self.library["settings"]["resourcing-points"], "resourcing-points"
            f, m = self.library["settings"]["resourcing-factor"], math.inf
            for ox, oy in self.library["settings"]["resourcing-points"]:
                d2 = math.sqrt((ox - x) ** 2 + (oy - y) ** 2)
                if d2 < m: m = d2
            for resource, rdef in self.library["resources"].items():
                if "process" in rdef: continue
                out_dict[resource] = f * random.uniform(0, f/m)
        else: raise ValueError("resourcing-method")
        print("New resources point:", out_dict)
        return out_dict

    def add_object(self, choosen):
        if None in list(choosen.values()):
            print("add_object failed none:", choosen); return
        x = int(choosen["x"])
        y = int(choosen["y"])
        obj = choosen["object"]
        player = choosen["player"]

        r2 = self.library["objects"][obj]["radius"] ** 2
        for name, x2, y2, *rest in self.battlefield["objects"]:
            rr2 = self.library["objects"][name]["radius"] ** 2
            d2 = (x2-x) **2 + (y2-y) **2
            if d2 < r2 or d2 < rr2:
                print("add_object failed d/r"); return
        terr, _ = self.terr_graph.check_terrain(x, y)
        buildable = self.library["terrains"][terr]["buildable"]
        if not buildable:
            print("add_object failed - not buildable"); return

        if obj == "store":
            row = obj, x, y, player, 1.0, None, 0.0
        elif obj in ("observer", "barrier", "radiator",
                     "developer", "repeater", "transmitter"):
             row = obj, x, y, player, 1.0, False
        else: row = obj, x, y, player, 1.0, None
        self.battlefield["objects"].append(row)
        if obj in ("mineshaft", "drill"):
            if (x, y) not in self.battlefield["resources"]:
                rdict = self.generate_resource(x, y)
                self.battlefield["resources"][x, y] = rdict

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
            (no == "mineshaft" and ne == "input") or
            (no == "store" and ne == "input") or
            (no == "output" and ne == "store") or
            (no == "store" and ne == "input") or
            (no == "mixer" and ne == "store") or
            (no == "mixer" and ne == "input") or
            (no == "output" and ne == "store")):
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
        elif no in ("store", "output") and ne == "mixer":
            ro, re = objects[i1][5], objects[i2][5]            
            if re is None: return None, None, None, None
            if ro not in self.library["resources"][re]["process"]:
                return None, None, None, None
            if po != pe: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif ((no in ("store", "output") and ne == "laboratory") or
              (no in ("store", "output") and ne == "barrier") or
              (no in ("store", "output") and ne == "developer") or
              (no in ("store", "output") and ne == "radiator") or
              (no in ("store", "output") and ne == "launcher") or
              (no in ("store", "output") and ne == "observer") or
              (no in ("store", "output") and ne == "transmitter")):
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
            if po == pe: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "observer":
            so = objects[i1][5]
            if so is None: return None, None, None, None
            if po == pe: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        return  None, None, None, None
    
    def find_all_connections(self, index):
        output_connections = []
        dfr = self.library["settings"]["base-free-range"]
        hf = self.library["settings"]["base-height-factor"]        
        name = self.battlefield["objects"][index][0]
        dfr2 = self.library["objects"][name].get("free-range", dfr)
        hf2 = self.library["objects"][name].get("height-factor", hf)            
        for i in range(len(self.battlefield["objects"])):
            distance, h, xyo, xye = self.check_objects_connection(index, i)
            if distance is None: continue
            free_range = dfr2 + h * hf2
            row = (index, i), xyo, xye, distance, free_range
            output_connections.append(row)
        return output_connections

    def bandwidth(self, name, dist, free):
        if dist <= free: return 1.0
        rangex = self.library["objects"][name]["range"]
        if free < dist and free > 0:
            dn = rangex - free
            ln = rangex - dist
        else:
            dn = rangex - free - dist
            ln = rangex - free
        return ln / dn
    def connection_bandwidth(self, conn):
        (index, _), _, _, distance, free_range = conn
        name = self.battlefield["objects"][index][0]
        bw = self.bandwidth(name, distance, free_range)
        return bw
    def bandwidth2(self, pipe):
        obj = self.battlefield["objects"][pipe[0][0][0]]
        if len(pipe) == 1:
            bw = self.bandwidth(obj[0], pipe[0][3], pipe[0][4])
            hpe = self.battlefield["objects"][pipe[0][0][0]][4]
            hpo = self.battlefield["objects"][pipe[0][0][1]][4]
            return *pipe[0][0], bw * hpe * hpo
        elif len(pipe) == 2:
            bw0 = self.bandwidth(obj[0], pipe[0][3], pipe[0][4])
            obj2 = self.battlefield["objects"][pipe[1][0][0]]
            bw = bw0 * self.bandwidth(obj2[0], pipe[1][3], pipe[1][4])
            hpe = self.battlefield["objects"][pipe[0][0][0]][4]
            hpo = self.battlefield["objects"][pipe[1][0][1]][4]
            return pipe[0][0][0], pipe[1][0][1], bw * hpe * hpo
        else: raise ValueError("len")

    def find_all_connections2(self, index):
        obj = self.battlefield["objects"][index]
        if obj[0] != "developer":
            for conn in self.find_all_connections(index): yield [conn]
            return
        developer_output = {}
        for oe, xyo, xye, dist, free in self.find_all_connections(index):
            if self.battlefield["objects"][oe[1]][0] == "repeater":
                for oe2, xyo2, xye2, dist2, free2 in self.find_all_connections(oe[1]):
                    #if oe[0] == oe2[1]: continue
                    conn = [(oe, xyo, xye, dist, free), (oe2, xyo2, xye2, dist2, free2)]
                    _, _, bw = self.bandwidth2(conn)
                    if developer_output.get((oe[0], oe2[1]), (0.0, None))[0] < bw:
                        developer_output[oe[0], oe2[1]] = bw, conn
            else:
                conn = [(oe, xyo, xye, dist, free)]
                _, _, bw = self.bandwidth2(conn)
                if developer_output.get(oe, (0.0, None))[0] < bw:
                    developer_output[oe] = bw, conn
        for _, conn in developer_output.values():
            yield conn

    def analyze_bw(self, six):
        olen = len(self.battlefield["objects"])        
        for i in range(olen):
            if i == six: continue
            print(self.battlefield["objects"][i][0:3], "-->")
            for conn in self.find_all_connections2(i):
                _, o, bw = self.bandwidth2(conn)
                out = self.battlefield["objects"][o][0:3]
                print("----->", out, bw)
        if six is not None:
            print(self.battlefield["objects"][six][0:3], "==>>")
            for conn in self.find_all_connections2(six):
                _, o, bw = self.bandwidth2(conn)
                out = self.battlefield["objects"][o][0:3]
                print("----->", out, bw)
                
def inc_object_param5(row, resources):
    if row[5] is not None: 
        ix = (resources.index(row[5]) + 1) % (len(resources) + 1)
        row[5] = None if ix == len(resources) else resources[ix]
    else: row[5] = resources[0]

class ObjectWindow(TerrWindow):
    def __init__(self, config, library, battlefield):
        self.painter = ObjectPainter(config, library, battlefield)
        self.selected_object_index2 = None
        self.selected_object_index = None
        self.pointer_mode = "terr"
        self.reset_shoosen()
        
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

    def reset_shoosen(self):
        self.choosen = {
            "object": None,
            "player": None,            
            "x": None,
            "y": None
        }
        
    def on_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Escape":
            print("##> move center & redraw")
            self.pointer_mode = "terr"
            self.config["window-offset"] = self.config_backup["window-offset"]
            self.config["window-zoom"] = self.config_backup["window-zoom"]
            self.painter.reset()
            self.reset_shoosen()
            self.draw_content()
        elif key_name == "F1":
            print("##> pointer mode: terr")
            self.pointer_mode = "terr"
            self.graph = self.graph_terr
            self.painter.reset()
            self.draw_content()
        elif key_name == "F2":
            print("##> pointer mode: obj")
            self.pointer_mode = "obj"
            self.graph = self.graph_obj
            self.selected_object_index2 = None
            self.selected_object_index = None
            self.painter.reset()
            self.reset_shoosen()
            self.draw_content()
        elif key_name == "F3":
            print("##> pointer mode: obj-new")
            self.pointer_mode = "obj-new"
            self.graph = self.graph_obj
            self.selected_object_index2 = None
            self.selected_object_index = None
            self.painter.reset()
            self.reset_shoosen()
            self.draw_content()
        elif key_name == "F4":
            print("##> pointer mode: obj-edit")
            self.selected_object_index2 = None
            self.pointer_mode = "obj-edit"
            self.graph = self.graph_obj
            self.painter.reset()
            self.reset_shoosen()
            self.draw_content()
        elif key_name == "Delete" and self.pointer_mode == "obj-edit":
            index = self.selected_object_index
            if index is not None:
                xo = self.battlefield["objects"][index][1]
                yo = self.battlefield["objects"][index][2]
                del self.battlefield["objects"][index]
                for i, (name, *rest) in enumerate(self.battlefield["objects"]):
                    if name != "launcher": continue
                    if rest[4] is None: continue
                    if rest[4] == (xo, yo):
                        print("Launcher lost a target...")
                        self.battlefield["objects"][i][5] = None
                self.painter.reset()
                self.reset_shoosen()
                self.draw_content()
                
        elif key_name == "Return" and self.pointer_mode == "obj-new":
            print("##> create new object")
            self.graph.add_object(self.choosen)            
            self.draw_content()        
        elif key_name == "a" and self.pointer_mode == "obj":
            links = []
            if not self.painter.connections:
                for i, _ in enumerate(self.battlefield["objects"]):
                    ls = self.graph_obj.find_all_connections(i)
                    links.extend(ls)
                    self.painter.connections = links
            else: self.painter.connections = []
            self.draw_content()
        elif key_name == "r" and self.pointer_mode == "obj":
            self.graph_obj.analyze_bw(self.selected_object_index)
            rf = RunFrame(self.library, self.battlefield, self.graph_obj)
            rf.analyze()
        elif key_name == "v" and self.pointer_mode == "obj":
            validate(None, self.library, self.battlefield)
        elif key_name == "s" and self.pointer_mode == "obj":
            cnt, libname, mapname = 0, "lib", "map"
            flib = lambda c: f"{libname}-{c}.txt"
            fmap = lambda c: f"{mapname}-{c}.txt"
            while os.path.exists(flib(cnt)): cnt += 1
            while os.path.exists(fmap(cnt)): cnt += 1
            with open(flib(cnt), "w") as fd:
                fd.write(pformat(self.library))
            print("Save library:", flib(cnt))
            with open(fmap(cnt), "w") as fd:
                fd.write(pformat(self.battlefield))
            print("Save battlefield:", fmap(cnt))
        elif key_name == "p" and self.pointer_mode == "obj-new":
            players = list(self.library["players"].keys())            
            if self.choosen["player"] is not None:
                ixp = players.index(self.choosen["player"])
                self.choosen["player"] = players[(ixp+1) % len(players)]
            else: self.choosen["player"] = players[0]
            print("##> switch player: ", self.choosen["player"])
        elif key_name == "o" and self.pointer_mode == "obj-new":
            objects = [ob for ob in self.library["objects"]]
            if self.choosen["object"] is not None:
                ixp = objects.index(self.choosen["object"])
                self.choosen["object"] = objects[(ixp+1) % len(objects)]
            else: self.choosen["object"] = objects[0]
            print("##> switch objects: ", self.choosen["object"])
        else: return TerrWindow.on_press(self, widget, event)
        
    def on_click_obj_select(self, widget, event):        
        ox, oy = self.get_click_location(event)
        max_d2 = self.config["max-selection-d2"] * self.config["window-zoom"]
        self.selected_object_index = self.graph_obj.find_object(ox, oy, max_d2)
        if self.selected_object_index is None:
            self.painter.reset()
            print("Selected object: -")
            self.draw_content(); return None
        objrow = self.battlefield["objects"][self.selected_object_index]
        print("Selected object:", objrow)
        if objrow[0] in ("mineshaft", "drill"):
            resources = self.battlefield["resources"][objrow[1], objrow[2]]
            print("Resources in-place:", resources)
        return self.selected_object_index

    def on_click_obj_edit(self, widget, event):
        index = self.on_click_obj_select(widget, event)
        if index is None: return True        
        row = self.battlefield["objects"][self.selected_object_index]
        if row[0] in ("store", "output", "input"):
            resources = list(sorted(self.library["resources"].keys()))
            inc_object_param5(row, resources)
        if row[0] in ("barrier", "radiator", "observer",
                      "developer", "repeater", "transmitter"):
            row[5] = not row[5]
        if row[0] == "laboratory":
            inc_object_param5(row, self.library["technologies"])
        if row[0] == "mixer":
            r_items = self.library["resources"].items()
            resources = [r for r, v in r_items if "process" in v]
            resources = list(sorted(resources))
            inc_object_param5(row, resources)
        if row[0] == "mineshaft":
            r_items = self.library["resources"].items()
            resources = [r for r, v in r_items if "process" not in v]
            resources = list(sorted(resources))
            inc_object_param5(row, resources)
        if row[0] == "launcher":
            if row[5] is not None: row[5] = None
            elif self.selected_object_index2 is not None:
                i2 = self.selected_object_index2
                row2 = self.battlefield["objects"][i2]
                if row[3] == row2[3]:
                    print("Warning! The same player, ignore...")
                else: row[5] = (row2[1], row2[2])
        print("Object after edit:", row)
        self.painter.selected_object_index = index
        self.draw_content()
        return True
        
    def on_click_obj(self, widget, event):
        index = self.on_click_obj_select(widget, event)
        if index is None: return True
        links = self.graph_obj.find_all_connections(index)
        for link in links:
            bw = self.graph_obj.connection_bandwidth(link)
            name = self.battlefield["objects"][link[0][1]][0]
            print(f"{name}{link[2]}", "--->", bw)
        self.painter.selected_object_index = index
        self.painter.connections = links
        self.draw_content()
        return True

    def on_click(self, widget, event):
        if self.pointer_mode == "terr":
            return TerrWindow.on_click(self, widget, event)
        elif self.pointer_mode == "obj":
            return self.on_click_obj(widget, event)
        elif self.pointer_mode == "obj-edit":
            if event.button == 1:
                return self.on_click_obj_edit(widget, event)
            if event.button == 3:
                ox, oy = self.get_click_location(event)
                max_d2 = self.config["max-selection-d2"] * self.config["window-zoom"]
                self.selected_object_index2 = self.graph_obj.find_object(ox, oy, max_d2)
                print("Object2 index:", self.selected_object_index2)
        elif self.pointer_mode == "obj-new":
            if event.button == 1:
                ox, oy = self.get_click_location(event)
                self.choosen["x"] = ox
                self.choosen["y"] = oy
                self.painter.cross = ox, oy
                self.draw_content()
            elif event.button == 3:
                self.choosen["x"] = None
                self.choosen["y"] = None
                self.painter.cross = None
                self.draw_content()
        else: raise ValueError("on_click")
        
def run_example():
    example_config = {
        "window-zoom": 0.566,
        "window-title": "obj-window",
        "window-size": (1800, 820),
        "window-offset": (750, 400),
        "max-selection-d2": 400,
        "move-sensitive": 50,
    }

    import ast, sys
    from MapExamples import library0
    from MapExamples import battlefield0

    if len(sys.argv) >= 2:
        print("try to load map", sys.argv[1])
        with open(sys.argv[1], "r", encoding="utf-8") as fd:
            battlefield0 = ast.literal_eval(fd.read())
    if len(sys.argv) >= 3:
        print("try to load lib", sys.argv[2])
        with open(sys.argv[2], "r", encoding="utf-8") as fd:
            library0 = ast.literal_eval(fd.read())

    validate(example_config, library0, battlefield0)
    ObjectWindow(example_config, library0, battlefield0)

    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
if __name__ == "__main__": run_example()

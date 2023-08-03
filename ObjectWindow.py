#!/usr/bin/python3

import gi, copy, os
from pprint import pformat

from ObjectValidator import validate
from ObjectPainter import ObjectPainter
from ObjectGraph import ObjectGraph
from BaseWindow import BaseWindow
from TerrWindow import TerrWindow
from TerrWindow import TerrGraph

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

VIEW = "__view"
GLORY = "__glory"
RADIATION = "__radiation"
BARRIER = "__barrier"
DEVEL = "__devel"
FIRE = "__fire"

class RunFrame(dict):
    def __init__(self, library, battlefield, graph):
        self.battlefield =  battlefield
        self.library = library
        self.graph = graph
        dict.__init__(self)

    def __str__(self):
        output = "======[RunFrame]======"
        fsort = lambda kv: kv[1][1]
        for k, v in sorted(self.items(), key=fsort):
            output += f"\n{k} -- {v[1]} --> {v[0]}"
        output += "\n======[RunFrame]======"
        return output
        
    def analyze_out_volumes(self):
        olen = len(self.battlefield["objects"])
        tmp_out_bw_sum, tmp_bw = {}, {}
        for index in range(olen):
            obj = self.battlefield["objects"][index]
            objlib = self.library["objects"][obj[0]]
            if "volume" not in objlib: continue
            resource, volume = obj[5], obj[6]
            if resource is None: continue
            if volume <= 0.0: continue
            for bw, conn in self.graph.find_all_connections2(index):
                assert len(conn) == 1, f"volume cannot be forwarded {conn}"
                tmp_bw[*conn[0][0]] = bw, resource
                if conn[0][0][1] in tmp_out_bw_sum:
                    tmp_out_bw_sum[conn[0][0][1]] += bw
                else: tmp_out_bw_sum[conn[0][0][1]] = bw
        for io, (bw, resource) in tmp_bw.items():
            frac = bw / tmp_out_bw_sum[io[1]]
            obj = self.battlefield["objects"][io[0]]
            objlib = self.library["objects"][obj[0]]
            resrc, volume = obj[5], obj[6]
            assert resrc == resource, "internal error"
            portion = min([objlib["capacity"], volume])
            self[io] = [portion * frac, resource]

    def analyze_out_radiators(self):
        olen = len(self.battlefield["objects"])
        for index in range(olen):
            obj = self.battlefield["objects"][index]
            if obj[0] != "radiator": continue
            if not obj[5]: continue # switch
            objlib = self.library["objects"][obj[0]]
            portion, resource, keys_update = 0.0, objlib["fuel"], []
            for (i, o), (p, res) in self.items():
                if res != resource: continue
                if o != index: continue
                keys_update.append((i, o))
                portion += p
            player, hp = obj[3], obj[4]
            tech = self.library["players"][player]["technologies"]["radiation-ability"]
            if portion > objlib["capacity"]:
                back_factor = objlib["capacity"] / portion
                for k in keys_update: self[k][0] *= back_factor
                portion = objlib["capacity"]
            radfac = self.library["settings"]["radiation-factor"]
            radiation = portion * (1.0 + tech) * hp * radfac
            if radiation > 0.0: self[index, player] = [radiation, RADIATION]

    def analyze_out_barriers(self):
        olen = len(self.battlefield["objects"])
        for index in range(olen):
            obj = self.battlefield["objects"][index]
            if obj[0] != "barrier": continue
            if not obj[5]: continue # switch
            objlib = self.library["objects"][obj[0]]
            portion, resource, keys_update = 0.0, objlib["fuel"], []
            for (i, o), (p, res) in self.items():
                if res != resource: continue
                if o != index: continue
                keys_update.append((i, o))
                portion += p
            player, hp = obj[3], obj[4]
            tech = self.library["players"][player]["technologies"]["barrier-ability"]
            if portion > objlib["capacity"]:
                back_factor = objlib["capacity"] / portion
                for k in keys_update: self[k][0] *= back_factor
                portion = objlib["capacity"]
            barfac = self.library["settings"]["barrier-factor"]
            protection = portion * (1.0 + tech) * hp * barfac
            if protection > 0.0: self[index, player] = [protection, BARRIER]

    def calc_suppression(self, index):
        obj = self.battlefield["objects"][index]
        total = self.battlefield["natural-radiation"]
        objlib = self.library["objects"][obj[0]]
        for (i, player), (p, res) in self.items():
            if obj[3] != player or res != BARRIER: continue
            d, dh, xyo, xye = self.graph.check_objects_connection(i, index)
            if d is None: continue
            obj2 = self.battlefield["objects"][i]
            free_range = self.graph.calc_free_range(obj2, dh)
            conn = (i, index), xyo, xye, d, free_range
            bw = self.graph.connection_bandwidth(conn)
            total -= p * bw            
        for (i, player), (p, res) in self.items():
            if obj[3] == player or res != RADIATION: continue
            d, dh, xyo, xye = self.graph.check_objects_connection(i, index)
            if d is None: continue
            obj2 = self.battlefield["objects"][i]
            free_range = self.graph.calc_free_range(obj2, dh)
            conn = (i, index), xyo, xye, d, free_range
            bw = self.graph.connection_bandwidth(conn)
            total += p * bw
        if total <= 0.0 or "suppress-base" not in objlib: return 0.0
        return total / (total + objlib["suppress-base"])

    def analyze_out_effectors(self):
        effectors = ["observer", "transmitter", "laboratory", "launcher", "developer"]
        olen = len(self.battlefield["objects"])
        for index in range(olen):
            obj = self.battlefield["objects"][index]
            objlib = self.library["objects"][obj[0]]
            if obj[0] not in effectors: continue
            if obj[5] in (None, False): continue
            player, hp = obj[3], obj[4]
            if obj[0] == "laboratory":
                factor, resource = self.library["settings"]["research-factor"], obj[5]
                tech = self.library["players"][player]["technologies"]["research-gain"] 
            elif obj[0] == "transmitter":
                factor, resource = self.library["settings"]["transsmition-factor"], GLORY
                tech = self.library["players"][player]["technologies"]["transsmition-gain"]
            elif obj[0] == "observer":
                factor, resource = self.library["settings"]["observation-factor"], VIEW
                tech = self.library["players"][player]["technologies"]["observation-gain"]
            elif obj[0] == "launcher":
                factor, resource = self.library["settings"]["fire-factor"], FIRE
                tech = self.library["players"][player]["technologies"]["launcher-gain"]
            elif obj[0] == "developer":
                factor, resource = self.library["settings"]["development-factor"], DEVEL
                tech = self.library["players"][player]["technologies"]["developer-gain"]
            else: raise ValueError(f"internal-error {obj[0]}")
            portion, keys_update  = 0.0, []
            for (i, o), (p, res) in self.items():
                if o != index: continue
                keys_update.append((i, o)); portion += p
            if portion > objlib["capacity"]:
                back_factor = objlib["capacity"] / portion
                for k in keys_update: self[k][0] *= back_factor
                portion = objlib["capacity"]
            supress = self.calc_suppression(index)
            portion = factor * hp * portion * (1 + tech) * (1.0 - supress)
            if obj[0] == "launcher":
                links = self.graph.find_all_connections2(index)
                for bw, link in links:
                    self[link[0][0]] = [bw * portion, resource]
            elif obj[0] == "developer":
                links = self.graph.find_all_connections2(index)
                for bw, link in links:
                    self[link[0][0][0], link[-1][0][1]] = [bw * portion, resource]
            else: self[index, player] = [portion, resource]

    def analyze_out_mine(self):
        olen = len(self.battlefield["objects"])
        tmp_out_bw_sum, tmp_bw = {}, {}
        for index in range(olen):
            obj = self.battlefield["objects"][index]
            if obj[0] != "mineshaft": continue
            resources = self.battlefield["resources"][obj[1], obj[2]]            
            player, hp, resource = obj[3], obj[4], obj[5]
            ore = resources.get(resource, 0.0)
            if ore <= 0.0: continue
            supress = self.calc_suppression(index)
            tech = self.library["players"][player]["technologies"]["mine-gain"]
            portion = hp * ore * (1 + tech) * (1.0 - supress)
            for bw, conn in self.graph.find_all_connections2(index):
                assert len(conn) == 1, f"volume cannot be forwarded {conn}"
                tmp_bw[*conn[0][0]] = bw, portion, resource
                if conn[0][0][1] in tmp_out_bw_sum:
                    tmp_out_bw_sum[conn[0][0][1]] += bw
                else: tmp_out_bw_sum[conn[0][0][1]] = bw
        for io, (bw, portion, resource) in tmp_bw.items():
            frac = bw / tmp_out_bw_sum[io[1]]
            obj = self.battlefield["objects"][io[0]]
            assert resource == obj[5], "internal error"
            self[io] = [portion * frac, resource]

    def analyze(self):
        self.analyze_out_volumes()
        self.analyze_out_radiators()
        self.analyze_out_barriers()
        self.analyze_out_effectors()
        self.analyze_out_mine()
        print(self)

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
        elif key_name == "space" and self.pointer_mode == "obj":
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
            players = list(sorted(self.library["players"].keys()))            
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

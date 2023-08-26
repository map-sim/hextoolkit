from SimValidator import SimValidator
from SimPainter import SimPainter
from TerrWindow import TerrWindow

import gi, os, copy, math, random
from pprint import pformat

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class SimGraph:
    max_d2 = 48
    def __init__(self, library, battlefield):
        self.battlefield =  battlefield
        self.library = library

    def check_resource(self, index, x, y):
        if index is None: return
        obj = self.battlefield["objects"][index]
        dx = obj["xy"][0] - x; dy = obj["xy"][1] - y
        if obj["name"] == "post": return "devel"
        if dx < -0.6:
            if obj["name"] == "devel": return "AB"
            else: return "devel"
        if "out" in obj: return obj["out"]
        if obj["name"] == "devel": return "devel"
        if obj["name"] == "hit": return "hit"
        if obj["name"] == "store":
            if len(obj["goods"]) == 0: return
            if len(obj["goods"]) >= 1 and dx >= 0 and dx < 0.6 and dy > 0.25: return obj["goods"][0]
            if len(obj["goods"]) >= 2 and dx < 0 and dx > -0.6 and dy > 0.25: return obj["goods"][1]
            if len(obj["goods"]) >= 5 and dx >= 0 and dx < 0.6 and dy < -0.25: return obj["goods"][4]
            if len(obj["goods"]) >= 6 and dx < 0 and dx > -0.6 and dy < -0.25: return obj["goods"][5]
            if len(obj["goods"]) >= 3 and dx >= 0 and dx < 0.6 and dy <= 0.25 and dy >= -0.25: return obj["goods"][2]
            if len(obj["goods"]) >= 4 and dx < 0 and dx > -0.6 and dy <= 0.25 and dy >= -0.25: return obj["goods"][3]
        return

    def find_next_object(self, x, y):
        index, min_d2 = None, math.inf
        for i, obj in enumerate(self.battlefield["objects"]):
            d2 = (obj["xy"][0] - x) ** 2 + (obj["xy"][1] - y) ** 2
            if d2 > self.max_d2: continue
            if d2 < min_d2: min_d2, index = d2, i
        return index

    def run_mine(self, obj, terr):
        if obj["name"] != "mine": return
        if obj["out"] is None: return
        target_xy = None
        indexes = list(range(len(self.battlefield["links"])))
        random.shuffle(indexes)
        for i in indexes:
            link = self.battlefield["links"][i]
            if link[1] != obj["xy"]: continue
            if obj["out"] != link[0]: continue
            target_xy = link[2]
        if target_xy is None: return
        target_obj = None
        for obj2 in self.battlefield["objects"]:
            if obj2["xy"] == target_xy and obj2["name"] == "store":
                target_obj = obj2
        if target_obj is None: return
        if not target_obj["work"]: return
        if len(target_obj["goods"]) >= 6: return
        t = terr.check_terrain(*obj["xy"])[0]
        resources = self.library["terrains"][t]["resources"]
        p = resources.get(obj["out"], 0.0)
        r = random.random()
        if r > p: return
        print("New good in a mine:", obj["out"])
        target_obj["goods"].append(obj["out"])
        
    def run_storage(self, good, xyo, xye):
        objo, obje = None, None
        for obj in self.battlefield["objects"]:
            if obj["xy"] == xyo or obj["xy"] == xye:
                if obj["name"] != "store": return
            if obj["xy"] == xyo: objo = obj
            if obj["xy"] == xye: obje = obj
        if good not in objo["goods"]: return
        if len(obje["goods"]) >= 6: return
        index = objo["goods"].index(good)
        del objo["goods"][index]
        obje["goods"].append(good)

    def run(self, terr):
        indexes = list(range(len(self.battlefield["links"])))
        random.shuffle(indexes)
        for i in indexes:
            self.run_storage(*self.battlefield["links"][i])
        indexes = list(range(len(self.battlefield["objects"])))
        random.shuffle(indexes)
        for i in indexes:
            self.run_mine(self.battlefield["objects"][i], terr)

class SimWindow(TerrWindow):
    def __init__(self, config, library, battlefield):
        provider = Gtk.CssProvider()
        provider.load_from_data(b""".main-label {
        background-color: rgba(255, 255, 255, .75);
        padding: 10px 10px;}""")

        self.mode_label = Gtk.Label()
        style = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        self.mode_label.get_style_context().add_provider(provider, style)
        self.mode_label.get_style_context().add_class("main-label")
        
        self.mode = "navi"
        self.set_mode_label("navi")
        self.show_info = False
        self.player = None
        self.good = None
        self.obj = None

        TerrWindow.__init__(self, config, library, battlefield)
        self.graphs = {"sim": SimGraph(library, battlefield), "terr": self.graph}
        self.fix.put(self.mode_label, 0, 0)
        self.show_all()

        self.painter = SimPainter(config, library, battlefield)
        self.config_backup = copy.deepcopy(config)
        self.draw_content()

    def set_mode_label(self, text):
        large_font_span = "<span size='25000'>"
        text = large_font_span + f"{text}</span>"
        self.mode_label.set_markup(text)

    def update_info(self):
        content = f"<span size='25000'>{self.mode}: info</span>"
        content += "<span size='15000'>"
        for key, val in self.config.items():
            content += f"\nconfig {key} --> {val}"
            print(f"config {key}", "-->", val)
        print("window width", "-->", self.width)
        content += f"\nwindow width --> {self.width}"
        print("window height", "-->", self.height)
        content += f"\nwindow height --> {self.height}"
        self.set_mode_label(content + "</span>")

    def on_scroll(self, widget, event):
        TerrWindow.on_scroll(self, widget, event)
        if self.show_info: self.update_info()

    def delete_object_links(self):
        torm = set()
        obj = self.battlefield["objects"][self.painter.selected_index]
        for n, link in enumerate(self.battlefield["links"]):
            if link[1] == obj["xy"] or link[2] == obj["xy"]: torm.add(n)
        for n in reversed(sorted(torm)):
            del self.battlefield["links"][n]
    def delete_object(self):
        self.delete_object_links()
        del self.battlefield["objects"][self.painter.selected_index]
        self.painter.selected_index = None
        self.good = None

    def try_to_add_obj(self, x, y):
        obj = self.library["objects"][self.obj]
        iv1 = obj["interval"]
        for k, obj2 in enumerate(self.battlefield["objects"]):
            iv2 = self.library["objects"][obj2["name"]]["interval"]
            d2 = (x - obj2["xy"][0]) ** 2
            d2 += (y - obj2["xy"][1]) ** 2
            d = math.sqrt(d2)
            if d < max([iv1, iv2]):
                print("To close to:", obj2["name"], obj2["xy"]); return False
        new_obj = {"xy": (x, y), "name": self.obj, "own": self.player, "cnt": obj["modules"]}
        if new_obj["name"] == "mixer": new_obj["out"] = None
        if new_obj["name"] == "mine": new_obj["out"] = None
        if new_obj["name"] == "store": new_obj["work"] = False; new_obj["goods"] = []
        if new_obj["name"] == "devel": new_obj["work"] = False
        if new_obj["name"] == "send": new_obj["work"] = False
        if new_obj["name"] == "lab": new_obj["work"] = False
        if new_obj["name"] == "hit": new_obj["work"] = False
        if new_obj["name"] == "post": new_obj["armor"] = True
        elif new_obj["name"] == "nuke": pass
        else: new_obj["armor"] = False
        if self.painter.selected_index is not None:
            obj3 = self.battlefield["objects"][self.painter.selected_index]
            if obj3["name"] == "devel" and self.player == obj3["own"]:
                link = "devel", obj3["xy"], (x, y)
                self.battlefield["links"].append(link)
                new_obj["cnt"] = 0
        self.battlefield["objects"].append(new_obj)
        self.draw_content()
        return True
        
    def try_to_make_link(self, x, y):
        obj = self.battlefield["objects"][self.painter.selected_index]
        if self.good is None: print("No good no-link"); return False
        if self.good != "devel":
            if obj["name"] == "nuke": print("Nuke no-link"); return False
            if obj["name"] == "post": print("Post no-link"); return False
        index = self.graphs["sim"].find_next_object(x, y)
        obj2 = self.battlefield["objects"][index]
        if obj["xy"] == obj2["xy"]: print("Self-link not supported!"); return False
        if self.good == "devel" and "devel" not in [obj["name"], obj2["name"]]:
            print("Devel is supported only by devel!"); return False
        if self.good == "hit" and obj["name"] != "hit":
            print("Hit is supported only by hit!"); return False            
        if obj["name"] == "devel" and self.good in self.library["resources"]:
            if obj2["name"] != "store": print("Recycling only to store!"); return False

        if obj2["name"] == "mine" and self.good in self.library["resources"]: 
            print("Mine does not accept resources!"); return False
        if obj2["name"] == "nuke" and self.good in self.library["resources"]:
            print("Nuke does not accept resources!"); return False
        if obj2["name"] == "post" and self.good in self.library["resources"]:
            print("Post does not accept resources!"); return False
        if self.good in self.library["resources"]:
            if "store" not in [obj["name"], obj2["name"]]:
                print("Resources have to be in store!"); return False            
        count = 0; hit_counter = 0; anti_counter = 0
        new_link = self.good, obj["xy"], obj2["xy"] 
        for link in self.battlefield["links"]:
            if link[1] == obj["xy"] and link[2] == obj2["xy"]: count += 1
            if link[1] == obj["xy"] and self.good == "hit":
                for obj3 in self.battlefield["objects"]:
                    if obj3["xy"] == link[2]:
                        if obj3["own"] == obj["own"]: anti_counter += 1
                        else: hit_counter += 1
            if obj["name"] != "store" or obj2["name"] != "store":
                if link[1] == new_link[1] and link[2] == new_link[2]:
                    print("Link already exists" ); return False
        if count >= 2: print("No free slot (max 2)"); return False
        if obj["own"] != obj2["own"] and hit_counter >= 2:
            print("No free hit slot (max 2)"); return False
        if obj["own"] == obj2["own"] and anti_counter >= 3:
            print("No free anti-hit slot (max 2)"); return False

        d2 = (obj["xy"][0] - obj2["xy"][0]) ** 2
        d2 += (obj["xy"][1] - obj2["xy"][1]) ** 2
        d = math.sqrt(d2)
        if self.good == "devel": r = 2*self.library["objects"]["devel"]["range"]
        elif self.good == "hit": r = 2*self.library["objects"]["hit"]["range"]
        else: r = self.library["objects"]["store"]["range"]
        if d > r: print("Distance greater than range"); return False
        self.battlefield["links"].append(new_link)
        self.draw_content()
        return True

    def try_to_remove_link(self, x, y):
        obj = self.battlefield["objects"][self.painter.selected_index]
        if self.good is None: print("No good no-del-link"); return
        index = self.graphs["sim"].find_next_object(x, y)
        obj2 = self.battlefield["objects"][index]

        torm = list()
        for n, link in enumerate(self.battlefield["links"]):
            if link == (self.good, obj["xy"], obj2["xy"]): torm.append(n)
        for n in reversed(sorted(torm)): del self.battlefield["links"][n] 
        self.draw_content()
    
    def on_click(self, widget, event):
        TerrWindow.on_click(self, widget, event)
        
        ox, oy = self.get_click_location(event)
        if self.mode == "edit" and event.button == 3:
            print("try to make link", self.good)
            status = self.try_to_make_link(ox, oy)
            if status: print("New link done!")
        if self.mode == "delete" and event.button == 3:
            print("delete link", self.good)
            self.try_to_remove_link(ox, oy)            
        if self.mode == "edit" and event.button == 1:
            if self.obj is not None and self.player is not None: 
                print(f"try to add obj {self.obj}/{self.player}")
                status = self.try_to_add_obj(ox, oy)
                if status: print("New obj done!")
            
        if event.button == 1: 
            index = self.graphs["sim"].find_next_object(ox, oy)
            self.painter.set_selected_object(index)
            self.draw_content()

            self.good = self.graphs["sim"].check_resource(index, ox, oy)
            terr, tmplist = self.graphs["terr"].check_terrain(ox, oy), []
            content = f"<span size='25000'>{self.mode}: click</span>"
            content += f"<span size='15000'>\n----------------\n"
            content += f"terrain-type: {terr[0]}\nterrain-shape: {terr[1][0]}"
            if terr[1][2]: content += f"\nterrain-points: {terr[1][2]}"
            if index is not None:
                obj = self.battlefield["objects"][index]
                content += f"\n----------------\n{obj['name']} {obj['xy']}"
                content += f" -- Player: {obj['own']}\n"
                for k, v in obj.items():
                    if k in ("name", "xy", "own"): continue
                    if k == "armor": tmplist += [f"{k}: {'yes' if v else 'no'}"]
                    elif k == "work": tmplist += [f"{k}: {'yes' if v else 'no'}"]
                    elif k == "goods": tmplist += [f"{k}: {', '.join(v)}"]
                    else: tmplist += [f"{k}: {v}"]
            content += " | ".join(tmplist)
            if self.good: content += f"\n----------------\ngood: {self.good}"
            self.set_mode_label(content + "</span>")

    def save_lib_and_map(self):
        self.set_mode_label("navi: save")
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
    def switch_owner(self):
        if self.painter.selected_index is None: return
        obj = self.battlefield["objects"][self.painter.selected_index]
        if self.player is None: return
        if obj["own"] != self.player: self.delete_object_links()
        obj["own"] = self.player
        
    def switch_player(self):
        players = list(sorted(self.library["players"].keys()))
        if self.player is not None:
            index = players.index(self.player)
            index = (index + 1) % len(players)
        else: index = 0
        self.player = players[index]
        self.set_mode_label(f"edit: player: {self.player}")
    def switch_object(self):
        objs = list(sorted(self.library["objects"].keys()))
        if self.obj is not None:
            index = objs.index(self.obj)
            index = (index + 1) % len(objs)
        else: index = 0
        self.obj = objs[index]
        self.set_mode_label(f"edit: object: {self.obj}")
    def switch_good_in_mine(self):
        if self.painter.selected_index is None: return
        obj = self.battlefield["objects"][self.painter.selected_index]
        if obj["name"] != "mine": return
        for n, (g, xy0, _ ) in enumerate(self.battlefield["links"]):
            if xy0 == obj["xy"] and g == obj["out"]:
                del self.battlefield["links"][n]
        raws = [k for k, v in self.library["resources"].items() if "process" not in v]
        if obj["out"] is not None:
            i = (raws.index(obj["out"]) + 1) % len(raws)
            self.good = obj["out"] = raws[i]  
        else: elf.good = obj["out"] = raws[0]
        print("New goot in mine:", obj["out"])
    def switch_good_in_mixer(self):
        if self.painter.selected_index is None: return
        obj = self.battlefield["objects"][self.painter.selected_index]
        if obj["name"] != "mixer": return
        for n, (g, xy0, _ ) in enumerate(self.battlefield["links"]):
            if xy0 == obj["xy"] and g == obj["out"]:
                del self.battlefield["links"][n]
        cmpl = [k for k, v in self.library["resources"].items() if "process" in v]
        if obj["out"] is not None:
            i = (cmpl.index(obj["out"]) + 1) % len(cmpl)
            self.good = obj["out"] = cmpl[i]
        else: self.good = obj["out"] = cmpl[0]
        print("New goot in mixer:", obj["out"])
        
    def on_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name == "Escape":
            print("##> mode: navi & zoom reset")
            self.config["window-offset"] = self.config_backup["window-offset"]
            self.config["window-zoom"] = self.config_backup["window-zoom"]
            self.set_mode_label("navi")
            self.mode = "navi"
            self.player = None
            self.good = None
            self.obj = None
            self.show_info = False
            self.painter.selected_index = None
            self.draw_content()
        elif key_name == "F1" or key_name == "Home":
            print("##> mode: navi")
            self.show_info = False
            self.set_mode_label("navi")
            self.mode = "navi"
            self.draw_content()
        elif key_name == "F2" or key_name == "Insert":
            print("##> pointer mode: edit")
            self.set_mode_label("edit")
            self.mode = "edit"
            self.show_info = False
            self.draw_content()
        elif key_name == "F3" or key_name == "Delete":
            print("##> pointer mode: delete")
            self.set_mode_label("delete")
            self.mode = "delete"
            self.show_info = False
            self.draw_content()
        elif key_name == "F4" or key_name == "End":
            print("##> pointer mode: run")
            self.set_mode_label("run")
            self.mode = "run"
            self.show_info = False
            self.draw_content()
        elif key_name == "i":
            self.show_info = not self.show_info
            if not self.show_info: self.set_mode_label("edit")
        elif key_name == "c" and self.mode == "navi":
            self.set_mode_label("navi: check")
            validator = SimValidator()
            validator.validate_config(self.config)
            validator.validate_library(self.library)
            validator.validate_map(self.library, self.battlefield)
            self.show_info = False
        elif key_name == "Return" and self.mode == "run":
            print("Simulate a single step...")
            self.graphs["sim"].run(self.graphs["terr"])
            self.draw_content()
        elif key_name == "d" and self.mode == "delete":
            if self.painter.selected_index is not None:
                self.delete_object()
                self.draw_content()
        elif key_name == "x" and self.mode == "edit":
            self.switch_owner(); self.draw_content()
        elif key_name == "o" and self.mode == "edit":
            self.switch_object(); print(f"object: {self.obj}")
        elif key_name == "p" and self.mode == "edit":
            self.switch_player(); print(f"player: {self.player}")
        elif key_name == "y" and self.mode == "edit":
            if self.painter.selected_index is not None:
                obj = self.battlefield["objects"][self.painter.selected_index]
                if "work" in obj: obj["work"] = True        
            self.switch_good_in_mine()
            self.switch_good_in_mixer()
            self.draw_content()
        elif key_name == "n" and self.mode == "edit":
            if self.painter.selected_index is not None:
                obj = self.battlefield["objects"][self.painter.selected_index]
                if "targets" in obj: obj["targets"] = []
                if "target" in obj: obj["target"] = None
                if "work" in obj: obj["work"] = False
                if "out" in obj: obj["out"] = None
                self.draw_content()
        elif key_name == "s" and self.mode == "navi":
            self.save_lib_and_map()
            self.show_info = False
        else: TerrWindow.on_press(self, widget, event)
        if self.show_info: self.update_info()

def run_example():
    example_config = {
        "window-title": "mode-window",
        "window-size": (1800, 820),
        "window-offset": (840, 125),
        "window-zoom": 15.0,
        "move-sensitive": 50
    }
    
    import ast, sys
    from SimExamples import library0
    from SimExamples import battlefield0

    if len(sys.argv) >= 2:
        print("try to load map", sys.argv[1])
        with open(sys.argv[1], "r", encoding="utf-8") as fd:
            battlefield0 = ast.literal_eval(fd.read())
    if len(sys.argv) >= 3:
        print("try to load lib", sys.argv[2])
        with open(sys.argv[2], "r", encoding="utf-8") as fd:
            library0 = ast.literal_eval(fd.read())
    
    validator = SimValidator()
    validator.validate_library(library0)
    validator.validate_config(example_config)
    validator.validate_map(library0, battlefield0)
    SimWindow(example_config, library0, battlefield0)

    try: Gtk.main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

# broadwayd :5
# GDK_BACKEND=broadway BROADWAY_DISPLAY=:5 python3 ...
# http://127.0.0.1:8085/
if __name__ == "__main__": run_example()

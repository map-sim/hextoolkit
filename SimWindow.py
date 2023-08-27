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
    def __init__(self, library, battlefield, terr_graph):
        self.battlefield =  battlefield
        self.terr_graph = terr_graph
        self.library = library

    def update_difficulty(self):
        if self.library["settings"]["difficulty-method"] == "random":
            self.battlefield["difficulty"] = random.randint(2,12)
        else: raise ValueError("difficulty-method")

    def get_object_by_xy(self, xy, name=None):
        for obj in self.battlefield["objects"]:
            if obj["xy"] != xy: continue
            if name is None: return obj
            elif obj["name"] == name: return obj
            else: return None
        return None

    def _check_availability(self, obj, substracts):
        substracts2 = copy.deepcopy(substracts)
        for g, xyo, xye in self.battlefield["links"]:
            if g not in substracts2: continue
            if xye != obj["xy"]: continue
            indexg = substracts2.index(g)
            obj2 = self.get_object_by_xy(xyo, "store")
            if obj2 is None or not obj2["work"]: continue
            if g not in obj2["goods"]: continue
            del substracts2[indexg]
            if not substracts2:
                return True
        return False

    def _run_effector(self, obj, substracts):
        if not self._check_availability(obj, substracts): return False
        indexes = list(range(len(self.battlefield["links"])))
        substracts2 = copy.deepcopy(substracts)
        random.shuffle(indexes)
        for i in indexes:
            if not substracts2: break
            link = self.battlefield["links"][i]
            if link[2] != obj["xy"]: continue
            if link[0] not in substracts2: continue
            obj2 = self.get_object_by_xy(link[1], "store")
            if obj2 is None or not obj2["work"]: continue
            if link[0] not in obj2["goods"]: continue
            del obj2["goods"][obj2["goods"].index(link[0])]
            del substracts2[substracts2.index(link[0])]
        return True

    def run_send(self, obj):
        if obj["name"] != "send" or not obj["work"]: return
        substracts = self.library["objects"]["send"]["substracts"]
        if not self._run_effector(obj, substracts): return
        difficulty = self.battlefield["difficulty"]
        if difficulty >= 8: p = 0.0 
        if difficulty == 7: p = 1.0/6
        if difficulty == 6: p = 1.0/3
        if difficulty == 5: p = 1.0/2
        if difficulty == 4: p = 2.0/3
        if difficulty == 3: p = 5.0/6
        if difficulty <= 2: p = 1.0
        los = random.random()
        if los < p:
            self.battlefield["players"][obj["own"]]["send"] += 1
            print(f"Player {obj['own']} send 1 resource into space ({los}<{p})")
        else: print(f"Player {obj['own']} fail to send 1 resource into space ({los}>={p})")

    def run_lab(self, obj):
        if obj["name"] != "lab" or not obj["work"]: return
        substracts = self.library["objects"]["lab"]["substracts"]
        if not self._run_effector(obj, substracts): return
        self.battlefield["players"][obj["own"]]["research"] += 1
        print(f"Player {obj['own']} made 1 research point")

    def run_mine(self, obj):
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
        t = self.terr_graph.check_terrain(*obj["xy"])[0]
        resources = self.library["terrains"][t]["resources"]
        p = resources.get(obj["out"], 0.0)
        r = random.random()
        if r > p: return
        print("New good in a mine:", obj["out"])
        target_obj["goods"].append(obj["out"])
        
    def run_store(self, link):
        good, xyo, xye = link
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

    def run_power_supply(self):
        N = self.library["settings"]["power-by-nuke"]
        M = self.library["settings"]["modules-for-power"]
        needed_power = {p: 0 for p in self.library["players"]}
        available_power = {p: 0 for p in self.library["players"]}
        total_modules = {p: 0 for p in self.library["players"]}
        for obj in self.battlefield["objects"]:
            if obj["cnt"] > 0: total_modules[obj["own"]] += obj["cnt"]
            if "out" in obj and obj["out"] is not None: needed_power[obj["own"]] += 1
            elif "work" in obj and obj["work"]: needed_power[obj["own"]] += 1
            if obj["name"] == "nuke" and obj["cnt"] > 0:
                available_power[obj["own"]] += N
        print("NPower:", ", ".join([f"{p}: {n}" for p,n in needed_power.items()]))
        for player in self.library["players"]:
            # TODO if tech
            available_power[player] += int(total_modules[player] / M)
        available_power2 = copy.deepcopy(available_power)
        for player in self.library["players"]:
            for p, conf in self.battlefield["players"].items():
                if available_power[p] > conf["power-share"].get(player, 0):
                    available_power2[player] += conf["power-share"].get(player, 0)
                    available_power2[p] -= conf["power-share"].get(player, 0)       
                    available_power[p] -= conf["power-share"].get(player, 0)
        available_power = available_power2
        print("APower:", ", ".join([f"{p}: {n}" for p,n in available_power.items()]))
        for player in self.library["players"]:
            if needed_power[player] <= available_power[player]:
                print(f"{player} has sufficient power supply"); continue
            off_buildings, tooff = needed_power[player] - available_power[player], []
            print(f"{player} has deficit: {off_buildings}")
            for i, obj in enumerate(self.battlefield["objects"]):
                if "out" in obj and obj["out"] is None: continue
                if "work" in obj and not obj["work"]: continue  
                if obj["name"] in ["post", "nuke"]: continue
                if obj["own"] != player: continue
                if obj["cnt"] <= 0: continue
                tooff.append(i)
            random.shuffle(tooff)
            for i in range(off_buildings):
                obj = self.battlefield["objects"][tooff[i]]
                print(f"Blackout: {obj['name']} {obj['xy']} / {obj['own']}")
                if "work" in obj: obj["work"] = False
                if "out" in obj: obj["out"] = None

    def run_group(self, items, key):
        indexes = list(range(len(items)))
        random.shuffle(indexes)
        for i in indexes:
            if key == "lab": self.run_lab(items[i])
            elif key == "send": self.run_send(items[i])
            elif key == "store": self.run_store(items[i])
            elif key == "mine": self.run_mine(items[i])
            else: raise ValueError(key)

    def run(self):
        self.battlefield["iteration"] += 1
        # self.run_natural_demage()
        self.run_power_supply()

        self.run_group(self.battlefield["objects"], "send")
        # self.run_group(self.battlefield["links"], "devel")
        # self.run_group(self.battlefield["links"], "hit")
        self.run_group(self.battlefield["objects"], "lab")
        self.run_group(self.battlefield["links"], "store")
        self.run_group(self.battlefield["objects"], "mine")
        self.update_difficulty()

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
        self.show_report = False
        self.show_info = False
        self.player = None
        self.good = None
        self.obj = None

        TerrWindow.__init__(self, config, library, battlefield)
        self.graphs = {"sim": SimGraph(library, battlefield, self.graph),
                       "terr": self.graph}
        self.fix.put(self.mode_label, 0, 0)
        self.show_all()

        self.painter = SimPainter(config, library, battlefield)
        self.config_backup = copy.deepcopy(config)
        self.draw_content()

    def set_mode_label(self, text):
        large_font_span = "<span size='25000'>"
        text = large_font_span + f"{text}</span>"
        self.mode_label.set_markup(text)

    def update_report(self):
        content = f"<span size='25000'>{self.mode}: report</span>"
        content += "\n\n<span size='15000'>"
        content += f"current iteration: {self.battlefield['iteration']}\n"
        content += f"transsmition difficulty: {self.battlefield['difficulty']}\n"
        content += f"objects number: {len(self.battlefield['objects'])}\n"
        content += f"links number: {len(self.battlefield['links'])}\n"
        content += "------------------------\n"
        players = self.library["players"]
        send_row = [f"{p}: {self.battlefield['players'][p]['send']}" for p in players]
        content += f"send resources        => {', '.join(send_row)}\n"
        destroy_row = [f"{p}: {self.battlefield['players'][p]['destroyed']}" for p in players]
        content += f"destruction points   => {', '.join(destroy_row)}\n"
        lost_row = [f"{p}: {self.battlefield['players'][p]['lost']}" for p in players]
        content += f"lost builds/modules => {', '.join(lost_row)}\n"
        tex_row = [f"{p}: {len(self.battlefield['players'][p]['technologies'])}" for p in players]
        content += f"found technologies => {', '.join(tex_row)}\n"
        research_row = [f"{p}: {self.battlefield['players'][p]['research']}" for p in players]
        content += f"research points       => {', '.join(research_row)}\n"
        for p in players:
            ps = self.battlefield["players"][p]["power-share"]
            power_row = [f"{p}: {ps.get(p, 0)}" for p in players]
            content += f"{p} power-share => {', '.join(power_row)}\n"
        self.set_mode_label(content + "</span>")
        
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

    def find_next_object(self, x, y):
        index, min_d2 = None, math.inf
        for i, obj in enumerate(self.battlefield["objects"]):
            d2 = (obj["xy"][0] - x) ** 2 + (obj["xy"][1] - y) ** 2
            if d2 > self.config["selection-radius"]: continue
            if d2 < min_d2: min_d2, index = d2, i
        return index

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
        x = int(x); y = int(y)
        terr = self.graphs["terr"].check_terrain(x, y)
        if not self.library["terrains"][terr[0]]["buildable"]:
            print(f"{terr[0]} is not buildable"); return False        
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
        index = self.find_next_object(x, y)
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
            if link[0] == self.good and link[1] == obj["xy"] and link[2] == obj2["xy"]: 
                print("Identical link already exists" ); return False
            if link[1] == obj["xy"] and link[2] == obj2["xy"]: count += 1
            if link[1] == obj["xy"] and self.good == "hit":
                for obj3 in self.battlefield["objects"]:
                    if obj3["xy"] == link[2]:
                        if obj3["own"] == obj["own"]: anti_counter += 1
                        else: hit_counter += 1
            
            if link[0] in ["hit", "devel"]:
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
        index = self.find_next_object(x, y)
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
            index = self.find_next_object(ox, oy)
            self.painter.set_selected_object(index)
            self.draw_content()

            self.good = self.painter.check_resource(index, ox, oy)
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
    def switch_good(self):
        goods = list(sorted(self.library["resources"].keys()))
        goods += ["devel", "hit"]
        if self.good is not None:
            index = goods.index(self.good)
            index = (index + 1) % len(goods)
        else: index = 0
        self.good = goods[index]
        self.set_mode_label(f"edit: good: {self.good}")
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
        if obj["cnt"] <= 0: obj["out"] = None; return
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
        if obj["cnt"] <= 0: obj["out"] = None; return
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
            self.show_report = False
            self.painter.selected_index = None
            self.draw_content()
        elif key_name == "F1" or key_name == "Home":
            print("##> mode: navi")
            self.set_mode_label("navi")
            self.mode = "navi"
            self.draw_content()
        elif key_name == "F2" or key_name == "Insert":
            print("##> pointer mode: edit")
            self.set_mode_label("edit")
            self.mode = "edit"
            self.draw_content()
        elif key_name == "F3" or key_name == "Delete":
            print("##> pointer mode: delete")
            self.set_mode_label("delete")
            self.mode = "delete"
            self.draw_content()
        elif key_name == "F4" or key_name == "End":
            print("##> pointer mode: run")
            self.set_mode_label("run")
            self.mode = "run"
            self.show_info = False
            self.show_report = True
            self.draw_content()
        elif key_name == "c" and self.mode == "navi":
            self.set_mode_label("navi: check")
            validator = SimValidator()
            validator.validate_config(self.config)
            validator.validate_library(self.library)
            validator.validate_map(self.library, self.battlefield)
        elif key_name == "Return" and self.mode == "run":
            print("Simulate a single step...")
            self.graphs["sim"].run()
            self.draw_content()

        elif key_name == "i":
            self.show_info = not self.show_info
            if not self.show_info: self.set_mode_label(self.mode)
            else: self.show_report = False
        elif key_name == "r":
            self.show_report = not self.show_report
            if not self.show_report: self.set_mode_label(self.mode)
            else: self.show_info = False
            
        elif key_name == "l" and self.mode == "navi":
            if self.painter.draw_good_links is False:
                self.painter.draw_good_links = self.good
            else: self.painter.draw_good_links = False
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
        elif key_name == "g" and self.mode in ["navi", "edit", "delete"]:
            self.switch_good(); print(f"good: {self.good}")
            if self.painter.draw_good_links is not False:
                self.painter.draw_good_links = self.good
                self.draw_content()                
        elif key_name == "y" and self.mode == "edit":
            if self.painter.selected_index is not None:
                obj = self.battlefield["objects"][self.painter.selected_index]
                if "work" in obj and obj["cnt"] > 0: obj["work"] = True        
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
        else: TerrWindow.on_press(self, widget, event)
        if self.show_report: self.update_report()
        if self.show_info: self.update_info()

def run_example():
    example_config = {
        "window-title": "mode-window",
        "window-size": (1800, 820),
        "window-offset": (840, 125),
        "window-zoom": 15.0,
        "selection-radius": 5,
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

import DemoSamples as demo
import SaveValidate as valid

from ObjPainter import AbstractPainter

from ast import literal_eval
import os, json, math

class SaveHandler:
    def __init__(self):
        self.stats = {}
        self.infra = {}
        self.military = {}
        self.controls = {}
        self.settings = {}
        self.terrains = {}
        self.xsystem = []
        self.landform = []
        self.markers = []
        self.units = {}
        self.builds = {}
        self.goods = {}
        self.orders = {}
        
    def load_demo_0(self):
        print("load demo_0")
        self.settings = demo.settings_0
        self.terrains = demo.terrains_0
        self.controls = demo.controls_0
        self.markers = demo.markers_0
        self.builds = demo.builds_0
        self.units = demo.units_0
        self.xsystem = demo.xsystem_0
        self.landform = demo.landform_0
        self.military = demo.military_0
        self.infra = demo.infra_0
        self.stats = demo.stats_0
        self.goods = demo.goods_0
        self.orders = demo.orders_0
        valid.SaveValidate(self)
        
    def save_on_drive(self, prefix="save."):
        fname = lambda c: f"{prefix}{c}"; counter = 0
        while os.path.exists(fname(counter)): counter += 1
        dir_name = fname(counter); os.mkdir(dir_name)
        def inner(fname, data):
            ffname = os.path.join(dir_name, fname)
            with open(ffname, "w") as fd:
                json.dump(data, fd, indent=4)
        def inner2(fname, data):
            ffname = os.path.join(dir_name, fname)
            with open(ffname, "w") as fd:
                data2 = {str(k): v for k, v in data.items()}
                json.dump(data2, fd, indent=4)
        inner2("infra.json", self.infra)
        inner2("military.json", self.military)
        inner("settings.json", self.settings)
        inner("terrains.json", self.terrains)
        inner("controls.json", self.controls)
        inner("landform.json", self.landform)
        inner("xsystem.json", self.xsystem)
        inner("markers.json", self.markers)
        inner("units.json", self.units)
        inner("builds.json", self.builds)
        inner("goods.json", self.goods)
        inner("stats.json", self.stats)
        inner("orders.json", self.orders)
        return dir_name
    def load_from_drive(self, save_name):
        print(f"load from drive {save_name}")
        def inner(fname):
            ffname = os.path.join(save_name, fname)
            with open(ffname, "r") as fd:
                return json.load(fd)
        def inner2(fname):
            ffname = os.path.join(save_name, fname)
            with open(ffname, "r") as fd:
                data = json.load(fd)
                return {literal_eval(k): v for k, v in data.items()}
        self.infra = inner2("infra.json")
        self.military = inner2("military.json")
        self.settings = inner("settings.json")
        self.terrains = inner("terrains.json")
        self.controls = inner("controls.json")
        self.landform = inner("landform.json")
        self.xsystem = inner("xsystem.json")
        self.markers = inner("markers.json")
        self.builds = inner("builds.json")
        self.goods = inner("goods.json")
        self.stats = inner("stats.json")
        self.units = inner("units.json")
        self.orders = inner("orders.json")
        valid.SaveValidate(self)

    def remove_markers(self, vex, name=None):
        for n, marker in reversed(list(enumerate(self.markers))):
            if (marker[0] == name or name is None) and vex in marker:
                del self.markers[n]

    def get_selected_vex(self):
        for n, marker in enumerate(self.markers):
            if marker[0] == "vex" and marker[1] is None:
                return marker[2]
        return None
    def unmark_all(self):
        self.markers = []
    def unmark_all_vexes(self):
        for n, marker in reversed(list(enumerate(self.markers))):
            if marker[0] == "vex": del self.markers[n]        
    def mark_only_one_vex(self, vex):
        self.unmark_all_vexes()
        self.markers.append(("vex", None, vex))

    def unmark_all_orders(self):
        to_remove = []
        for m, marker in enumerate(self.markers):
            if marker[0] in ["a1", "l1", "a2"]:
                to_remove.append(m)
        for m in reversed(to_remove):
            del self.markers[m]
        
    def mark_range(self, unit, vex):
        unitdef = self.units[unit['type']]
        radius = unitdef["action-perf"]["range"]
        if radius < 1: return

        r = self.settings.get("hex-radius", 1.0)
        xo, yo = AbstractPainter.vex_to_loc(vex, r)        
        self.unmark_all_vexes()
        self.markers.append(["vex", None, vex])
        for x in range(int(vex[0]-radius-3), int(vex[0]+radius+2)):
            for y in range(int(vex[1]-radius-3), int(vex[1]+radius+2)):
                if x == 0 and y == 0: continue 
                vex2 = vex[0] + x, vex[1] + y 
                xe, ye = AbstractPainter.vex_to_loc(vex2, r)                
                d = math.sqrt((xo-xe)**2 + (yo-ye)**2)
                if d > r * radius: continue
                marker = ["vex", unit['own'], vex2]
                self.markers.append(marker)

    def mark_order(self, unit, vex):
        if unit["order"] in ["move", "landing"]:
            if "from" in unit:
                marker = ["a1", unit["own"], *unit["from"], vex]
                self.markers.append(marker)
            if "to" in unit:
                marker = ["a1", unit["own"], vex, *unit["to"]]
                self.markers.append(marker)
        elif unit["order"] in ["supply", "transport"]: 
            marker = ["a1", unit["own"], *unit["from"], vex, *unit["to"]]
            self.markers.append(marker)
        elif unit["order"] == "storm":
            if isinstance(unit["to"], int):
                marker = ["a1", unit["own"], vex, (*vex, unit["to"])]
            else: marker = ["a1", unit["own"], vex, unit["to"]]
            self.markers.append(marker)
        elif unit["order"] == "shot":
            if isinstance(unit["to"], int):
                marker = ["a2", unit["own"], vex, (*vex, unit["to"])]
            else: marker = ["a2", unit["own"], vex, unit["to"]]
            self.markers.append(marker)
        elif unit["order"] == "regroup":
            marker = ["a2", unit["own"], *unit["from"], vex]
            self.markers.append(marker)
        elif unit["order"] == "devel":
            marker = ["a2", unit["own"], vex, (*vex, unit["to"])]
            self.markers.append(marker)
        elif unit["order"] == "defence": pass
        else: raise ValueError(f"unknown order: {unit['order']}")

    def orders_to_markers(self, seleced_vex=None, seleced_own=None):
        def inner(vex, own):
            if seleced_vex is not None:
                if seleced_vex != vex: return True
            if seleced_own is not None:
                if seleced_own != unit["own"]: return True
            return False

        self.unmark_all_orders()    
        for vex, units in self.military.items():
            for unit in units:
                if inner(vex, unit["own"]): continue
                self.mark_order(unit, vex)

    def area_control_markers(self, control=None):
        vex_to_own = {}; counters = {k: set() for k in self.controls}
        for vex, units in self.military.items():
            for unit in units:
                if control and control != unit["own"]: continue
                counters[unit["own"]].add(vex)                    
                if vex not in vex_to_own:
                    vex_to_own[vex] = unit["own"]
                elif vex_to_own[vex] == unit["own"]: pass
                else: vex_to_own[vex] = None
        for vex, infra in self.infra.items():
            for build in infra:
                if build is None: continue
                if control and control != build["own"]: continue
                counters[build["own"]].add(vex)
                if vex not in vex_to_own:
                    vex_to_own[vex] = build["own"]
                elif vex_to_own[vex] == build["own"]: pass
                else: vex_to_own[vex] = None
        for vex, own in vex_to_own.items():
            self.markers.append(["vex", own, vex])
        output = "area control:\n"
        for own in counters.keys():
            cnt = len(counters[own])
            output += f"{own} ... {cnt}\n"
        return output

if __name__ == "__main__":
    saver = Saver()
    saver.load_demo_0()

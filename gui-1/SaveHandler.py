import DemoSamples as demo
import MapValidate as valid
from ast import literal_eval
import os, json

class SaveHandler:
    def __init__(self):
        self.stats = {}
        self.infra = {}
        self.units = {}
        self.controls = {}
        self.settings = {}
        self.terrains = {}
        self.landform = []
        self.markers = []
        self.xsystem = {}
        self.isystem = {}

    def load_demo_0(self):
        print("load demo_0")
        self.settings = demo.settings_0
        self.terrains = demo.terrains_0
        self.controls = demo.controls_0
        self.landform = demo.landform_0
        self.markers = demo.markers_0
        self.xsystem = demo.xsystem_0
        self.isystem = demo.isystem_0
        self.stats = demo.stats_0
        self.infra = demo.infra_0
        self.units = demo.units_0
        valid.MapValidate(self)
        
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
        inner("settings.json", self.settings)
        inner("terrains.json", self.terrains)
        inner("controls.json", self.controls)
        inner("landform.json", self.landform)
        inner("markers.json", self.markers)
        inner("xsystem.json", self.xsystem)
        inner("isystem.json", self.isystem)
        inner("stats.json", self.stats)
        inner2("infra.json", self.infra)
        inner2("units.json", self.units)
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
        self.settings = inner("settings.json")
        self.terrains = inner("terrains.json")
        self.controls = inner("controls.json")
        self.landform = inner("landform.json")
        self.markers = inner("markers.json")
        self.xsystem = inner("xsystem.json")
        self.isystem = inner("isystem.json")
        self.stats = inner("stats.json")
        self.infra = inner2("infra.json")
        self.units = inner2("units.json")
        valid.MapValidate(self)

    def remove_markers(self, vex, name=None):
        for n, marker in reversed(list(enumerate(self.markers))):
            if (marker[0] == name or name is None) and vex in marker:
                del self.markers[n]

    def get_selected_vex(self):
        for n, marker in enumerate(self.markers):
            if marker[0] == "vex" and marker[1] is None:
                return marker[2]
        return None
    def unselect_all(self):
        self.markers = []
    def unselect_all_vexes(self):
        for n, marker in reversed(list(enumerate(self.markers))):
            if marker[0] == "vex": del self.markers[n]        
    def select_only_one_vex(self, vex):
        self.unselect_all_vexes()
        self.markers.append(("vex", None, vex))
        
    def orders_to_markers(self, seleced_vex=None):
        to_remove = []
        for m, marker in enumerate(self.markers):
            if marker[0] in ["a1", "l1", "a2"]:
                to_remove.append(m)
        for m in reversed(to_remove):
            del self.markers[m]
    
        for vex, units in self.units.items():
            if seleced_vex is not None:
                if seleced_vex != vex: continue
            for unit in units:
                if unit["order"] != "move": continue                        
                marker = ["a1", unit["own"], vex, *unit["target"]]
                self.markers.append(marker)
        for vex, units in self.units.items():
            if seleced_vex is not None:
                if seleced_vex != vex: continue
            for unit in units:
                if unit["order"] != "supply": continue                        
                marker = ["a1", unit["own"], *unit["source"], vex, *unit["target"]]
                self.markers.append(marker)
        for vex, units in self.units.items():
            if seleced_vex is not None:
                if seleced_vex != vex: continue
            for unit in units:
                if unit["order"] != "storm": continue
                if isinstance(unit["target"], tuple):
                    vex2 = tuple(unit["target"][:2])
                    marker = ["a1", unit["own"], vex, vex2]
                    self.markers.append(marker)
                else: print(f"TODO: storm infra in", unit["target"])
        for vex, units in self.units.items():
            if seleced_vex is not None:
                if seleced_vex != vex: continue
            for unit in units:
                if unit["order"] != "shot": continue
                if isinstance(unit["target"], tuple):
                    vex2 = tuple(unit["target"][:2])
                    marker = ["a2", unit["own"], vex, vex2]
                    self.markers.append(marker)
                    if len(unit["target"]) != 2:
                        print(f"TODO: shot infra in", unit["target"])
                else: print(f"TODO: shot infra in", unit["target"])
    def area_control_markers(self, control=None):
        vex_to_own = {}
        for vex, units in self.units.items():
            for unit in units:
                if control and control != unit["own"]: continue
                if vex not in vex_to_own: vex_to_own[vex] = unit["own"]
                elif vex_to_own[vex] == unit["own"]: pass
                else: vex_to_own[vex] = None
        for vex, infra in self.infra.items():
            for build in infra:
                if control and control != build["own"]: continue
                if vex not in vex_to_own: vex_to_own[vex] = build["own"]
                elif vex_to_own[vex] == build["own"]: pass
                else: vex_to_own[vex] = None
        for vex, own in vex_to_own.items():
            self.markers.append(["vex", own, vex])
    
if __name__ == "__main__":
    saver = Saver()
    saver.load_demo_0()

import DemoSamples as demo
from ast import literal_eval
import os, json

class SaveHandler:
    def __init__(self):
        self.stats = {}
        self.infra = {}
        self.controls = {}
        self.settings = {}
        self.terrains = {}
        self.tech_list = []
        self.landform = []
        self.markers = []

    def load_demo_0(self):
        self.tech_list = demo.tech_list_0
        self.settings = demo.settings_0
        self.terrains = demo.terrains_0
        self.controls = demo.controls_0
        self.landform = demo.landform_0
        self.markers = demo.markers_0
        self.stats = demo.stats_0
        self.infra = demo.infra_0

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
        inner("tech_list.json", self.tech_list)
        inner("settings.json", self.settings)
        inner("terrains.json", self.terrains)
        inner("controls.json", self.controls)
        inner("landform.json", self.landform)
        inner("markers.json", self.markers)
        inner("stats.json", self.stats)
        inner2("infra.json", self.infra)
        return dir_name
    def load_from_drive(self, save_name):
        def inner(fname):
            ffname = os.path.join(save_name, fname)
            with open(ffname, "r") as fd:
                return json.load(fd)
        def inner2(fname):
            ffname = os.path.join(save_name, fname)
            with open(ffname, "r") as fd:
                data = json.load(fd)
                return {literal_eval(k): v for k, v in data.items()}
        self.tech_list = inner("tech_list.json")
        self.settings = inner("settings.json")
        self.terrains = inner("terrains.json")
        self.controls = inner("controls.json")
        self.landform = inner("landform.json")
        self.markers = inner("markers.json")
        self.stats = inner("stats.json")
        self.infra = inner2("infra.json")

    def remove_links(self, vex):
        for n, marker in reversed(list(enumerate(self.markers))):
            if marker[0] == "link" and vex in marker:
                del self.markers[n]
    def remove_vectors(self, vex):
        for n, marker in reversed(list(enumerate(self.markers))):
            if marker[0] == "arr" and vex in marker:
                del self.markers[n]
    def remove_dashes(self, vex):
        for n, marker in reversed(list(enumerate(self.markers))):
            if marker[0] == "dash" and vex in marker:
                del self.markers[n]

    def get_selected_vex(self):
        for n, marker in enumerate(self.markers):
            if marker[0] == "vex" and marker[1] is None:
                return marker[2]
        return None
    def unselect_all_vexes(self):
        for n, marker in reversed(list(enumerate(self.markers))):
            if marker[0] == "vex": del self.markers[n]        
    def select_only_one_vex(self, vex):
        self.unselect_all_vexes()
        self.markers.append(("vex", None, vex))
        
        
if __name__ == "__main__":
    saver = Saver()
    saver.load_demo_0()

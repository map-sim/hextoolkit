import DemoSamples as demo

class SaveHandler:
    def __init__(self):
        self.controls = {}
        self.settings = {}
        self.terrains = {}
        self.landform = []
        self.markers = []
        
    def load_demo_0(self):
        self.settings = demo.settings_0
        self.terrains = demo.terrains_0
        self.controls = demo.controls_0
        self.landform = demo.landform_0
        self.markers = demo.markers_0

    def get_selected_vex(self):
        for n, marker in enumerate(self.markers):
            if marker[0] == "vex" and marker[1] is None:
                return marker[2]
        return None
    def unselect_all_vexes(self):
        torm = set()
        for n, marker in enumerate(self.markers):
            if marker[0] == "vex": torm.add(n)
        for n in reversed(sorted(torm)):
            del self.markers[n]        
    def select_only_one_vex(self, vex):
        self.unselect_all_vexes()
        self.markers.append(("vex", None, vex))
        
        
if __name__ == "__main__":
    saver = Saver()
    saver.load_demo_0()

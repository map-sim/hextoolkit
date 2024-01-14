import DemoSamples as demo

class SaveHandler:
    def __init__(self):
        self.settings = {}
        self.terrains = {}
        self.landform = {}
        
    def load_demo_0(self):
        self.settings = demo.settings_0
        self.terrains = demo.terrains_0
        self.landform = demo.landform_0

if __name__ == "__main__":
    saver = Saver()
    saver.load_demo_0()

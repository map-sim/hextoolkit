class MapValidate:
    def __init__(self, handler):
        self.handler = handler
        self.validate_landform()
        self.validate_markers()
        self.validate_infra()
        self.validate_military()
        self.validate_xsystem()
        self.validate_stats()
        
    def validate_landform(self):
        vexes = set(); counter = 0
        for vex in self.handler.landform:
            assert vex[0] in ("vex", "base", "grid", "coast"), vex[0]
            if vex[1] == "vex":
                assert vex[1] in self.handler.terrains, vex[1]
                assert vex[2] not in vexes, vex[2]
                vexes.add(vex[2])
            counter += 1
        print(f"landform ({counter})... OK")

    def validate_markers(self):
        counter = 0
        for marker in self.handler.markers:
            assert marker[0] in ("vex", "a1", "l1", "a2", "inf")
            if marker[1] is not None:
                assert marker[1] in self.handler.controls, marker[1]
            counter += 1
        print(f"markers ({counter})... OK")

    def validate_military(self):
        counter = 0
        for units in self.handler.military.values():
            for unit in units:
                assert unit["type"] in self.handler.units, unit["type"]
                assert unit["own"] in self.handler.controls, unit["own"] 
                counter += 1
        print(f"units ({counter})... OK")

    def validate_xsystem(self):
        counter = 0
        for unit_name in self.handler.units.keys():
            assert unit_name in self.handler.xsystem, unit_name
            counter += 1
        print(f"xsystem ({counter})... OK")

    def validate_infra(self):
        counter = 0
        for builds in self.handler.infra.values():
            for build in builds:
                if build is None: continue
                assert build["type"] in self.handler.builds, build["type"]
                assert build["own"] in self.handler.controls, build["own"] 
                counter += 1
        print(f"infra ({counter})... OK")

    def validate_stats(self):
        counter = 0
        for name, data in self.handler.stats.items():
            for key, vals in data.items():
                counter += len(vals)
        print(f"stats ({counter})... OK")

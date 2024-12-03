
class NextTurn:
    def __init__(self, handler):
        self.handler = handler
        
    def init_stats(self):
        groups = ["Units", "Infra", "Army"]
        for group in groups + ["Area"]:
            if group not in self.handler.stats:
                self.handler.stats[group] = {}
        for control in self.handler.controls:
            for group in groups + ["Area"]:
                if control not in self.handler.stats[group]:
                    self.handler.stats[group][control] = []
        for group in groups:                    
            if "All" not in self.handler.stats[group]:
                self.handler.stats[group]["All"] = []

    def stats_update(self):
        for control in self.handler.controls:
            u = 0; i = 0; s = 0; aset=set()
            ua = 0; ia = 0; sa = 0
            for vex, units in self.handler.military.items():
                for unit in units:
                    if unit["own"] == control:
                        u += 1; s += unit["size"]; aset.add(vex)
                    ua += 1; sa += unit["size"]
            self.handler.stats["Army"][control].append(s)
            self.handler.stats["Units"][control].append(u)
            for vex, infra in self.handler.infra.items():
                for build in infra:
                    if build["own"] == control:
                        i += 1; aset.add(vex)
                    ia += 1
            self.handler.stats["Infra"][control].append(i)
            self.handler.stats["Area"][control].append(len(aset))
        self.handler.stats["Units"]["All"].append(ua)
        self.handler.stats["Army"]["All"].append(sa)
        self.handler.stats["Infra"]["All"].append(ia)
        
    def execute(self):
        self.stats_update()

        self.handler.settings["current-turn"] += 1
        n = self.handler.settings["current-turn"]
        print(f"next turn: {n}")
        return f"next turn: {n}"

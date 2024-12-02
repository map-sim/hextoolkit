
class NextTurn:
    def __init__(self, handler):
        self.handler = handler
        
    def init_stats(self):
        if "units" not in self.handler.stats:
            self.handler.stats["units"] = {}
        if "army" not in self.handler.stats:
            self.handler.stats["army"] = {}
        if "infra" not in self.handler.stats:
            self.handler.stats["infra"] = {}
        for control in self.handler.controls:
            if control not in self.handler.stats["units"]:
                self.handler.stats["units"][control] = []
            if control not in self.handler.stats["infra"]:
                self.handler.stats["infra"][control] = []
            if control not in self.handler.stats["army"]:
                self.handler.stats["army"][control] = []
        if "All" not in self.handler.stats["infra"]:
            self.handler.stats["infra"]["All"] = []
        if "All" not in self.handler.stats["units"]:
            self.handler.stats["units"]["All"] = []
        if "All" not in self.handler.stats["army"]:
            self.handler.stats["army"]["All"] = []

    def stats_update(self):
        for control in self.handler.controls:
            u = 0; i = 0; s = 0
            ua = 0; ia = 0; sa = 0
            for units in self.handler.units.values():
                for unit in units:
                    if unit["own"] == control:
                        u += 1; s += unit["size"]
                    ua += 1; sa += unit["size"]
            self.handler.stats["army"][control].append(s)
            self.handler.stats["units"][control].append(u)
            
            for infra in self.handler.infra.values():
                for build in infra:
                    if build["own"] == control: i += 1
                    ia += 1
            self.handler.stats["infra"][control].append(i)
        self.handler.stats["units"]["All"].append(ua)
        self.handler.stats["army"]["All"].append(sa)
        self.handler.stats["infra"]["All"].append(ia)
        
    def execute(self):
        self.stats_update()

        self.handler.settings["current-turn"] += 1
        n = self.handler.settings["current-turn"]
        print(f"next turn: {n}")
        return f"next turn: {n}"

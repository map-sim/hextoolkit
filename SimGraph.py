import copy, random, math

class SimGraph:
    def __init__(self, library, battlefield, terr_graph):
        self.battlefield =  battlefield
        self.terr_graph = terr_graph
        self.library = library

    def update_difficulty(self):
        if self.library["settings"]["difficulty-method"] == "random":
            self.battlefield["difficulty"] = random.randint(2,12)
        else: raise ValueError("difficulty-method")

    def delete_object_links(self, index):
        torm = set()
        obj = self.battlefield["objects"][index]
        for n, link in enumerate(self.battlefield["links"]):
            if link[1] == obj["xy"] or link[2] == obj["xy"]: torm.add(n)
        for n in reversed(sorted(torm)): del self.battlefield["links"][n]
    def delete_object(self, index):
        self.delete_object_links(index)
        del self.battlefield["objects"][index]

    def run_natural_demage(self):
        torm = set()
        for i, obj in enumerate(self.battlefield["objects"]):
            t = self.terr_graph.check_terrain(*obj["xy"])[0]
            risk = self.library["terrains"][t]["risk"]
            if risk <= 0: continue
            los = random.random()
            print(los, "<?", risk)
            if los < risk:
                if obj["cnt"] > 0:
                    obj["cnt"] -= 1
                elif obj["cnt"] < 0:
                    obj["cnt"] += 1
                print(f"{obj['own']}'s object: {obj['name']} took 1 demage point from env")
                if obj["cnt"] == 0: torm.add(i)
        for n in reversed(sorted(torm)):
            print(f"Player {obj['own']} lost object: {obj['name']}")
            self.delete_object(n)

    def get_object_by_xy(self, xy, name=None):
        for obj in self.battlefield["objects"]:
            if obj["xy"] != xy: continue
            if name is None: return obj
            elif obj["name"] == name:
                return obj
            else: return None
        return None

    def find_by_xy_source_and_target_name(self, xy, name=None, good=None):
        indexes = list(range(len(self.battlefield["links"])))
        random.shuffle(indexes)
        for i in indexes:
            link = self.battlefield["links"][i]
            if link[1] != xy: continue
            if good is not None and good != link[0]: continue
            obj = self.get_object_by_xy(link[2], name)
            if obj is not None: yield link, obj
    def find_by_xy_target_and_source_name(self, xy, name=None, good=None):
        indexes = list(range(len(self.battlefield["links"])))
        random.shuffle(indexes)
        for i in indexes:
            link = self.battlefield["links"][i]
            if link[2] != xy: continue
            if good is not None and good != link[0]: continue
            obj = self.get_object_by_xy(link[1], name)
            if obj is not None: yield link, obj

    def check_store_accept(self, obj):
        if obj["name"] != "store": return False
        if self.check_tech(obj["own"], "resource-compresion"):
            store_capasity = 6
        else: store_capasity = 4
        if len(obj["goods"]) >= store_capasity: return False
        if not obj["work"]: return False
        return True

    def run_mine(self, obj, first_try=True):
        if obj["name"] != "mine" or obj["out"] is None: return
        for _, target in self.find_by_xy_source_and_target_name(obj["xy"], "store", obj["out"]):
            if not self.check_store_accept(target): continue
            if obj["own"] != target["own"]: continue
            t = self.terr_graph.check_terrain(*obj["xy"])[0]
            resources = self.library["terrains"][t]["resources"]
            if random.random() < resources.get(obj["out"], 0.0):
                print("New good in a mine:", obj["out"])
                target["goods"].append(obj["out"]); break
        if not first_try: return
        if self.check_tech(obj["own"], "advanced-mining"):
            if random.random() < 0.5: self.run_mine(obj, False)
    def run_mixer(self, obj, first_try=True):
        if obj["name"] != "mixer" or obj["out"] is None: return
        for _, target in self.find_by_xy_source_and_target_name(obj["xy"], "store", obj["out"]):
            if not self.check_store_accept(target): continue
            if obj["own"] != target["own"]: continue
            process = self.library["resources"][obj["out"]]["process"]
            substracts = []
            for k, v in process.items():
                substracts.extend([k] * int(v))
            if not self._run_effector(obj, substracts): return
            target["goods"].append(obj["out"])
        if not first_try: return
        if self.check_tech(obj["own"], "advanced-processing"):
            if random.random() < 0.5: self.run_mine(obj, False)

    def run_store(self, link, transfer=False):
        good, xyo, xye = link
        objo, obje = None, None
        for obj in self.battlefield["objects"]:
            if obj["xy"] == xyo or obj["xy"] == xye:
                if obj["name"] != "store": return
            if obj["xy"] == xyo: objo = obj
            if obj["xy"] == xye: obje = obj
        if not objo["work"]: return
        if good not in objo["goods"]: return
        if not self.check_store_accept(obje): return
        if not transfer:
            if objo["own"] != obje["own"]: return
        elif objo["own"] != obje["own"]:
            print("Player", objo["own"], "exports to player", obje["own"], "1", good)
        index = objo["goods"].index(good)
        del objo["goods"][index]
        obje["goods"].append(good)

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
            if not substracts2: return True
            if g in substracts2:
                if obj2["goods"].count(g) <= 1: continue
                indexg2 = substracts2.index(g)
                del substracts2[indexg2]
            if not substracts2:
                return True
        return False

    def _run_effector(self, obj, substracts=None):
        if substracts is None:
            substracts = self.library["objects"][obj["name"]]["substracts"]
        if not self._check_availability(obj, substracts): return False
        substracts2 = copy.deepcopy(substracts)
        indexes = list(range(len(self.battlefield["links"])))
        random.shuffle(indexes)
        for i in 2 * indexes:
            link = self.battlefield["links"][i]
            if link[2] != obj["xy"]: continue
            if link[0] not in substracts2: continue
            obj2 = self.get_object_by_xy(link[1], "store")
            if obj2 is None or not obj2["work"]: continue
            if link[0] not in obj2["goods"]: continue
            del obj2["goods"][obj2["goods"].index(link[0])]
            del substracts2[substracts2.index(link[0])]
            if not substracts2: break
        return True

    def run_send(self, obj, first=True):
        if obj["name"] != "send" or not obj["work"]: return
        if not self._run_effector(obj): return
        difficulty = self.battlefield["difficulty"]
        sensor_tech = self.check_tech(obj["own"], "sensor-system")
        if sensor_tech: difficulty -= 1 
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
        if first and self.check_tech(obj["own"], "fast-transsmition"):
            if random.random() < 0.5:
                self.run_send(obj, first=False)

    def run_lab(self, obj, first=True):
        if obj["name"] != "lab" or not obj["work"]: return
        if not self._run_effector(obj): return
        self.battlefield["players"][obj["own"]]["research"] += 1
        print(f"Player {obj['own']} made 1 research point")
        if first and self.check_tech(obj["own"], "extended-rnd-department"):
            if random.random() < 0.5:
                self.run_lab(obj, first=False)
        
    def check_view(self, obj, obj2):
        method = self.library["settings"]["view-method"]
        if method == "equal-or-lower":
            return self.check_view_eq_low(obj, obj2)
        else: raise ValueError("view-method")

    def check_view_eq_low(self, obj, obj2):        
        dxy = self.library["settings"]["view-resolution"]
        to = self.terr_graph.check_terrain(*obj["xy"])[0]
        lo = self.library["terrains"][to]["level"]
        d = self.calc_distance(obj, obj2)
        no = int(d/dxy)
        dx = float(obj2["xy"][0] - obj["xy"][0]) / no
        dy = float(obj2["xy"][1] - obj["xy"][1]) / no
        for n in range(no):
            x = obj["xy"][0] + n * dx; y = obj["xy"][1] + n * dy
            t = self.terr_graph.check_terrain(x, y)[0]
            lv = self.library["terrains"][t]["level"]
            if lv > lo: return False
        t = self.terr_graph.check_terrain(*obj2["xy"])[0]
        lv = self.library["terrains"][t]["level"]
        if lv > lo: return False
        else: return True    
                
    def calc_distance(self, obj, obj2):
        d2 = (obj["xy"][0] - obj2["xy"][0]) ** 2 
        d2 += (obj["xy"][1] - obj2["xy"][1]) ** 2
        if d2 == 0: return 0.0
        return  math.sqrt(d2)

    def run_devel(self, obj):
        if obj["name"] != "devel" or not obj["work"]: return
        if obj["cnt"] <= 0: return
        R = self.library["objects"]["devel"]["range"]
        subs2 = [self.library["objects"]["devel"]["substracts"][0]]
        recovery_tech = self.check_tech(obj["own"], "construction-recovery")
        for _, build in self.find_by_xy_source_and_target_name(obj["xy"], good="devel"): break
        else: build = None
        if build is not None:
            armor_tech = self.check_tech(obj["own"], "passive-armor")
            M = self.library["objects"][build["name"]]["modules"]
            if build["cnt"] >= M and not armor_tech: return
            elif build["cnt"] >= M and build["armor"]: return
            dist = self.calc_distance(obj, build)
            if dist <= R: P = float(obj["cnt"]) / 3
            elif dist <= 2 * R: P = float(obj["cnt"]) / 3 - 1.0/6
            if dist > 2 * R: return
            los = random.random()
            if los > P and not recovery_tech:
                if self._run_effector(obj, subs2):
                    print("Devel disaster...")
                return # return without building
            elif los > P and recovery_tech:
                if random.random() > P:
                    if self._run_effector(obj, subs2):
                        print("Devel disaster...")
                    return # return without building
            print("--------------------------------------->", build)
            if build["cnt"] == M and armor_tech and not build["armor"]:
                if self._run_effector(obj, subs2):
                    f"Player {obj['own']} build armor on {build['name']}"
                    build["armor"] = True
            if self._run_effector(obj):
                if build["cnt"] > 0 and build["cnt"] < M: build["cnt"] += 1
                elif build["cnt"] <= 0: build["cnt"] -= 1
                if build["name"] == "hit" and build["cnt"] < 0:
                    build["cnt"] = -build["cnt"]
                    print("{build['name']} starts to be operated")
                if build["cnt"] == -M:
                    build["cnt"] = M
                    print("{build['name']} starts to be operated")
                f"Player {obj['own']} builds one module of {build['name']}"
            print("--------------------------------------->", build)
        elif self.check_tech(obj["own"], "build-recycling"):
            for _, build in self.find_by_xy_target_and_source_name(obj["xy"], name=None, good="devel"): break
            else:
                for _, store in self.find_by_xy_source_and_target_name(obj["xy"], name="store", good=subs2[0]):
                    if not self.check_store_accept(store): continue
                    print("Auto recycling...!")
                    P = float(obj["cnt"]) / 3
                    if random.random() < P:
                        obj["cnt"] -= 1
                        store["goods"].append(subs2[0])
                    elif recovery_tech and random.random() < P:
                        obj["cnt"] -= 1
                        store["goods"].append(subs2[0])
                    if obj["cnt"] == 0:
                        print("Auto destruction!")
                        for n, obj2 in enumerate(self.battlefield["objects"]):
                            if obj2["xy"] == obj["xy"]: return n
                    else: return                    
                return
            store = None
            for _, obj2 in self.find_by_xy_source_and_target_name(obj["xy"], name="store", good=subs2[0]):
                if not self.check_store_accept(obj2): continue
                store = obj2
            if store is None: return
            dist = self.calc_distance(obj, build)
            if dist <= R: P = float(obj["cnt"]) / 3
            elif dist <= 2 * R: P = float(obj["cnt"]) / 3 - 1.0/6
            if dist > 2 * R: return
            if random.random() < P:
                build["cnt"] -= 1
                store["goods"].append(subs2[0])
            elif recovery_tech and random.random() < P:
                build["cnt"] -= 1
                store["goods"].append(subs2[0])
            if build["cnt"] == 0:
                for n, obj2 in enumerate(self.battlefield["objects"]):
                    if obj2["xy"] == build["xy"]: return n

    def try_to_hit(self, obj, link):
        print(link)
        
    def run_hit(self, obj):
        if obj["name"] != "hit" or not obj["work"]: return
        if obj["cnt"] <= 0: return
        R = self.library["objects"]["hit"]["range"]
        for link, _ in self.find_by_xy_source_and_target_name(obj["xy"], good="hit"):
            self.try_to_hit(obj, link)
            
    def check_tech(self, player, tech):
        assert tech in self.library["technologies"], f"no-tech: {tech}"
        techs = self.battlefield["players"][player]["technologies"]
        return tech in techs
        
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
                if self.check_tech(player, "energy-recovery"): factor = 1.25
                else: factor = 1.25
                available_power[obj["own"]] += int(factor * N)
        np_players = ", ".join([f"{p}: {n}" for p,n in needed_power.items()])
        print("Needed Power:", np_players)
        for player in self.library["players"]:
            if self.check_tech(player, "intergrid-transformation"):
                available_power[player] += int(total_modules[player] / M)
        available_power2 = copy.deepcopy(available_power)
        for player in self.library["players"]:
            intergrid_tech = self.check_tech(player, "intergrid-transformation")
            for p, conf in self.battlefield["players"].items():
                intergrid_tech2 = self.check_tech(p, "intergrid-transformation")
                if available_power[p] > conf["power-share"].get(player, 0):
                    if not (intergrid_tech or intergrid_tech2): continue
                    available_power2[player] += conf["power-share"].get(player, 0)
                    available_power2[p] -= conf["power-share"].get(player, 0)       
                    available_power[p] -= conf["power-share"].get(player, 0)
        available_power = available_power2
        ap_players = ", ".join([f"{p}: {n}" for p,n in available_power.items()])
        print("Available Power:", ap_players)
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
        torm = set()
        for i in indexes:
            if key == "lab": self.run_lab(items[i])
            elif key == "send": self.run_send(items[i])
            elif key == "devel": torm.add(self.run_devel(items[i]))
            elif key == "store": self.run_store(items[i], False)
            elif key == "store2": self.run_store(items[i], True)
            elif key == "mixer": self.run_mixer(items[i])
            elif key == "mine": self.run_mine(items[i])
            elif key == "hit": self.run_hit(items[i])
            else: raise ValueError(key)
        fsort = lambda x: -1 if x is None else x
        for n in reversed(sorted(torm, key = fsort)):
            if n is None: continue
            self.delete_object(n)

    def run(self):
        self.battlefield["iteration"] += 1
        print("=================", self.battlefield["iteration"])
        self.run_natural_demage()
        self.run_power_supply()

        self.run_group(self.battlefield["objects"], "send")
        self.run_group(self.battlefield["objects"], "devel")
        self.run_group(self.battlefield["objects"], "hit")
        self.run_group(self.battlefield["objects"], "lab")
        self.run_group(self.battlefield["links"], "store")        
        self.run_group(self.battlefield["objects"], "mixer")
        self.run_group(self.battlefield["objects"], "mine")
        self.run_group(self.battlefield["links"], "store2")
        self.update_difficulty()


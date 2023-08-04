import math, random

class ObjectGraph:    
    def __init__(self, library, battlefield, graph_terr):
        self.terr_graph = graph_terr
        self.battlefield =  battlefield
        self.library = library

    def height_diff(self, xo, yo, xe, ye):
        to, _ = self.terr_graph.check_terrain(xo, yo)
        te, _ = self.terr_graph.check_terrain(xe, ye)
        ho = self.library["terrains"][to]["level"]
        he = self.library["terrains"][te]["level"]
        return ho - he
    
    def generate_resource(self, x, y):
        out_dict = {}
        if self.library["settings"]["resourcing-method"] == "asymptotic-random":
            assert self.library["settings"]["resourcing-points"], "resourcing-points"
            f, m = self.library["settings"]["resourcing-factor"], math.inf
            for ox, oy in self.library["settings"]["resourcing-points"]:
                d2 = math.sqrt((ox - x) ** 2 + (oy - y) ** 2)
                if d2 < m: m = d2
            for resource, rdef in self.library["resources"].items():
                if "process" in rdef: continue
                out_dict[resource] = f * random.uniform(0, f/m)
        else: raise ValueError("resourcing-method")
        print("New resources point:", out_dict)
        return out_dict

    def add_object(self, choosen):
        if None in list(choosen.values()):
            print("add_object failed none:", choosen); return
        x = int(choosen["x"])
        y = int(choosen["y"])
        obj = choosen["object"]
        player = choosen["player"]

        r2 = self.library["objects"][obj]["radius"] ** 2
        for name, x2, y2, *rest in self.battlefield["objects"]:
            rr2 = self.library["objects"][name]["radius"] ** 2
            d2 = (x2-x) **2 + (y2-y) **2
            if d2 < r2 or d2 < rr2:
                print("add_object failed d/r"); return
        terr, _ = self.terr_graph.check_terrain(x, y)
        buildable = self.library["terrains"][terr]["buildable"]
        if not buildable:
            print("add_object failed - not buildable"); return

        if obj == "store":
            row = obj, x, y, player, 1.0, None, 0.0
        elif obj in ("observer", "barrier", "radiator",
                     "developer", "repeater", "transmitter"):
             row = obj, x, y, player, 1.0, False
        else: row = obj, x, y, player, 1.0, None
        self.battlefield["objects"].append(row)
        if obj in ("mineshaft", "drill"):
            if (x, y) not in self.battlefield["resources"]:
                rdict = self.generate_resource(x, y)
                self.battlefield["resources"][x, y] = rdict

    def check_objects_connection(self, i1, i2):
        objects = self.battlefield["objects"]
        if i1 == i2: return None, None, None, None
        xo, yo = objects[i1][1], objects[i1][2]
        xe, ye = objects[i2][1], objects[i2][2]
        no, ne = objects[i1][0], objects[i2][0]
        po, pe = objects[i1][3], objects[i2][3]
        do = self.library["objects"][no].get("range", 0)
        if ((no == "store" and ne == "store") or
            (no == "mineshaft" and ne == "store") or
            (no == "mineshaft" and ne == "input") or
            (no == "store" and ne == "input") or
            (no == "output" and ne == "store") or
            (no == "store" and ne == "input") or
            (no == "mixer" and ne == "store") or
            (no == "mixer" and ne == "input") or
            (no == "output" and ne == "store")):
            ro, re = objects[i1][5], objects[i2][5]
            if ro is None: return None, None, None, None
            if re is None: return None, None, None, None
            if po != pe: return None, None, None, None
            if ro != re: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "input" and ne == "output":
            ro, re = objects[i1][5], objects[i2][5]
            if ro is None: return None, None, None, None
            if re is None: return None, None, None, None
            if ro != re: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)        
        elif no in ("store", "output") and ne == "mixer":
            ro, re = objects[i1][5], objects[i2][5]            
            if re is None: return None, None, None, None
            if ro not in self.library["resources"][re]["process"]:
                return None, None, None, None
            if po != pe: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif ((no in ("store", "output") and ne == "laboratory") or
              (no in ("store", "output") and ne == "barrier") or
              (no in ("store", "output") and ne == "developer") or
              (no in ("store", "output") and ne == "radiator") or
              (no in ("store", "output") and ne == "launcher") or
              (no in ("store", "output") and ne == "observer") or
              (no in ("store", "output") and ne == "transmitter")):
            if po != pe: return None, None, None, None
            re = self.library["objects"][ne]["fuel"]
            ro, ze = objects[i1][5], objects[i2][5]
            if ro != re: return None, None, None, None
            if ro is None: return None, None, None, None
            if ze in (None, False): return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "developer" and ne == "repeater":
            if po != pe: return None, None, None, None
            if not objects[i1][5]: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "developer" or no == "repeater" or no == "barrier":
            if po != pe: return None, None, None, None
            if not objects[i1][5]: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "radiator":
            if po == pe: return None, None, None, None
            if not objects[i1][5]: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "launcher":
            te = objects[i1][5]
            if te is None: return None, None, None, None
            if te[0] != xe or te[1] != ye: return None, None, None, None
            if po == pe: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        elif no == "observer":
            so = objects[i1][5]
            if so is None: return None, None, None, None
            if po == pe: return None, None, None, None
            d = math.sqrt((xo-xe) **2 + (yo-ye) **2)
            if d > do: return None, None, None, None
            h = self.height_diff(xo, yo, xe, ye)
            return d, h, (xo, yo), (xe, ye)
        return  None, None, None, None

    def calc_free_range(self, obj, dh):
        print(obj)
        dfr2 = self.library["objects"][obj[0]]["free-range"]
        hf2 = self.library["objects"][obj[0]]["surpass"]            
        return dfr2 + dh * hf2
        
    def find_all_connections(self, index):
        output_connections = []
        for i in range(len(self.battlefield["objects"])):
            distance, dh, xyo, xye = self.check_objects_connection(index, i)
            if distance is None: continue
            free_range = self.calc_free_range(self.battlefield["objects"][index], dh)
            row = (index, i), xyo, xye, distance, free_range
            output_connections.append(row)
        return output_connections

    def bandwidth(self, name, dist, free):
        if dist <= free: return 1.0
        rangex = self.library["objects"][name]["range"]
        if free < dist and free > 0:
            dn = rangex - free
            ln = rangex - dist
        else:
            dn = rangex - free - dist
            ln = rangex - free
        return ln / dn
    def connection_bandwidth(self, conn):
        (index, _), _, _, distance, free_range = conn
        name = self.battlefield["objects"][index][0]
        bw = self.bandwidth(name, distance, free_range)
        return bw
    def bandwidth2(self, pipe):
        obj = self.battlefield["objects"][pipe[0][0][0]]
        if len(pipe) == 1:
            bw = self.bandwidth(obj[0], pipe[0][3], pipe[0][4])
            hpo = self.battlefield["objects"][pipe[0][0][0]][4]
            hpe = self.battlefield["objects"][pipe[0][0][1]][4]
            po = self.battlefield["objects"][pipe[0][0][0]][3]
            pe = self.battlefield["objects"][pipe[0][0][1]][3]
            tech = self.library["players"][po]["technologies"]["bandwidth-factor"]
            if po != pe:
                t = self.library["players"][pe]["technologies"]["bandwidth-factor"]
                tech = tech / 2 + t / 2
            if obj[0] == "launcher": return *pipe[0][0], (1.0 + tech) * bw * hpo
            else: return *pipe[0][0], (1.0 + tech) * bw * (hpe * hpo) ** 0.5
        elif len(pipe) == 2:
            bw0 = self.bandwidth(obj[0], pipe[0][3], pipe[0][4])
            obj2 = self.battlefield["objects"][pipe[1][0][0]]
            bw = bw0 * self.bandwidth(obj2[0], pipe[1][3], pipe[1][4])
            hpe = self.battlefield["objects"][pipe[0][0][0]][4]
            hps = self.battlefield["objects"][pipe[0][0][1]][4]
            hpo = self.battlefield["objects"][pipe[1][0][1]][4]
            return pipe[0][0][0], pipe[1][0][1], bw * (hpe * hps * hpo) ** (1/3)
        else: raise ValueError("len")

    def find_all_connections2(self, index):
        obj = self.battlefield["objects"][index]
        if obj[0] != "developer":
            for conn in self.find_all_connections(index):
                _, _, bw = self.bandwidth2([conn])
                yield bw, [conn]
            return
        developer_output = {}
        for oe, xyo, xye, dist, free in self.find_all_connections(index):
            if self.battlefield["objects"][oe[1]][0] == "repeater":                
                conn = [(oe, xyo, xye, dist, free)]
                _, _, bw = self.bandwidth2(conn)
                if developer_output.get(oe, (0.0, None))[0] < bw:
                    developer_output[oe] = bw, conn                
                for oe2, xyo2, xye2, dist2, free2 in self.find_all_connections(oe[1]):
                    # if oe[0] == oe2[1]: repeater can repair of its developer
                    conn = [(oe, xyo, xye, dist, free), (oe2, xyo2, xye2, dist2, free2)]
                    _, _, bw = self.bandwidth2(conn)
                    if developer_output.get((oe[0], oe2[1]), (0.0, None))[0] < bw:
                        developer_output[oe[0], oe2[1]] = bw, conn
            else:
                conn = [(oe, xyo, xye, dist, free)]
                _, _, bw = self.bandwidth2(conn)
                if developer_output.get(oe, (0.0, None))[0] < bw:
                    developer_output[oe] = bw, conn
        for bw, conn in developer_output.values():
            yield bw, conn

    def analyze_bw(self, six):
        olen = len(self.battlefield["objects"])        
        for i in range(olen):
            if i == six: continue
            print(self.battlefield["objects"][i][0:3], "-->")
            for bw, conn in self.find_all_connections2(i):
                out = self.battlefield["objects"][conn[-1][0][1]][0:3]
                print("----->", out, bw)
        if six is not None:
            print(self.battlefield["objects"][six][0:3], "==>>")
            for bw, conn in self.find_all_connections2(six):
                out = self.battlefield["objects"][conn[-1][0][1]][0:3]
                print("----->", out, bw)

    def find_object(self, ox, oy, radius2):
        selected_object_index, min_d2 = None, math.inf
        for i, (name, x, y, *params) in enumerate(self.battlefield["objects"]):
            d2 = (x-ox) **2 + (y-oy) **2
            if min_d2 <= d2: continue
            if d2 > radius2: continue
            selected_object_index, min_d2 = i, d2            
        return selected_object_index

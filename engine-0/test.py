from PySpice.Spice.Netlist import Circuit

class Analyzer(Circuit):
    abc = "abcdefghij"
    xyz = "pqrstuwxyz"
    counter = [0]
    minus = "m"

    def __init__(self):
        cnt = self.counter[0]
        Circuit.__init__(self, f"cir{cnt}")
        self.counter[0] += 1
        self.voltage = {}
        self.effectors = {}
        self.suppliers = {}

    def show_effectors(self):
        total = 0.0
        print("========== EFFECTORS =============== >>")
        for (x, y, i), res in self.effectors.items():
            voltage = self.check_node(x, y)
            curr = voltage / res
            print(x, y, i, "-->", round(curr, 3), "A")
            total += curr
        print(f"-------------------\nSum ... {total} A")
        print("========== EFFECTORS =============== <<")
        
    def show_suppliers(self):
        total = 0.0
        print("========== SUPPLIERS =============== >>")
        for (x, y, i), curr in self.suppliers.items():
            voltage = self.check_node(x, y)
            print(x, y, i, "-->", round(curr, 3), "A")
            total += curr
        print(f"-------------------\nSum ... {total} A")
        print("========== SUPPLIERS =============== <<")
            
    def tup2code(self, xy):
        ##     0123456789
        sx = str(int(xy[0]))
        sy = str(int(xy[1]))

        if xy[0] < 0: cx = "".join([self.xyz[int(lt)] for lt in sx[1:]])
        else: cx = "".join([self.abc[int(lt)] for lt in sx])
        cy = sy.replace("-", self.minus)
        return(f"{cx}{cy}")

    def code2tup(self, c):
        abc = "".join(filter(lambda x: x in self.abc, c))
        xyz = "".join(filter(lambda x: x in self.xyz, c))
        if abc: nx = int("".join([str(self.abc.index(lt)) for lt in abc]))
        elif xyz: nx = -int("".join([str(self.xyz.index(lt)) for lt in xyz]))
        else: raise ValueError(f"Wrong argument: {c}")

        ffunc = lambda x: (x not in self.abc) and (x not in self.xyz)
        rest = "".join(filter(ffunc, c))
        if self.minus in rest:
            ny = int(rest.replace(self.minus, "-"))
        else: ny = int(rest)
        return nx, ny

    def conn2code(self, xy0, xy1):
        assert xy0 != xy1
        xy0, xy1 = list(sorted([xy0, xy1]))
        c0 = self.tup2code(xy0)
        c1 = self.tup2code(xy1)
        return f"{c0}_{c1}"

    def decode(self, c):
        if "_" in c:
            c0, c1 = c.split("_")
            xy0 = self.code2tup(c0)
            xy1 = self.code2tup(c1)
            return xy0, xy1
        else: return self.code2tup(c)

    def supplier(self, hexy, index, current):
        self.suppliers[*hexy, index] = current
        node = self.tup2code(hexy)
        name = f"{node}.{index}"
        inode = name
        vs = self.CurrentSource(name, self.gnd, node, current)
        #vs = self.VoltageSource(name, self.gnd, inode, current)
        # print(vs)
        return vs

    def effector(self, hexy, index, conductance):
        resistance = 1.0 / conductance
        self.effectors[*hexy, index] = resistance
        node = self.tup2code(hexy)
        if index is None: name = node
        else: name = f"{node}.{index}"
        rs = self.Resistor(name, self.gnd, node, resistance)
        # print(rs)
        return rs

    def link(self, hexyo, hexye, resistance):
        name = self.conn2code(hexyo, hexye)
        nodeo = self.tup2code(hexyo); nodee = self.tup2code(hexye)
        ln = self.Resistor(name, nodeo, nodee, resistance)
        # print(ln)
        return ln

    def simulate(self):
        print("========== SIMULATE =============== >>")
        simulator = self.simulator()
        analysis = simulator.operating_point()
        for node in analysis.nodes.values():
            xy = self.code2tup(str(node))
            sxy = f"{xy[0]},{xy[1]}"
            self.voltage[*xy] = float(node[0])
            val = float(node[0])
            print(str(node), "..", sxy, "..", round(val, 3), "V")
        print("========== SIMULATE =============== <<")
    def check_node(self, xy, y=None):
        if isinstance(y, int) and isinstance(xy, int):
            return self.voltage.get((xy, y), 0)
        elif isinstance(xy, str) and y is None:
            xy = self.code2tup(xy)
            return self.voltage.get(xy, 0)
        elif isinstance(xy, tuple) and y is None:
            return self.voltage.get(xy, 0)
        else: raise ValueError("args")

a = Analyzer()

u0 = a.supplier((0, 0), 0, 3)
u1 = a.supplier((0, 0), 1, 2)
r0 = a.effector((0, 0), 2, 10)
r1 = a.effector((0, 0), 3, 10)

l0 = a.link((0, 0), (1, 1), 0.1)
r2 = a.effector((1, 1), None, 10)

l1 = a.link((0, 0), (0, 1), 0.1)
l2 = a.link((0, 1), (1, 1), 0.1)

# r3 = a.effector((0, 1), None, 10)

l3 = a.link((0, 0), (1, 0), 0.1)
l4 = a.link((1, 0), (1, 1), 0.1)

a.simulate()

print("effector 1,1:", a.check_node(1, 1), "V")
print("effector b1:", a.check_node("b1"), "V")




a.show_suppliers()
a.show_effectors()

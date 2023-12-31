library0 = {
    "settings": {
        "view-method": "equal-or-lower",
        "view-resolution": 0.1,
        "difficulty-method": "random",
        "modules-for-power": 8,
        "power-by-nuke": 14,
        "energy-recovery": 0.25,
        "anti-rockets": 2,
    },
    "technologies": [
        "intergrid-transformation",
        "energy-recovery", "construction-recovery", "build-recycling", 
        "advanced-mining", "advanced-processing", "resource-compresion",
        "extended-rnd-department", "sensor-system", "fast-transsmition",
        "passive-armor", "explosively-formed-projectile", "marketing campaign", 
        "multiple-targets", "missile-salvo", "centralized-command-system",
        "satellite-positioning-system", "anti-missile-system",        
    ],
    "players": {
        "Aaa": {
            "color": [1.0, 1.0, 0.5, 1.0],
        },
        "Bbb": {
            "color": [0.5, 1.0, 1.0, 1.0],
        }
    },
    "resources": {
        "A": {"color": [0.9, 0.2, 0.15]},
        "B": {"color": [0.15, 0.8, 0.1]},
        "C": {"color": [0.25, 0.5, 1.0]},
        "AB": {"color": [1.0, 0.85, 0.1], "process": {"A": 1, "B": 1}},
        "AC": {"color": [1.0, 0.45, 1.0], "process": {"A": 1, "C": 1}},
        "BC": {"color": [0.1, 0.9, 0.9], "process": {"C": 1, "B": 1}}
    },
    "objects": {
        "mine": {"shape": "mine-0", "modules": 2, "interval": 3, "range": 0},
        "mixer": {"shape": "mixer-0", "modules": 2, "interval": 3, "range": 0},
        "store": {"shape": "store-0", "modules": 2, "interval": 3, "range": 8},
        "nuke": {"shape": "nuke-0", "modules": 8, "interval": 6, "range": 0},
        "post": {"shape": "post-0", "modules": 1, "interval": 2, "range": 0},
        "lab":  {"shape": "lab-0", "modules": 2, "interval": 3, "range": 0, "substracts": ["AC", "BC"]},
        "devel": {"shape": "devel-0", "modules": 3, "interval": 3, "range": 8, "substracts": ["AB", "AB"]},
        "send": {"shape": "send-0", "modules": 2, "interval": 4, "range": 0, "substracts": ["BC"]},
        "hit": {"shape": "hit-0", "modules": 3, "interval": 4, "range": 30, "substracts": ["AC"]},
    },
    "terrains": {
 	"desert-0":       {"color": [1.0, 0.95, 0.93], "buildable": True, "level": 0, "risk": 0.0, "desc": "desert", "resources":{}},
	"deposit-c-0":   {"color": [0.8, 0.8, 0.9],   "buildable": True, "level": 0, "risk": 0.0, "desc": "deposit", "resources":{"C": 0.333}},
	"deposit-ab-0":     {"color": [0.9, 0.9, 0.7],   "buildable": True, "level": 0, "risk": 0.0, "desc": "deposit", "resources":{"A": 0.2, "B": 0.25}},
        "tectonic-fault-0":{"color": [0.9, 0.82, 0.8],   "buildable": True, "level": 0, "risk": 0.0277777, "desc": "tectonic-fault", "resources":{}},
        "crater-crown-0":  {"color": [1.0, 0.8, 0.8],   "buildable": False, "level": 1, "risk": 0.0, "desc": "crater-crown", "resources":{}},
	"toxic-sea-0":    {"color": [0.55, 0.9, 0.9],   "buildable": False, "level": 0, "risk": 0.0, "desc": "toxic-sea", "resources":{}},
    },
}
battlefield0 = {
    "iteration": 0,
    "difficulty": 2,
    "links": [
        ("A", (55, -67), (52, -71)),
        ("A", (58, -66), (52, -71)),
        ("A", (52, -71), (45, -70)),
        ("A", (45, -70), (38, -69)),
        ("A", (38, -69), (37, -63)),
        ("A", (38, -69), (32, -66)),
        ("C", (32, -59), (37, -63)),
        ("C", (32, -59), (32, -66)),
        ("C", (31, -52), (32, -59)),
        ("C", (30, -45), (31, -52)),
        ("C", (27, -40), (30, -45)),
        ("C", (31, -38), (30, -45)),
        ("AC", (37, -63), (42, -60)),
        ("AC", (42, -60), (49, -59)),
        ("AC", (49, -59), (54, -53)),
        ("AC", (54, -53), (52, -46)),
        ("AC", (52, -46), (50, -39)),
        ("AC", (54, -53), (59, -47)),
        ("AC", (59, -47), (64, -41)),
        ("AC", (59, -47), (65, -51)),
        ("AC", (65, -51), (71, -47)),

        ("AC", (32, -66), (25, -63)),
        ("AC", (25, -63), (23, -56)),
        ("AC", (23, -56), (21, -49)),
        ("AC", (21, -49), (19, -42)),
        
        ("AC", (19, -42), (12, -40)),
        ("AC", (12, -40), (5, -38)),
        ("AC", (19, -42), (21, -35)),
        ("AC", (24, -28), (30, -23)),
        ("AC", (21, -35), (16, -31)),
        ("AC", (21, -35), (24, -28))
    ],
    "objects": [
        {"xy": (76, 100), "name": "mine", "own": "Aaa", "cnt": 2, "armor": False, "out": None},
        {"xy": (70, 101), "name": "mine", "own": "Aaa", "cnt": 2, "armor": False, "out": None},
        {"xy": (68, 90), "name": "devel", "own": "Aaa", "cnt": 3, "armor": False, "work": False},
        {"xy": (70, 96), "name": "store", "own": "Aaa", "cnt": 2, "armor": False, "work": False, "goods": []},
        {"xy": (68, 86), "name": "store", "own": "Aaa", "cnt": 2, "armor": False, "work": False, "goods": []},
        {"xy": (72, 92), "name": "mixer", "own": "Aaa", "cnt": 2, "armor": False, "out": None},
        {"xy": (63, 95), "name": "nuke", "own": "Aaa", "cnt": 8},
        
        {"xy": (-11, -64), "name": "nuke", "own": "Bbb", "cnt": 8},
        {"xy": (0, -64), "name": "nuke", "own": "Bbb", "cnt": 8},
        {"xy": (55, -67), "name": "mine", "own": "Bbb", "cnt": 2, "armor": True, "out": "A"},
        {"xy": (58, -66), "name": "mine", "own": "Bbb", "cnt": 2, "armor": True, "out": "A"},
        {"xy": (52, -71), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["A", "A", "A", "A"]},
        {"xy": (45, -70), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["A", "A", "A", "A"]},
        {"xy": (38, -69), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["A", "A", "A", "A"]},
        {"xy": (27, -40), "name": "mine", "own": "Bbb", "cnt": 2, "armor": True, "out": "C"},
        {"xy": (31, -38), "name": "mine", "own": "Bbb", "cnt": 2, "armor": True, "out": "C"},
        {"xy": (30, -45), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["C", "C", "C", "C"]},
        {"xy": (31, -52), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["C", "C", "C", "C"]},
        {"xy": (32, -59), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["C", "C", "C", "C"]},
        {"xy": (37, -63), "name": "mixer", "own": "Bbb", "cnt": 2, "armor": False, "out": "AC"},
        {"xy": (32, -66), "name": "mixer", "own": "Bbb", "cnt": 2, "armor": False, "out": "AC"},
        {"xy": (42, -60), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (49, -59), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (54, -53), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (59, -47), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (65, -51), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (52, -46), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (64, -41), "name": "hit", "own": "Bbb", "cnt": 3, "armor": True, "work": True},
        {"xy": (71, -47), "name": "hit", "own": "Bbb", "cnt": 3, "armor": True, "work": True},
        {"xy": (50, -39), "name": "hit", "own": "Bbb", "cnt": 3, "armor": True, "work": True},
        {"xy": (25, -63), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (23, -56), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (21, -49), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (19, -42), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (21, -35), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (24, -28), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (12, -40), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["AC", "AC", "AC", "AC"]},
        {"xy": (5, -38), "name": "hit", "own": "Bbb", "cnt": 3, "armor": True, "work": True},
        {"xy": (30, -23), "name": "hit", "own": "Bbb", "cnt": 3, "armor": True, "work": True},
        {"xy": (16, -31), "name": "hit", "own": "Bbb", "cnt": 3, "armor": True, "work": True},
    ],
    "players": {
        "Aaa": {
            "send": 0,
            "losses": 0,
            "trophy": 0,
            "research": 0,
            "technologies": ["build-recycling"],
            "power-share": {},
            "view-share": []
        },
        "Bbb": {
            "send": 0,
            "losses": 0,
            "trophy": 0,
            "research": 0,
            "technologies": ["intergrid-transformation",
                             "passive-armor"],
            "power-share": {},
            "view-share": []
        }
    },
    "terrains": [
        ("base", "desert-0"),
        ("polygon", "crater-crown-0", (-14.92, 13.48), (-13.71, 13.8), (-13.52, 15.41), (-14.8, 14.95),),
        ("polygon", "crater-crown-0", (-14.94, 14.87), (-15.05, 16.33), (-14.23, 17.25), (-12.55, 17.96), (-10.65, 18.17), (-10.76, 16.6), (-11.74, 14.97),),
        ("polygon", "crater-crown-0", (-14.68, 15.06), (-14.38, 13.46), (-14.24, 11.27), (-15.94, 10.04), (-17.9, 9.44), (-18.67, 12.4), (-17.37, 14.2),),
        ("polygon", "crater-crown-0", (-20.99, 7.27), (-23.83, 6.04), (-24.66, 4.1), (-24.33, 1.39), (-22.35, 1.35), (-21.12, 3.24), (-20.24, 5.17),),
        ("polygon", "crater-crown-0", (-7.81, 20.1), (-7.42, 20.76), (-6.37, 21.86), (-4.39, 22.47), (-1.06, 21.46), (0.3, 19.88), (-1.58, 18.79), (-5.14, 19.01),),
        ("polygon", "crater-crown-0", (-1.72, 21.04), (-4.05, 21.7), (-5.07, 24.64), (-1.54, 25.89), (4.16, 27.21), (12.01, 25.95), (13.21, 25.0), (12.43, 24.46), (6.37, 22.3), (1.58, 21.52),),
        ("polygon", "crater-crown-0", (-24.08, 2.59), (-26.98, 0.69), (-28.3, -1.3), (-28.55, -7.26), (-26.4, -9.66), (-22.92, -5.93), (-22.42, -1.55),),
        ("polygon", "crater-crown-0", (15.68, 30.73),(19.48, 28.13), (23.13, 27.08), (27.55, 27.08), (29.76, 28.48), (31.66, 30.38), (29.91, 33.19), (24.81, 33.26),(19.76, 32.21),),
        ("polygon", "crater-crown-0", (7.98, 31.36), (10.16, 31.87), (11.38, 32.71), (8.88, 33.55), (5.73, 32.84),),
        ("polygon", "crater-crown-0", (-32.05, -10.81), (-29.07, -13.39), (-27.29, -17.95), (-28.28, -24.29), (-29.87, -25.88), (-33.44, -20.33), (-34.72, -14.87),),
        ("polygon", "crater-crown-0", (28.49, 29.22), (31.25, 31.43), (35.75, 32.45), (40.87, 31.03), (46.24, 25.83), (46.95, 22.04), (44.5, 21.17), (35.51, 22.91), (31.73, 25.2),),
        ("polygon", "crater-crown-0", (49.7, 22.1), (52.9, 23.3), (55.96, 22.1), (61.96, 17.57), (62.62, 14.24), (60.62, 11.58), (51.97, 14.11),),
        ("polygon", "crater-crown-0", (58.69, 13.08), (56.78, 10.57), (58.1, 7.47), (60.76, 2.16), (62.83, 0.38), (65.34, 3.78), (67.26, 9.09), (61.2, 13.52),),
        ("polygon", "crater-crown-0", (70.62, -20.61), (70.76, -17.57), (75.03, -14.13), (84.41, -12.75), (91.17, -16.47), (88.97, -22.54), (80.14, -22.95),),
        ("polygon", "crater-crown-0", (78.11, -20.93), (80.21, -21.92), (81.75, -26.23), (80.1, -30.75), (74.25, -36.16), (71.38, -36.16), (71.05, -30.97), (73.47, -25.57),),
        ("polygon", "crater-crown-0", (66.76, -1.86), (68.63, 3.6), (73.08, 5.47), (74.95, 4.75), (74.66, 0.44), (68.47, -4.73),),
        ("polygon", "crater-crown-0", (71.56, -39.33), (73.73, -39.22), (74.35, -40.78), (72.8, -42.22), (68.15, -42.95), (68.25, -40.98),),
        ("polygon", "crater-crown-0", (69.11, -41.88), (66.8, -42.15), (65.34, -42.9), (64.23, -46.76), (65.03, -48.05), (67.11, -46.36), (69.28, -42.95),),
        ("polygon", "crater-crown-0", (61.4, -52.32), (56.0, -52.89), (51.29, -55.54), (50.71, -58.18), (53.93, -59.56), (59.44, -58.64), (62.78, -55.31),),
        ("polygon", "crater-crown-0", (88.62, -9.26), (91.93, -11.47), (103.57, -13.68), (119.63, -12.82), (124.29, -9.26), (120.98, -6.32), (108.6, -2.52), (100.02, -3.01), (91.44, -5.22),),
        ("polygon", "crater-crown-0", (43.58, -59.91), (47.35, -59.24), (49.71, -60.05), (50.53, -60.87), (47.94, -63.9), (40.99, -63.6), (36.18, -61.68),),
        ("polygon", "crater-crown-0", (23.98, 36.22), (29.18, 35.85), (31.97, 37.43), (30.85, 40.68), (19.14, 46.16), (15.24, 45.33), (13.29, 42.54), (15.05, 39.29),),
        ("polygon", "crater-crown-0", (16.99, 43.65), (15.79, 43.78), (11.27, 47.4), (4.8, 55.42), (4.03, 60.2), (6.1, 65.25), (10.75, 67.06), (16.83, 64.99), (18.87, 56.07), (18.71, 49.47),),
        ("polygon", "crater-crown-0", (-111.07, -36.93), (-99.93, -31.9), (-95.26, -24.36), (-102.45, -19.33), (-111.97, -22.13), (-116.17, -29.52),),        
        ("polygon", "crater-crown-0", (31.29, -121.11), (31.25, -116.96), (38.12, -105.68), (49.15, -103.23), (55.47, -108.62), (51.85, -118.29),),
        ("polygon", "crater-crown-0", (68.63, 76.58), (74.97, 76.78), (83.14, 82.09), (89.26, 93.12), (83.75, 100.07), (73.13, 93.33),),
        ("polygon", "crater-crown-0", (4.55, 70.09), (8.52, 71.64), (7.85, 74.16), (4.55, 75.81), (3.68, 73.78),),
        ("polygon", "crater-crown-0", (129.53, -12.34), (132.42, -10.96), (136.21, -11.37), (138.77, -13.31), (135.87, -14.0),),
        ("polygon", "crater-crown-0", (-103.02, 45.75), (-107.83, 49.42), (-106.13, 59.89), (-99.91, 64.41), (-91.99, 60.45), (-89.44, 50.27),),
        ("polygon", "crater-crown-0", (148.59, -60.98), (149.41, -56.48), (152.89, -53.0), (162.71, -52.8), (165.57, -60.36), (163.94, -67.93), (155.55, -69.98),),

        ("polygon", "toxic-sea-0", (-30.82, -54.4), (-24.36, -45.67), (-13.04, -36.94), (0.05, -38.39), (5.22, -49.87), (-6.9, -60.21), (-20.64, -63.29),),
        ("polygon", "toxic-sea-0", (-26.39, -50.72), (-36.81, -48.46), (-50.37, -50.34), (-67.19, -59.76), (-77.48, -74.7), (-72.97, -80.22), (-56.77, -76.2), (-42.58, -67.92), (-28.15, -56.37),),
        ("polygon", "toxic-sea-0", (-27.76, -53.57), (-71.76, -76.43), (-75.76, -92.14), (-71.04, -98.14), (-51.05, -98.99), (-30.62, -91.71), (-13.19, -77.85), (-14.33, -61.43),),
        ("polygon", "toxic-sea-0", (-96.6, -93.97), (-107.59, -137.13), (-78.55, -165.9), (-56.06, -164.33), (-36.44, -140.01), (-34.87, -113.59), (-38.68, -90.11),),
        ("polygon", "toxic-sea-0", (-50.23, -96.03), (-58.05, -160.53), (-51.8, -175.26), (-16.53, -170.13), (6.01, -150.27), (6.9, -115.0), (-13.21, -77.4),),
        ("polygon", "toxic-sea-0", (-56.24, -57.56), (-90.61, -49.89), (-107.54, -57.3), (-116.53, -82.95), (-100.4, -102.52), (-64.43, -94.58),),

        ("polygon", "deposit-ab-0", (-2.45, 34.02), (-3.42, 34.02), (-4.61, 34.59), (-3.29, 35.52), (-2.27, 35.65), (-0.46, 35.34),),
        ("polygon", "deposit-ab-0", (-1.43, 37.6), (-0.32, 36.87), (1.34, 36.91), (3.12, 37.64), (0.7, 38.84), (-0.03, 38.65),),
        ("polygon", "deposit-ab-0", (-3.3, 43.49), (-2.03, 43.49), (-0.37, 44.54), (-1.49, 45.16), (-3.48, 45.23), (-5.22, 44.98),),
        ("polygon", "deposit-ab-0", (-1.74, 49.83), (-0.4, 49.83), (0.8, 51.53), (-1.18, 52.73), (-3.93, 52.09),),
        ("polygon", "deposit-ab-0", (-38.59, -5.93), (-36.16, -5.85), (-36.43, -2.54), (-39.53, -2.22), (-40.6, -3.56),),

        ("polygon", "deposit-ab-0", (76.01, 98.8), (77.94, 99.55), (78.39, 100.89), (76.6, 102.38), (73.58, 100.74),),
        ("polygon", "deposit-ab-0", (176.66, 41.79), (174.49, 44.93), (176.18, 47.58), (179.55, 45.65), (180.28, 43.48),),
        ("polygon", "deposit-ab-0", (68.88, 99.94), (68.79, 101.11), (70.2, 101.6), (72.55, 101.31), (70.95, 99.63),),
        
        ("polygon", "deposit-ab-0", (94.99, -23.29), (95.71, -23.29), (96.75, -23.72), (96.2, -24.33), (94.67, -24.38), (93.4, -23.67),),
        ("polygon", "deposit-ab-0", (85.76, -25.13), (88.19, -25.13), (90.79, -25.67), (89.46, -26.64), (85.94, -26.95), (84.19, -25.92),),
        ("polygon", "deposit-ab-0", (53.4, -67.98), (55.11, -65.67), (58.12, -64.67), (58.73, -66.58), (59.72, -69.68), (57.84, -69.84),),
        ("polygon", "deposit-ab-0", (94.78, -19.67), (95.91, -17.75), (98.28, -17.24), (100.88, -18.09), (98.73, -19.5),),
        ("polygon", "deposit-ab-0", (107.26, -16.61), (109.04, -16.69), (110.98, -18.47), (107.33, -18.94),),
        
        ("polygon", "tectonic-fault-0", (32.25, -12.22), (39.39, -8.73), (41.29, -14.09), (40.39, -19.86), (25.77, -23.66),),
        ("polygon", "tectonic-fault-0", (3.97, -33.48), (5.97, -27.77), (10.97, -21.77), (29.97, -12.34), (34.83, -11.34), (33.11, -15.77), (24.26, -27.62),),
        ("polygon", "tectonic-fault-0", (30.37, -14.86), (30.22, -9.98), (34.02, -0.9), (40.15, 4.77), (44.65, 5.7), (44.96, 2.75), (44.96, -2.61), (42.86, -8.58),),
        ("polygon", "tectonic-fault-0", (58.87, 24.24), (60.19, 21.78), (65.3, 20.45), (75.24, 24.43), (81.49, 34.56), (83.01, 41.37), (72.21, 38.44), (60.95, 33.99), (58.87, 28.97),),
        ("polygon", "tectonic-fault-0", (76.34, 34.99), (75.96, 37.87), (75.59, 48.04), (82.62, 57.58), (90.53, 60.35), (98.19, 58.59), (98.06, 51.81), (93.92, 42.89), (80.74, 36.87),),
        ("polygon", "tectonic-fault-0", (96.33, 52.45), (90.96, 57.44), (97.14, 67.43), (109.06, 76.42), (121.6, 78.73), (125.66, 78.79), (124.72, 73.67), (107.25, 57.63),),
        ("polygon", "tectonic-fault-0", (80.47, 37.87), (93.3, 44.56), (100.55, 45.54), (126.91, 44.7), (129.0, 41.08), (124.95, 38.57), (105.99, 35.22), (80.89, 35.08),),
        ("polygon", "tectonic-fault-0", (109.72, 74.74), (123.93, 77.13), (137.99, 94.48), (143.53, 114.37), (141.28, 119.01), (135.75, 116.61), (112.27, 96.42), (108.83, 75.48),),
        ("polygon", "tectonic-fault-0", (125.08, 39.3), (126.28, 43.93), (143.85, 48.38), (165.1, 45.81), (179.07, 36.21), (176.67, 34.93), (143.93, 35.27),),
        ("polygon", "tectonic-fault-0", (18.86, -18.73), (23.77, -6.75), (29.76, -3.33), (35.67, -4.75), (32.43, -14.49),),
        ("polygon", "tectonic-fault-0", (112.96, 40.97), (124.9, 36.32), (147.27, 40.85), (127.35, 48.7),),

        ("polygon", "deposit-c-0", (25.7, 4.7), (26.34, 6.24), (28.13, 6.88), (28.96, 6.43), (28.2, 4.25),),
        ("polygon", "deposit-c-0", (1.71, -16.51), (2.14, -14.54), (4.18, -13.12), (6.37, -12.98), (6.37, -15.52), (5.17, -16.37),),
        ("polygon", "deposit-c-0", (27.29, -38.5), (29.1, -37.54), (31.34, -37.54), (30.8, -40.52), (26.54, -40.84),),
        ("polygon", "deposit-c-0", (49.8, -19.8), (51.29, -19.8), (53.74, -18.31), (53.53, -14.69), (50.12, -15.54),),
        ("polygon", "deposit-c-0", (25.27, -25.87), (25.75, -26.23), (28.87, -25.09), (31.04, -22.85), (30.75, -22.11), (27.2, -22.87),),
        ("polygon", "deposit-c-0", (15.57, -20.04), (15.16, -19.33), (16.8, -16.84), (19.82, -15.05), (20.42, -15.53), (19.56, -18.03),),

        ("polygon", "deposit-c-0", (70.79, 40.75), (72.49, 41.15), (72.89, 42.75), (70.59, 42.45), (69.29, 41.35),),
        ("polygon", "deposit-c-0", (86.67, 34.07), (88.67, 34.25), (90.67, 32.73), (88.79, 32.01), (86.19, 32.25),),
    ]
}

library0 = {
    "players": {
        "Aaa": {
            "color": [1.0, 1.0, 0.5],
        },
        "Bbb": {
            "color": [0.5, 1.0, 1.0],
        }
    },
    "resources": {
        "A": {"color": [1.0, 0.1, 0.1]},
        "B": {"color": [0.1, 0.8, 0.1]},
        "C": {"color": [0.1, 0.1, 1.0]},
        "AB": {"color": [1.0, 0.8, 0.1], "process": {"A": 1, "B": 1}},
        "AC": {"color": [1.0, 0.1, 1.0], "process": {"A": 1, "C": 1}},
        "BC": {"color": [0.1, 0.9, 0.9], "process": {"C": 1, "B": 1}}
    },
    "objects": {
        "mine": {"shape": "mine-0", "modules": 2, "interval": 3, "range": 0},
        "mixer": {"shape": "mixer-0", "modules": 2, "interval": 3, "range": 0},
        "store": {"shape": "store-0", "modules": 2, "interval": 3, "range": 6},
        "devel": {"shape": "devel-0", "modules": 3, "interval": 3, "range": 6},
        "send": {"shape": "send-0", "modules": 2, "interval": 4, "range": 0},
        "nuke": {"shape": "nuke-0", "modules": 8, "interval": 6, "range": 0},
        "lab": {"shape": "lab-0", "modules": 2, "interval": 3, "range": 0},
        "hit": {"shape": "hit-0", "modules": 3, "interval": 4, "range": 20},
    },
    "terrains": {
 	"desert-0":       {"color": [1.0, 0.95, 0.93], "buildable": True, "level": 0, "risk": 0.0, "desc": "desert", "resources":{}},
	"deposit-ab-0":   {"color": [0.9, 0.9, 0.9],   "buildable": True, "level": 0, "risk": 0.0, "desc": "deposit", "resources":{"C": 0.3}},
	"deposit-c-0":     {"color": [0.9, 0.9, 0.9],   "buildable": True, "level": 0, "risk": 0.0, "desc": "deposit", "resources":{"A": 0.1, "B": 0.15}},
        "tectonic-fault-0":{"color": [0.9, 0.82, 0.8],   "buildable": True, "level": 0, "risk": 0.0277777, "desc": "tectonic-fault", "resources":{}},
        "crater-crown-0":  {"color": [1.0, 0.8, 0.8],   "buildable": False, "level": 1, "risk": 0.0, "desc": "crater-crown", "resources":{}},
	"toxic-sea-0":    {"color": [0.4, 1.0, 1.0],   "buildable": False, "level": 0, "risk": 0.0, "desc": "toxic-sea", "resources":{}},
    },
}
battlefield0 = {
    "iteration": 0,
    "radiation": 3,
    "objects": [
        [(10, 5), "mixer", "Aaa", 2, "AC"],
        [(13, 2), "mixer", "Aaa", 1, "AB"],
        [(15, 5), "store", "Aaa", 0, ["AC", "BC", "AB", "A", "B", "C"]],
        [(14, 8), "store", "Aaa", 1, ["AC", "AC", "AC", "A"]],
        [(17, 8), "store", "Aaa", 2, []],
        [(20, 9), "mine", "Aaa", 1, "A"],
        [(6, 12), "nuke", "Aaa", 5],
        [(14, 12), "lab", "Aaa", 1],
        [(16, 16), "hit", "Aaa", 3],
        [(20, 16), "devel", "Aaa", 3],
        [(24, 16), "send", "Aaa", 2],
    ],
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
    ]
}


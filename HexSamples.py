
library_0 = {
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
        "passive-armor", "explosively-formed-projectile", "marketing-campaign", 
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
 	"desert-0":      {"color": [1.0, 0.95, 0.93], "buildable": True, "level": 0, "risk": 0.0, "desc": "desert", "resources":{}},
	"deposit-c-0":   {"color": [0.8, 0.8, 0.9],   "buildable": True, "level": 0, "risk": 0.0, "desc": "deposit", "resources":{"C": 0.333}},
	"deposit-ab-0":  {"color": [0.9, 0.9, 0.7],   "buildable": True, "level": 0, "risk": 0.0, "desc": "deposit", "resources":{"A": 0.2, "B": 0.25}},
        "tectonic-fault-0":{"color": [0.9, 0.82, 0.8], "buildable": True, "level": 0, "risk": 0.0277777, "desc": "tectonic-fault", "resources":{}},
        "crater-crown-0":  {"color": [1.0, 0.8, 0.8],  "buildable": False, "level": 1, "risk": 0.0, "desc": "crater-crown", "resources":{}},
	"toxic-sea-0":    {"color": [0.55, 0.9, 0.9],  "buildable": False, "level": 0, "risk": 0.0, "desc": "toxic-sea", "resources":{}},
    },
}

battlefield_0 = {
    "iteration": 0,
    "difficulty": 2,
    "links": [
    ],
    "objects": [
        {"xy": (-2, -2), "name": "nuke", "own": "Bbb", "cnt": 8},
        {"xy": (2, 2), "name": "mine", "own": "Aaa", "cnt": 2, "armor": False, "out": None},
        {"xy": (3, 3), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["A", "A", "A", "A"]},
        {"xy": (4, 3), "name": "store", "own": "Bbb", "cnt": 2, "armor": False, "work": True, "goods": ["A", "B", "C", "AB", "AC", "BC"]},
        {"xy": (4, 4), "name": "mixer", "own": "Bbb", "cnt": 2, "armor": False, "out": "AC"},
        {"xy": (5, 5), "name": "hit", "own": "Bbb", "cnt": 3, "armor": True, "work": True},
        {"xy": (7, 5), "name": "devel", "own": "Aaa", "cnt": 3, "armor": False, "work": False},
        {"xy": (7, 9), "name": "send", "own": "Aaa", "cnt": 2, "armor": False, "work": False},
        {"xy": (9, 5), "name": "post", "own": "Aaa", "cnt": 1, "armor": True},
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
        ("vex", "crater-crown-0", (0, 0), 2),
        ("vex", "crater-crown-0", (1, 0), 2),
        ("vex", "crater-crown-0", (1, 1), 2),
        ("grid", (0.5, 0.5, 0.5), 2)
    ]
}


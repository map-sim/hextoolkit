###
### settings
###

settings_0 = {
    'current-turn': 0,
    'window-title': 'main-window',
    'window-size': (1100, 1050),
    'window-offset': (740, 225),
    'window-zoom': 15.0,
    'move-sensitive': 50,
    'hex-radius': 2.2,
    'base-thickness': 0.08,
    'marker-color': (1.0, 1.0, 0.3),
    'show-markers': False,
    'display-length': 22,
    'devel-free-impact': 0.1,
    'devel-unit-impact': 0.08
}

builds_0 = {
    "plant": {
        "cost": 100,
        "strength": 80,
        "costal": False,
        "range": 30,
        "power": 20,
    },
    "supply": {
        "cost": 50,
        "strength": 20,
        "costal": False,
        "off-grid": 0.0,
        "power": -3,
    },
    "unit": {
        "cost": 40,
        "strength": 10,
        "costal": False,
        "off-grid": 0.5,
        "power": -1,
    },
    "link": {
        "cost": 10,
        "costal": True,
        "strength": 60,
        "power": 0,
    },
    "seahub": {
        "cost": 50,
        "strength": 90,
        "costal": True,
        "off-grid": 0.5,
        "power": -1,
    },
    "airhub": {
        "cost": 40,
        "strength": 50,
        "costal": False,
        "off-grid": 0.4,
        "power": -1,
    },
    "fort": {
        "cost": 30,
        "costal": False,
        "strength": 200,
        "power": 0,
    }
}

units_0 = {
    "supplying": {
        "char": "S",
        "costal": -1,
        "type": "light",
        "max-size": 8,
        "cost": 20.0,
        "speed": 1.5,
        "supply": 1.0,
        "shot-range": 0.0,
        "stock-form": "mech",
        "stock-2nd": "mech",
        "action-cost": {
            "move": (0.5, 0.01),
            "supply": (1.0, 0.02),
            "defence": (0.75, 0.5),
            "storm": (0.75, 0.5),
            "devel": (1.0, 1.0),
        }
    },
    "engineering": {
        "char": "E",
        "costal": 1,
        "type": "light",
        "max-size": 2,
        "cost": 30.0,
        "speed": 0.5,
        "supply": 0.05,
        "costal": 1,
        "shot-range": 0.0,
        "stock-form": "mech",
        "stock-2nd": "devel",
        "action-cost": {
            "move": (0.5, 0.0),
            "supply": (1.0, 0.0),
            "defence": (1.0, 0.0),
            "storm": (1.5, 0.0),
            "devel": (1.0, 1.0),
        }
    },
    "special": {
        "char": "Q",
        "costal": 3,
        "type": "super-light",
        "max-size": 2,
        "cost": 50.0,
        "speed": 2.0,
        "supply": 0.03,
        "shot-range": 6.0,
        "stock-form": "special",
        "stock-2nd": "special",
        "action-cost": {
            "move": (0.5, 0.0),
            "supply": (1.0, 0.0),
            "defence": (1.0, 1.0),
            "storm": (1.5, 1.0),
            "shot": (0.2, 1.0),
            "devel": (1.0, 0.5),
        }
    },
    "motorized": {
        "char": "K",
        "costal": -1,
        "type": "light",
        "max-size": 8,
        "cost": 27.5,
        "speed": 1.0,
        "supply": 0.2,
        "shot-range": 4.0,
        "stock-form": "mech",
        "stock-2nd": "mech",
        "action-cost": {
            "move": (0.66, 0.1),
            "supply": (1.0, 0.2),
            "defence": (0.75, 0.66),
            "storm": (1.0, 1.0),
            "shot": (0.25, 0.5),
            "devel": (0.66, 0.5),
        }
    },
    "mechanized": {
        "char": "M",
        "costal": 4,
        "type": "heavy",
        "max-size": 8,
        "cost": 72.0,
        "speed": 0.9,
        "supply": 0.1,
        "shot-range": 5.0,
        "stock-form": "heavy",
        "stock-2nd": "heavy",
        "action-cost": {
            "move": (0.72, 0.1),
            "supply": (1.2, 0.2),
            "defence": (0.85, 0.66),
            "storm": (1.35, 1.5),
            "shot": (0.35, 0.7),
        }
    },
    "armored": {
        "char": "T",
        "costal": 4,
        "type": "heavy",
        "max-size": 8,
        "cost": 100.0,
        "speed": 0.4,
        "supply": 0.0,
        "shot-range": 5.33,
        "stock-form": "heavy",
        "stock-2nd": "heavy",
        "action-cost": {
            "move": (1.2, 0.05),
            "defence": (1.5, 0.88),
            "storm": (2.25, 1.75),
            "shot": (0.4, 0.8),
        }
    },
    "artillery": {
        "char": "A",
        "costal": -1,
        "type": "heavy",
        "max-size": 4,
        "cost": 80.0,
        "speed": 0.5,
        "supply": 0.0,
        "shot-range": 12.0,
        "stock-form": "heavy",
        "stock-2nd": "heavy",
        "action-cost": {
            "move": (0.8, 0.05),
            "defence": (0.5, 0.88),
            "storm": (0.75, 0.75),
            "shot": (0.5, 1.2),
        }
    },
    "helicopter": {
        "char": "H",
        "costal": -1,
        "type": "helicopter",
        "max-size": 4,
        "cost": 180.0,
        "speed": 4.5,
        "supply": 1.0,
        "shot-range": 4.0,
        "type": "navigable",
        "stock-form": "aviate",
        "stock-2nd": "aviate",
        "action-cost": {
            "move": (0.8, 0.05),
            "supply": (1.0, 0.02),
            "storm": (0.75, 0.75),
            "defence": (0.5, 0.88),
            "shot": (0.5, 1.2),
        }
    },
    "cutter": {
        "char": "C",
        "costal": 0,
        "type": "navy",
        "max-size": 1,        
        "cost": 280.0,
        "speed": 0.1,
        "supply": 5.0,
        "shot-range": 4.0,
        "stock-form": "seatech",
        "stock-2nd": "seatech",
        "action-cost": {
            "move": (0.8, 0.05),
            "supply": (1.0, 0.02),
            "defence": (0.5, 0.88),
            "transport": (0.66, 0.2),
            "storm": (0.75, 0.75),
            "shot": (0.5, 1.2),
        }
    }
}

###
### xsystem
###

xsystem_0 = {
    "supplying": {},
    "engineering": {},
    "special": {},
    "motorized": {},
    "mechanized": {},
    "armored": {
        "building": 1.5,
        "supplying": 1.1,
        "engineering": 0.99,
        "motorized": 0.95,
        "special": 0.9,
        "mechanized": 0.75,
        "armored": 0.6,
        "artillery": 1.0,
        "cutter": 0.75,
    },
    "artillery": {
        "building": 1.5,
        "supplying": 1.0,
        "engineering": 0.92,
        "motorized": 0.9,
        "special": 0.85,
        "mechanized": 0.8,
        "armored": 0.75,
        "artillery": 0.5,
        "cutter": 1.0,
    },
    "cutter": {},
    "helicopter": {}
}

###
### landform
###

landform_0 = [
    ('base', 'water-0'),
    ('vex', 'steppe-0', (-3, 2)),
    ('vex', 'steppe-0', (-4, 1)),
    ('vex', 'steppe-0', (-2, 2)),
    ('vex', 'steppe-0', (-3, 0)),
    ('vex', 'steppe-0', (-3, 1)),
    ('vex', 'desert-0', (-3, -1)),
    ('vex', 'desert-0', (-2, -1)),
    ('vex', 'desert-0', (-1, -1)),
    ('vex', 'desert-0', (-1, -2)),
    ('vex', 'steppe-0', (0, -2)),
    ('vex', 'steppe-0', (0, -1)),
    ('vex', 'steppe-0', (0, -3)),
    ('vex', 'steppe-0', (1, -3)),
    ('vex', 'desert-0', (2, -3)),
    ('vex', 'desert-0', (0, 0)),
    ('vex', 'desert-0', (-1, 0)),
    ('vex', 'desert-0', (-2, 1)),
    ('vex', 'desert-0', (0, 3)),
    ('vex', 'desert-0', (1, 3)),
    ('vex', 'desert-0', (1, 2)),
    ('vex', 'desert-0', (-1, 3)),
    ('vex', 'desert-0', (0, 1)),
    ('vex', 'desert-0', (0, 4)),
    ('vex', 'desert-0', (1, 1)),
    ('vex', 'steppe-0', (2, 2)),
    ('vex', 'steppe-0', (2, 3)),
    ('vex', 'desert-0', (1, -1)),
    ('vex', 'steppe-0', (1, -2)),
    ('vex', 'desert-0', (2, -1)),
    ('vex', 'hills-0', (2, -2)),
    ('vex', 'desert-0', (3, 0)),
    ('vex', 'steppe-0', (3, 1)),
    ('vex', 'steppe-0', (4, 2)),
    ('vex', 'steppe-0', (4, 3)),
    ('vex', 'steppe-0', (5, 2)),
    ('vex', 'steppe-0', (4, 1)),
    ('vex', 'steppe-0', (-4, 2)),
    ('vex', 'desert-0', (3, -1)),
    ('vex', 'desert-0', (3, -2)),
    ('vex', 'desert-0', (4, -1)),
    ('vex', 'desert-0', (5, 0)),
    ('vex', 'shallows-0', (3, 3)),
    ('vex', 'shallows-0', (3, 2)),
    ('vex', 'shallows-0', (1, 4)),
    ('vex', 'shallows-0', (2, 4)),
    ('vex', 'shallows-0', (3, 4)),
    ('vex', 'shallows-0', (1, 0)),
    ('vex', 'shallows-0', (2, 0)),
    ('vex', 'shallows-0', (2, 1)),
    ('vex', 'shallows-0', (2, 5)),
    ('vex', 'shallows-0', (3, 5)),
    ('vex', 'shallows-0', (4, 4)),
    ('vex', 'shallows-0', (-3, 3)),
    ('vex', 'shallows-0', (-2, 3)),
    ('vex', 'shallows-0', (-2, -2)),
    ('vex', 'shallows-0', (-3, -2)),
    ('vex', 'shallows-0', (-4, -1)),
    ('vex', 'shallows-0', (-4, 0)),
    ('vex', 'hills-0', (4, 0)),
    ('vex', 'hills-0', (-2, 0)),
    ('vex', 'hills-0', (-1, 2)),
    ('vex', 'hills-0', (-1, 1)),
    ('vex', 'hills-0', (0, 2)),
    ('grid', (0.9, 0.9, 0.9), 0.16),
    ('grid', (0.6, 0.6, 0.6), 0.08)
]

###
### controls
###

controls_0 = {
    "Aaa": {
        "base-color": [0.1, 0.8, 0.1],
        "unit-color": [0.5, 1.0, 0.5],
        "marker-color": [0.6, 1.0, 0.6],
        "population": 50
    },
    "Bbb": {
        "base-color": [0.9, 0.2, 0.2],
        "unit-color": [1.0, 0.5, 0.5],
        "marker-color": [1.0, 0.6, 0.6],
        "population": 60
    }
}

stats_0 = {
    # example
    # "group-0": {
    #     "qwerty": [1.4, 2.1, 9.2, 8.8, 0.4, 0.8],
    #     "abc": [2.2, 3.1, 12.2, 13.2, 1.2, 3.2]
    # },
    # "group-1": {
    #     "Aaa": [0.0, 1.4, 2.1, 9.2, 8.8],
    #     "Bbb": [0.0, 2.2, 3.1, 12.2, 13.2]
    # }
}

###
### goods / stocks
###

goods_0 = {
    "basic": {"drag": 0.5, "type": "basic"},
    "devel": {"drag": 10.2, "type": "devel"},
    "mech": {"drag": 1.5, "type": "regular"},
    "heavy": {"drag": 2.5, "type": "regular"},
    "seatech": {"drag": 4.5, "type": "regular"},
    "aviate": {"drag": 4.2, "type": "regular"}
}

###
### units
###

# orders: defense
#         move (target: hex)
#         supply (source: hex, target: hex)
#         storm (target: hex | index)
#         shot (target: hex | index | hex + index)

military_0 = {
    (2, 3): [
        {"own": "Aaa", "type": "mechanized", "size": 3, "state": 1.0, "exp": 1.2, "stock": (0.6, 0.5), "order": "shot", "to": (0, 2)},
        {"own": "Aaa", "type": "motorized", "size": 2, "state": 1.0, "exp": 1.5, "stock": (0.6, 0.5), "order": "shot", "to": (1, 2, 0)},
        {"own": "Aaa", "type": "motorized", "size": 3, "state": 1.0, "exp": 1.9, "stock": (0.6, 0.5), "order": "shot", "to": 3},
        {"own": "Aaa", "type": "motorized", "size": 3, "state": 1.0, "exp": 1.7, "stock": (0.6, 0.5), "order": "defence"}
    ],
    (2, 2): [
        {"own": "Aaa", "type": "supplying", "size": 2, "state": 1.0, "exp": 1.2, "stock": (0.6, 0.0), "order": "defence"},
        {"own": "Aaa", "type": "motorized", "size": 2, "state": 1.0, "exp": 1.3, "stock": (0.6, 0.5), "order": "defence"}
    ],
    (1, 1): [
        {"own": "Aaa", "type": "mechanized", "size": 1, "state": 1.0, "exp": 1.6, "stock": (0.6, 0.5), "order": "defence"},
        {"own": "Aaa", "type": "mechanized", "size": 1, "state": 1.0, "exp": 1.1, "stock": (0.6, 0.5), "order": "regroup", "progress": 0.9}
    ],
    (-2, 2): [
        {"own": "Bbb", "type": "motorized", "size": 1, "state": 0.4, "exp": 1.2, "stock": (0.66, 0.66), "order": "storm", "to": (-1, 2)},
        {"own": "Bbb", "type": "motorized", "size": 1, "state": 1.0, "exp": 1.6, "stock": (0.75, 0.6), "order": "storm", "to": 2}
    ],
    (-3, 0): [
        {"own": "Bbb", "type": "engineering", "size": 1, "state": 0.4, "exp": 1.7, "stock": (0.66, 0.66), "order": "storm", "to": (-1, 2)},
        {"own": "Bbb", "type": "supplying", "size": 1, "state": 1.0, "exp": 1.8, "stock": (0.75, 0.6), "order": "storm", "to": 2}
    ],
    (4, 1): [
        {"own": "Aaa", "type": "special", "size": 1, "state": 1.0, "exp": 1.9, "stock": (0.6, 0.5), "order": "shot", "to": (-3, 2, 0)},
        {"own": "Aaa", "type": "special", "size": 1, "state": 1.0, "exp": 1.8, "stock": (0.6, 0.5), "order": "shot", "to": (-3, 2, 1)},
        {"own": "Aaa", "type": "special", "size": 1, "state": 1.0, "exp": 1.7, "stock": (0.6, 0.5), "order": "shot", "to": (-3, 2, 2)},
        {"own": "Aaa", "type": "special", "size": 1, "state": 1.0, "exp": 1.6, "stock": (0.6, 0.5), "order": "shot", "to": (-3, 2, 3)},
        {"own": "Aaa", "type": "special", "size": 1, "state": 1.0, "exp": 1.5, "stock": (0.6, 0.5), "order": "shot", "to": (-3, 2, 4)},
        {"own": "Aaa", "type": "special", "size": 1, "state": 1.0, "exp": 1.4, "stock": (0.6, 0.5), "order": "shot", "to": (-3, 2, 5)}
    ],
    (0, 1): [
        {"own": "Bbb", "type": "armored", "size": 2, "state": 1.0, "exp": 1.3, "stock": (0.75, 0.6), "order": "move", "progress": 0.0, "to": [(1, 2), (0, 3)]}
    ],
    (-1, 1): [
        {"own": "Bbb", "type": "artillery", "size": 2, "state": 1.0, "exp": 1.3, "stock": (0.75, 0.6), "order": "move", "progress": 0.0, "to": [(1, 2), (0, 3)]}
    ],
    (-1, 6): [
        {"own": "Bbb", "type": "artillery", "size": 2, "state": 1.0, "exp": 1.2, "stock": (0.75, 0.6), "order": "defence"}
    ],
    (-3, 2): [
        {"own": "Bbb", "type": "engineering", "size": 2, "state": 1.0, "exp": 1.2, "stock": (0.75, 0.6), "order": "move", "progress": 0.0, "to": [(1, 2), (0, 3)]}
    ],
    (-1, 0): [
        {"own": "Bbb", "type": "supplying", "size": 2, "state": 1.0, "exp": 1.1, "stock": (0.5, 0.0), "order": "supply", "from": [(-3, 2), (-3, 1), (-2, 1)], "to": [(0, 0), (0, 1)]}
    ],
    (-5, 3): [
        {"own": "Bbb", "type": "cutter", "size": 1, "state": 1.0, "exp": 1.1, "stock": (0.5, 0.5), "order": "transport", "progress": 0.5, "unit": 0, "from": [(-3, 2), (-4, 2)], "to": [(-4, 2), (-4, 1)]}
    ]
}

###
### infrastructure
###
# common: type, own, build
# --------------- no slot needed:
# fort: stock, state(in, out, io)
# link: stock, state(in, out, io)
# --------------- slot limit:
# unit: stock, index
# supply: stock, what
# seahub: stock
# airhub: stock
# plant: stock

# io: in out off

infra_0 = {
    (4, 1): [
        {"type": "seahub", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}},
        {"type": "unit", "own": "Aaa", "state": 1.0, "io": {"mech": "in"}, "stock": {"mech": 200.4}},
        {"type": "supply", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}, "supply": "devel"},
        {"type": "supply", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}, "supply": "mech"},
        {"type": "supply", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}, "supply": "basic"},
    ],
    (4, 2): [
        {"type": "link", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}},
        {"type": "supply", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}, "supply": "seatech"},
        {"type": "supply", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}, "supply": "basic"},
    ],
    (4, 3): [
        {"type": "airhub", "own": "Aaa", "state": 0.5, "io": {}, "stock":{}},
        {"type": "supply", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}, "supply": "heavy"},
        {"type": "supply", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}, "supply": "basic"},
    ],
    (3, 2): [
        {"type": "seahub", "own": "Aaa", "state": 0.5, "io": {}, "stock":{}},
        {"type": "link", "own": "Aaa", "state": 0.5, "io": {}, "stock":{}},
    ],
    (2, 3): [
        {"type": "fort", "own": "Aaa", "state": 1.0, "io": {"devel": "in"}, "stock": {"devel": 1.5}},
        {"type": "unit", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}},
    ],
    (2, 2): [
        {"type": "fort", "own": "Aaa", "state": 0.5, "io": {}, "stock":{}},
        {"type": "fort", "own": "Aaa", "state": 0.5, "io": {}, "stock":{}},
        None,
        {"type": "link", "own": "Aaa", "state": 0.5, "io": {}, "stock":{}},
        {"type": "plant", "own": "Aaa", "state": 0.5, "io": {}, "stock":{}}
    ],
    (-3, 0): [
        {"type": "plant", "own": "Bbb", "state": 1.0, "io": {}, "stock":{}}
    ],
    (2, 1): [
        {"type": "link", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}},
        {"type": "link", "own": "Aaa", "state": 1.0, "io": {}, "stock":{}}
    ],
    (-1, 6): [
        {"type": "link", "own": "Bbb", "state": 1.0, "io": {}, "stock":{}}
    ],
    (-3, 2): [
        {"type": "seahub", "own": "Bbb", "state": 1.0, "io": {}, "stock":{}},
        {"type": "airhub", "own": "Bbb", "state": 1.0, "io": {}, "stock":{}},
        {"type": "plant", "own": "Bbb", "state": 1.0, "io": {}, "stock":{}},
        {"type": "link", "own": "Bbb", "state": 1.0, "io": {}, "stock":{}},
        {"type": "unit", "own": "Bbb", "state": 1.0, "io": {}, "stock":{}},
        {"type": "fort", "own": "Bbb", "state": 1.0, "io": {}, "stock":{}}
    ]
}

###
### markers
###

markers_0 = [
    # ("vex", "Aaa", (2, 3)),
    # ("vex", "Bbb", (1, 3)),
    # ("vex", "Aaa", (3, 4)),
    # ("vex", "Aaa", (2, 4)),
    # ("a1", "Bbb", (0, 3), (1, 3)),
    # ("a1", "Aaa", (3, 3), (3, 4)),
    # ("a1", "Aaa", (3, 4), (4, 4)),
    # ("a1", "Aaa", (3, 8), (8, 8)),
    # ("l1", "Aaa", (3, 9), (7, 9), (8, 10), (8, 9)),
    # ("a2", "Bbb", (3, 11), (7, 11), (8, 13), (8, 11), (9, 11), (10, 14)),
    
    ("inf", None, (-3, 2, 1)),
    ("vex", None, (-3, 5))
]

###
### terrains
###

terrains_0 = {
    'void-0': {
        'desc': 'void',
        'color': [0.0, 0.0, 0.0],
        'navigable': False,
        'buildable': False,
        'costal': False,
        'mobile': 0.0,
        'slots': 0
    },
    'desert-0': {
        'desc': 'desert',
        'color': [0.95, 0.95, 0.92],
        'navigable': False,
        'buildable': True,
        'costal': False,
        'mobile': 1.0,
        'slots': 1
    },
    'shallows-0': {
        'desc': 'shallows',
        'color': [0.8, 0.9, 1.0],
        'navigable': True,
        'buildable': False,
        'costal': True,
        'mobile': 10.0,
        'slots': 1
    },
    'water-0': {
        'desc': 'water',
        'color': [0.75, 0.85, 1.0],
        'navigable': True,
        'buildable': False,        
        'costal': False,
        'mobile': 100.0,
        'slots': 0
    },
    'hills-0': {
        'desc': 'hills',
        'color': [0.89, 0.84, 0.84],
        'navigable': False,
        'buildable': True,        
        'costal': False,
        'mobile': 0.1,
        'slots': 1
    },
    'steppe-0': {
        'desc': 'warm steppe',
        'color': [1.0, 1.0, 1.0],
        'navigable': False,
        'buildable': True,        
        'costal': False,
        'mobile': 3.0,
        'slots': 6
    }
}

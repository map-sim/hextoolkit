###
### settings
###

settings_0 = {
    'current-turn': 0,
    'window-title': 'main-window',
    'window-size': (1100, 1000),
    'window-offset': (740, 225),
    'window-zoom': 15.0,
    'move-sensitive': 50,
    'hex-radius': 2.2,
    'base-thickness': 0.08,
    'marker-color': (1.0, 1.0, 0.3),
    'show-markers': False,
    'display-length': 16
}

builds_0 = {
    "plant": {
        "cost": 100,
        "strength": 80,
        "range": 30,
        "power": 20,
    },
    "supply": {
        "cost": 50,
        "strength": 20,
        "no-power": 0.0,
        "power": -3,
    },
    "unit": {
        "cost": 40,
        "strength": 10,
        "no-power": 0.5,
        "power": -1,
    },
    "link": {
        "cost": 10,
        "strength": 60,
        "power": 0,
    },
    "seahub": {
        "cost": 50,
        "strength": 90,
        "no-power": 0.5,
        "power": -1,
    },
    "airhub": {
        "cost": 40,
        "strength": 50,
        "no-power": 0.25,
        "power": -1,
    },
    "fort": {
        "cost": 30,
        "strength": 200,
        "power": 0,
    }
}

units_0 = {
    "supplying": {
        "char": "S",
        "cost": 20.5,
        "speed": 1.5,
        "shot-range": 0,
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
        "cost": 30.5,
        "stock-form": "mech",
        "stock-reserve": "devel",
        "shot-range": 0,
        "order-effect": {
            "move": 0.5,
            "supply": 0.1,
            "devel": 1.0,
            "defence": 0.2,
            "storm": 0.1,
        },
        "order-cost": {
            "move": (0.5, 0.0),
            "supply": (1.0, 0.0),
            "devel": (1.0, 1.0),
            "defence": (1.0, 0.0),
            "storm": (1.5, 0.0),
        }
    },
    "special": {
        "char": "Q",
        "cost": 50.5,
        "stock-form": "special",
        "stock-reserve": "special",
        "shot-range": 6,
        "order-effect": {
            "move": 1.75,
            "supply": 0.3,
            "devel": 0.1,
            "defence": 1.0,
            "storm": 0.9,
            "shot": 0.33
        },
        "order-cost": {
            "move": (0.5, 0.0),
            "supply": (1.0, 0.0),
            "devel": (1.0, 0.5),
            "defence": (1.0, 1.0),
            "storm": (1.5, 1.0),
            "shot": (0.2, 1.0)
        }
    },
    "motorized": {
        "char": "K",
        "cost": 28.5,
        "stock-form": "mech",
        "stock-reserve": "mech",
        "shot-range": 2,
        "order-effect": {
            "move": 1.0,
            "supply": 0.2,
            "devel": 0.2,
            "defence": 1.5,
            "storm": 0.5,
            "shot": 0.25
        },
        "order-cost": {
            "move": (0.66, 0.1),
            "supply": (1.0, 0.2),
            "devel": (0.66, 0.5),
            "defence": (0.75, 0.66),
            "storm": (1.0, 1.0),
            "shot": (0.25, 0.5)
        }
    },
    "mechanized": {
        "char": "M",
        "cost": 72.0,
        "stock-form": "heavy",
        "stock-reserve": "heavy",
        "shot-range": 5,
        "efficiency": {
            "move": 0.8,
            "supply": 0.1,
            "defence": 1.25,
            "storm": 0.75,
            "shot": 0.5
        },
        "usage": {
            "move": (0.72, 0.1),
            "supply": (1.2, 0.2),
            "defence": (0.85, 0.66),
            "storm": (1.35, 1.5),
            "shot": (0.35, 0.7),
        }
    },
    "armored": {
        "char": "T",
        "cost": 100.0,
        "stock-form": "heavy",
        "stock-reserve": "heavy",
        "shot-range": 5,
        "efficiency": {
            "move": 0.4,
            "defence": 1.2,
            "storm": 1.25,
            "shot": 0.5
        },
        "usage": {
            "move": (1.2, 0.05),
            "defence": (1.5, 0.88),
            "storm": (2.25, 1.75),
            "shot": (0.4, 0.8),
        }
    },
    "artillery": {
        "char": "A",
        "cost": 80.0,
        "stock-form": "heavy",
        "stock-reserve": "heavy",
        "shot-range": 16,
        "efficiency": {
            "move": 0.5,
            "defence": 0.15,
            "storm": 0.1,
            "shot": 1.5,
        },
        "usage": {
            "move": (0.8, 0.05),
            "defence": (0.5, 0.88),
            "storm": (0.75, 0.75),
            "shot": (0.5, 1.2),
        }
    }
}

###
### xsystem
###

xsystem_0 = {}

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
    ('vex', 'steppe-0', (-1, -2)),
    ('vex', 'steppe-0', (0, -2)),
    ('vex', 'steppe-0', (0, -1)),
    ('vex', 'desert-0', (0, 0)),
    ('vex', 'desert-0', (-1, 0)),
    ('vex', 'desert-0', (-2, 1)),
    ('vex', 'desert-0', (0, 3)),
    ('vex', 'desert-0', (1, 3)),
    ('vex', 'desert-0', (1, 2)),
    ('vex', 'desert-0', (-1, 3)),
    ('vex', 'desert-0', (0, 1)),
    ('vex', 'desert-0', (0, 4)),
    ('vex', 'steppe-0', (1, 1)),
    ('vex', 'steppe-0', (2, 2)),
    ('vex', 'steppe-0', (2, 3)),
    ('vex', 'steppe-0', (1, -1)),
    ('vex', 'steppe-0', (1, -2)),
    ('vex', 'steppe-0', (2, -1)),
    ('vex', 'steppe-0', (2, -2)),
    ('vex', 'steppe-0', (3, 0)),
    ('vex', 'steppe-0', (3, 1)),
    ('vex', 'steppe-0', (4, 2)),
    ('vex', 'steppe-0', (4, 3)),
    ('vex', 'steppe-0', (5, 2)),
    ('vex', 'steppe-0', (4, 1)),
    ('vex', 'steppe-0', (3, -1)),
    ('vex', 'steppe-0', (3, -2)),
    ('vex', 'steppe-0', (4, -1)),
    ('vex', 'steppe-0', (5, 0)),
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
### stock
###

# basic, devel, mech, heavy, aviation, seatech

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
        {"own": "Aaa", "type": "mechanized", "size": 3, "state": 1.0, "stock": (0.6, 0.5), "order": "shot", "target": (0, 2)},
        {"own": "Aaa", "type": "motorized", "size": 2, "state": 1.0, "stock": (0.6, 0.5), "order": "shot", "target": (1, 2, 0)},
        {"own": "Aaa", "type": "motorized", "size": 3, "state": 1.0, "stock": (0.6, 0.5), "order": "shot", "target": 3},
        {"own": "Aaa", "type": "motorized", "size": 3, "state": 1.0, "stock": (0.6, 0.5), "order": "defence"}
    ],
    (2, 2): [
        {"own": "Aaa", "type": "supplying", "size": 2, "state": 1.0, "stock": (0.6, 0.0), "order": "defence"},
        {"own": "Aaa", "type": "motorized", "size": 2, "state": 1.0, "stock": (0.6, 0.5), "order": "defence"}
    ],
    (-1, 2): [
        {"own": "Aaa", "type": "mechanized", "size": 1, "state": 1.0, "stock": (0.6, 0.5), "order": "defence"},
        {"own": "Aaa", "type": "mechanized", "size": 1, "state": 1.0, "stock": (0.6, 0.5), "order": "defence"}
    ],
    (-2, 2): [
        {"own": "Bbb", "type": "motorized", "size": 1, "state": 0.4, "stock": (0.66, 0.66), "order": "storm", "target": (-1, 2)},
        {"own": "Bbb", "type": "motorized", "size": 1, "state": 1.0, "stock": (0.75, 0.6), "order": "storm", "target": 2}
    ],
    (-3, 0): [
        {"own": "Bbb", "type": "engineering", "size": 1, "state": 0.4, "stock": (0.66, 0.66), "order": "storm", "target": (-1, 2)},
        {"own": "Bbb", "type": "supplying", "size": 1, "state": 1.0, "stock": (0.75, 0.6), "order": "storm", "target": 2}
    ],
    (-3, -1): [
        {"own": "Aaa", "type": "special", "size": 1, "state": 1.0, "stock": (0.6, 0.5), "order": "defence"}
    ],
    (0, 1): [
        {"own": "Bbb", "type": "armored", "size": 2, "state": 1.0, "stock": (0.75, 0.6), "order": "move", "progress": 0.0, "target": [(1, 2), (0, 3)]}
    ],
    (-1, 1): [
        {"own": "Bbb", "type": "artillery", "size": 2, "state": 1.0, "stock": (0.75, 0.6), "order": "move", "progress": 0.0, "target": [(1, 2), (0, 3)]}
    ],
    (-3, 2): [
        {"own": "Bbb", "type": "engineering", "size": 2, "state": 1.0, "stock": (0.75, 0.6), "order": "move", "progress": 0.0, "target": [(1, 2), (0, 3)]}
    ],
    (-1, 0): [
        {"own": "Bbb", "type": "supplying", "size": 2, "state": 1.0, "stock": (0.5, 0.0), "order": "supply", "source": [(-3, 2), (-3, 1), (-2, 1)], "target": [(0, 0), (0, 1)]}
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

infra_0 = {
    (2, 3): [
        {"type": "unit", "own": "Aaa", "state": 1.0},
        {"type": "fort", "own": "Aaa", "state": 1.0},
        {"type": "unit", "own": "Bbb", "state": 1.0},
        {"type": "fort", "own": "Aaa", "state": 1.0},
        {"type": "supply", "own": "Aaa", "state": 1.0},
        {"type": "supply", "own": "Aaa", "state": 1.0}
    ],
    (2, 2): [
        {"type": "airhub", "own": "Aaa", "state": 0.5},
        {"type": "seahub", "own": "Aaa", "state": 0.5},
        {"type": "unit", "own": "Aaa", "state": 0.5},
        {"type": "link", "own": "Aaa", "state": 0.5},
        {"type": "plant", "own": "Aaa", "state": 0.5}
    ],
    (-2, 2): [
        {"type": "link", "own": "Aaa", "state": 0.5},
        {"type": "unit", "own": "Aaa", "state": 0.5}
    ],
    (1, 2): [
        {"type": "plant", "own": "Bbb", "state": 1.0}
    ],
    (2, 1): [
        {"type": "link", "own": "Aaa", "state": 1.0},
        {"type": "link", "own": "Aaa", "state": 1.0}
    ],
    (-1, 6): [
        {"type": "link", "own": "Bbb", "state": 1.0}
    ],
    (-3, 2): [
        {"type": "seahub", "own": "Bbb", "state": 1.0}
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
        'mobile': 0.0,
        'slots': 0
    },
    'desert-0': {
        'desc': 'desert',
        'color': [0.95, 0.95, 0.94],
        'navigable': False,
        'buildable': True,        
        'mobile': 1.0,
        'slots': 1
    },
    'shallows-0': {
        'desc': 'shallows',
        'color': [0.8, 0.9, 1.0],
        'navigable': True,
        'buildable': False,        
        'mobile': 10.0,
        'slots': 0
    },
    'water-0': {
        'desc': 'water',
        'color': [0.75, 0.85, 1.0],
        'navigable': True,
        'buildable': False,        
        'mobile': 100.0,
        'slots': 0
    },
    'hills-0': {
        'desc': 'hills',
        'color': [0.88, 0.85, 0.85],
        'navigable': False,
        'buildable': True,        
        'mobile': 0.1,
        'slots': 1
    },
    'steppe-0': {
        'desc': 'warm steppe',
        'color': [1.0, 1.0, 1.0],
        'navigable': False,
        'buildable': True,        
        'mobile': 3.0,
        'slots': 6
    }
}

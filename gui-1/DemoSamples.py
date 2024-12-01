###
### settings
###

settings_0 = {
    'window-title': 'main-window',
    'window-size': (1220, 1020),
    'window-offset': (840, 125),
    'window-zoom': 15.0,
    'move-sensitive': 50,
    'hex-radius': 2.2,
    'base-thickness': 0.08,
    'marker-color': (1.0, 1.0, 0.3),
    'show-markers': False,
    'display_length': 14
}

isystem_0 = {
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

xsystem_0 = {
    "supplying": {
        "char": "S",
        "cost": 20.5,
        "stock": None,
        "shot-range": 0,
        "efficiency": {
            "move": 1.5,
            "supply": 1.0,
            "defence": 0.33
        },
        "usage": {
            "move": (0.5, 0.0),
            "supply": (1.0, 0.0),
            "defence": (0.75, 0.0)
        }
    },
    "motorized": {
        "char": "K",
        "cost": 32.0,
        "stock": "mech",
        "shot-range": 2,
        "efficiency": {
            "move": 1.0,
            "defence": 1.1,
            "storm": 0.5,
            "shot": 0.3
        },
        "usage": {
            "move": (0.66, 0.0),
            "defence": (0.75, 0.5),
            "storm": (1.25, 1.1),
            "shot": (0.25, 0.5)
        }
    },
    "mechanized": {
        "char": "M",
        "cost": 72.0,
        "stock": "mech",
        "shot-range": 5,
        "efficiency": {
            "move": 0.9,
            "defence": 1.0,
            "storm": 0.75,
            "shot": 0.5
        },
        "usage": {
            "move": (0.72, 0.0),
            "defence": (0.85, 0.6),
            "storm": (1.35, 1.5),
            "shot": (0.35, 0.7)
        }
    }    
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
    ('vex', 'mountains-0', (-2, 0)),
    ('vex', 'mountains-0', (-1, 2)),
    ('vex', 'mountains-0', (-1, 1)),
    ('vex', 'mountains-0', (0, 2)),
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
    "group-0": {
        "qwerty": [1.4, 2.1, 9.2, 8.8, 0.4, 0.8],
        "abc": [2.2, 3.1, 12.2, 13.2, 1.2, 3.2]
    },
    "group-1": {
        "Aaa": [0.0, 1.4, 2.1, 9.2, 8.8],
        "Bbb": [0.0, 2.2, 3.1, 12.2, 13.2]
    }
}

###
### stock
###

# basic, devel, infantry

###
### units
###

# orders: defense
#         move (target: hex)
#         storm (target: hex | index)
#         shot (target: hex | index | hex + index)

units_0 = {
    (2, 3): [
        {"own": "Aaa", "type": "mechanized", "size": 3, "state": 1.0, "stock": (0.6, 0.5), "order": "shot", "target": (0, 2)},
        {"own": "Aaa", "type": "motorized", "size": 2, "state": 1.0, "stock": (0.6, 0.5), "order": "shot", "target": (1, 2, 0)},
        {"own": "Aaa", "type": "motorized", "size": 3, "state": 1.0, "stock": (0.6, 0.5), "order": "shot", "target": 3},
        {"own": "Aaa", "type": "motorized", "size": 3, "state": 1.0, "stock": (0.6, 0.5), "order": "defence"}
    ],
    (2, 2): [
        {"own": "Aaa", "type": "motorized", "size": 1, "state": 1.0, "stock": (0.6, 0.5), "order": "defence"}
    ],
    (-1, 2): [
        {"own": "Aaa", "type": "mechanized", "size": 1, "state": 1.0, "stock": (0.6, 0.5), "order": "defence"}
    ],
    (-2, 2): [
        {"own": "Bbb", "type": "motorized", "size": 1, "state": 0.4, "stock": (0.66, 0.66), "order": "storm", "target": (-1, 2)},
        {"own": "Bbb", "type": "motorized", "size": 1, "state": 1.0, "stock": (0.75, 0.6), "order": "storm", "target": 2}
    ],
    (0, 1): [
        {"own": "Bbb", "type": "motorized", "size": 2, "state": 1.0, "stock": (0.75, 0.6), "order": "move", "progress": 0.0, "target": [(1, 2), (0, 3)]}
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
    'mountains-0': {
        'desc': 'mountains',
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

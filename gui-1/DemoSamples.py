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
    'show-markers': True,
    'display_length': 14
}

xsystem_0 = {
    "supplying": {
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
    ('vex', 'mountains-0', (-2, 0)),
    ('vex', 'mountains-0', (-1, 2)),
    ('vex', 'mountains-0', (-1, 1)),
    ('vex', 'mountains-0', (0, 2)),
    ('grid', (0.8, 0.8, 0.8), 0.16),
    ('grid', (0.4, 0.4, 0.4), 0.08)
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
        {"own": "Aaa", "type": "motorized", "size": 3, "state": 1.0, "stock": (0.6, 0.5), "order": "shot", "target": (2, 2, 0)},
        {"own": "Aaa", "type": "motorized", "size": 3, "state": 1.0, "stock": (0.6, 0.5), "order": "shot", "target": (2, 2, 0)},
        {"own": "Aaa", "type": "motorized", "size": 3, "state": 1.0, "stock": (0.6, 0.5), "order": "shot", "target": (2, 2, 0)},
        {"own": "Aaa", "type": "motorized", "size": 3, "state": 1.0, "stock": (0.6, 0.5), "order": "defence"}
    ],
    (0, 2): [
        {"own": "Aaa", "type": "motorized", "size": 1, "state": 1.0, "stock": (0.6, 0.5), "order": "defence"}
    ],
    (2, 2): [
        {"own": "Bbb", "type": "motorized", "size": 1, "state": 0.4, "stock": (0.66, 0.66), "order": "storm", "target": (2, 3)},
        {"own": "Bbb", "type": "motorized", "size": 1, "state": 1.0, "stock": (0.75, 0.6), "order": "storm", "target": 2}
    ],
    (1, 1): [
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
        {"type": "unit", "own": "Aaa", "build": 1.0},
        {"type": "fort", "own": "Aaa", "build": 1.0},
        {"type": "unit", "own": "Bbb", "build": 1.0},
        {"type": "fort", "own": "Aaa", "build": 1.0},
        {"type": "supply", "own": "Aaa", "build": 1.0},
        {"type": "supply", "own": "Aaa", "build": 1.0}
    ],
    (2, 2): [
        {"type": "airhub", "own": "Aaa", "build": 0.5},
        {"type": "seahub", "own": "Aaa", "build": 0.5},
        {"type": "unit", "own": "Aaa", "build": 0.5},
        {"type": "link", "own": "Aaa", "build": 0.5},
        {"type": "plant", "own": "Aaa", "build": 0.5}
    ],
    (1, 2): [
        {"type": "plant", "own": "Bbb", "build": 1.0}
    ]
}

###
### markers
###

markers_0 = [
    ("vex", "Aaa", (2, 3)),
    ("vex", "Bbb", (1, 3)),
    ("vex", "Aaa", (3, 4)),
    ("vex", "Aaa", (2, 4)),
    ("a1", "Bbb", (0, 3), (1, 3)),
    ("a1", "Aaa", (3, 3), (3, 4)),
    ("a1", "Aaa", (3, 4), (4, 4)),
    ("a1", "Aaa", (3, 8), (8, 8)),
    ("l1", "Aaa", (3, 9), (7, 9), (8, 10), (8, 9)),
    ("a2", "Bbb", (3, 11), (7, 11), (8, 13), (8, 11), (9, 11), (10, 14)),
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
        'color': [0.75, 0.85, 1.0],
        'navigable': True,
        'buildable': False,        
        'mobile': 10.0,
        'slots': 0
    },
    'water-0': {
        'desc': 'water',
        'color': [0.65, 0.7, 1.0],
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

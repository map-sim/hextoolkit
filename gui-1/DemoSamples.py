###
### settings
###

settings_0 = {
    'window-title': 'main-window',
    'window-size': (1800, 780),
    'window-offset': (840, 125),
    'window-zoom': 15.0,
    'move-sensitive': 50,
    'hex-radius': 2.2,
    'base-thickness': 0.08,
    'marker-color': (0.0, 0.0, 0.0),
    'show-dashes': True,
    'show-arrows': True,
    'show-links': True,
    'display_length': 14
}

###
### landform
###

landform_0 = [
    ('base', 'water-0'),
    ### ('rect', 'void-0', -40, -10, 80, 40),
    ('vex', 'desert-0', (0, 3)),
    ('vex', 'desert-0', (1, 3)),
    ('vex', 'desert-0', (1, 2)),
    ('vex', 'desert-0', (-1, 3)),
    ('vex', 'desert-0', (-1, 2)),
    ('vex', 'desert-0', (-1, 1)),
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
        "marker-color": [0.2, 0.7, 0.2],
    },
    "Bbb": {
        "base-color": [0.9, 0.2, 0.2],
        "marker-color": [1.0, 0.3, 0.3],
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
### units
###

units_0 = {
    (2, 3): [
        {"own": "Aaa", "type": "infantry", "size": 1}
    ],
    (2, 2): [
        {"own": "Bbb", "type": "infantry", "size": 1},
        {"own": "Bbb", "type": "infantry", "size": 1}
    ]
}

###
### infrastructure
###

# fort, link
# unit, supply
# seahub, airport

infra_0 = {
    (2, 3): [
        {"type": "unit", "own": "Aaa"},
        {"type": "fort", "own": "Aaa"},
        {"type": "unit", "own": "Bbb"},
        {"type": "fort", "own": "Aaa"},
        {"type": "supply", "own": "Aaa"},
        {"type": "supply", "own": "Aaa"}
    ],
    (2, 2): [
        {"type": "airport", "own": "Aaa"},
        {"type": "seahub", "own": "Aaa"},
        {"type": "unit", "own": "Aaa"},
        {"type": "link", "own": "Aaa"},
        {"type": "plant", "own": "Aaa"}
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
    ("arr", "Bbb", (0, 3), (1, 3)),
    ("arr", "Aaa", (3, 3), (3, 4)),
    ("arr", "Aaa", (3, 4), (4, 4)),
    ("arr", "Aaa", (3, 8), (8, 8)),
    ("link", "Aaa", (3, 9), (7, 9), (8, 10), (8, 9)),
    ("dash", "Bbb", (3, 11), (7, 11), (8, 13), (8, 11), (9, 11), (10, 14)),
    ("vex", None, (-1, -1))
]

###
### tech tree
###

tech_list_0 = {
    "devel": "development supply",
    "supply": "common military supply",

    "armored": "armored force supply",
    "infantry": "infantry supply",
    "artillery": "artillery supply",
    "air-force": "air-force supply",
    "naval-force": "naval supply"
}

###
### terrains
###

terrains_0 = {
    'void-0': {
        'desc': 'void',
        'color': [0.0, 0.0, 0.0],
        'navigable': False,
        'buildable': False,
        'conductance': 0.0,
        'slots': 0
    },
    'desert-0': {
        'desc': 'desert',
        'color': [1.0, 0.96, 0.75],
        'navigable': False,
        'buildable': True,        
        'conductance': 1.0,
        'slots': 2
    },
    'shallows-0': {
        'desc': 'shallows',
        'color': [0.7, 0.85, 1.0],
        'navigable': True,
        'buildable': False,        
        'conductance': 10.0,
        'slots': 0
    },
    'water-0': {
        'desc': 'water',
        'color': [0.54, 0.7, 1.0],
        'navigable': True,
        'buildable': False,        
        'conductance': 100.0,
        'slots': 0
    },
    'mountains-0': {
        'desc': 'mountains',
        'color': [0.9, 0.7, 0.7],
        'navigable': False,
        'buildable': True,        
        'conductance': 0.1,
        'slots': 3
    },
    'steppe-0': {
        'desc': 'warm steppe',
        'color': [0.55, 0.92, 0.7],
        'navigable': False,
        'buildable': True,        
        'conductance': 3.0,
        'slots': 6
    }
}

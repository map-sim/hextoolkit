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
        "technologies": {
            "tech_A": 16.0,
            "tech_B": 16.0,
            "tech_C": 12.5
        }
    },
    "Bbb": {
        "base-color": [0.9, 0.2, 0.2],
        "marker-color": [1.0, 0.3, 0.3],
        "technologies": {
            "tech_A": 16.0,
            "tech_B": 6.66
        }
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

tech_list_0 = [
    "tech_A",
    "tech_B",
    "tech_C",
    "tech_D",
    "tech_E",
    "tech_F",
    "tech_G",
    "tech_H",
    "tech_I",
    "tech_J",
    "tech_K",
    "tech_L",
    "tech_M",
    "tech_N",
    "tech_O"
]

###
### terrains
###

terrains_0 = {
    'void-0': {
        'buildable': False,
        'color': [0.0, 0.0, 0.0],
        'desc': 'void',
        'slots': 0
    },
    'desert-0': {
        'buildable': True,
        'color': [1.0, 0.96, 0.75],
        'desc': 'desert',
        'slots': 2        
    },
    'shallows-0': {
        'buildable': None,
        'color': [0.7, 0.85, 1.0],
        'desc': 'shallows',
        'slots': 0
    },
    'water-0': {
        'buildable': False,
        'color': [0.54, 0.7, 1.0],
        'desc': 'water',
        'slots': 0
    },
    'mountains-0': {
        'buildable': True,
        'color': [0.9, 0.7, 0.7],
        'desc': 'mountains',
        'slots': 3
    },
    'steppe-0': {
        'buildable': True,
        'color': [0.55, 0.92, 0.7],
        'desc': 'warm steppe',
        'slots': 6
    }
}

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
    'tech-batchsize': 5
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
        "marker-color": [0.2, 0.7, 0.2]
    },
    "Bbb": {
        "base-color": [0.9, 0.2, 0.2],
        "marker-color": [1.0, 0.3, 0.3]
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
    ("dash", "Bbb", (3, 11), (7, 11), (8, 13), (8, 11), (9, 11)),
    ("vex", None, (-1, -1))
]

###
### tech tree
###

tech_tree_0 = {
    "tech_A": {"cost": 16.0},
    "tech_B": {"cost": 16.0},
    "tech_C": {"cost": 36.6},
    "tech_D": {"cost": 48.0},
    "tech_AB": {"cost": 56.0, "need": ["tech_A", "tech_B"]},
    "tech_BC": {"cost": 56.0, "need": ["tech_B", "tech_C"]},
    "tech_ABBC": {"cost": 66.6, "need": ["tech_AB", "tech_BC"]}
}

###
### terrains
###

terrains_0 = {
    'void-0': {
        'buildable': False,
        'color': [0.0, 0.0, 0.0],
        'desc': 'void',
        'resources': {}
    },
    'desert-0': {
        'buildable': True,
        'color': [1.0, 0.96, 0.75],
        'desc': 'desert',
        'resources': {
            'wind': 0.4,
            'sun': 0.5
        }
    },
    'shallows-0': {
        'buildable': None,
        'color': [0.7, 0.85, 1.0],
        'desc': 'shallows',
        'resources': {
            'wind': 0.65
        }
    },
    'water-0': {
        'buildable': False,
        'color': [0.54, 0.7, 1.0],
        'desc': 'water',
        'resources': {}
    },
    'mountains-0': {
        'buildable': True,
        'color': [0.9, 0.7, 0.7],
        'desc': 'mountains',
        'resources': {
            'wind': 0.55,
            'sun': 0.3
        }
    },
    'steppe-0': {
        'buildable': True,
        'color': [0.55, 0.92, 0.7],
        'desc': 'warm steppe',
        'resources': {
            'wind': 0.4,
            'sun': 0.5
        }
    }
}

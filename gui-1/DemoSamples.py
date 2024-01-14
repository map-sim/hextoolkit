###
### settings
###

settings_0 = {
    'window-title': 'main-window',
    'window-size': (1800, 780),
    'window-offset': (840, 125),
    'window-zoom': 15.0,
    'move-sensitive': 50,
    'hex-radius': 2.2
}

###
### landform
###

landform_0 = [
    ('base', 'water-0'),
    ('vex', 'desert-0', (0, 3)),
    ('vex', 'desert-0', (1, 3)),
    ('vex', 'desert-0', (1, 2)),
    ('vex', 'steppe-0', (2, 2)),
    ('vex', 'steppe-0', (2, 3)),
    ('grid', (0.8, 0.8, 0.8), 0.16),
    ('grid', (0.4, 0.4, 0.4), 0.08)
]

###
### terrains
###

terrains_0 = {
    'desert-0': {
        'buildable': True,
        'color': [1.0, 0.96, 0.75],
        'desc': 'desert',
        'resources': {}
    },
    'water-0': {
        'buildable': False,
        'color': [0.6, 0.8, 1.0],
        'desc': 'water',
        'resources': {
            'food': 0.2
        }
    },
    'mointain-0': {
        'buildable': True,
        'color': [0.33, 0.66, 0.99],
        'desc': 'water',
        'resources': {
            'metal': 0.5
        },
    },
    'forest-0': {
        'buildable': True,
        'color': [0.5, 0.88, 0.75],
        'desc': 'forest',
        'resources': {
            'food': 0.1,
            'wood': 0.5
        },
    },
    'steppe-0': {
        'buildable': True,
        'color': [0.66, 0.99, 0.88],
        'desc': 'warm steppe',
        'resources': {
            'food': 0.2
        },
    },
    'steppe-1': {
        'buildable': True,
        'color': [0.77, 0.99, 0.92],
        'desc': 'cold step',
        'resources': {
            'food': 0.02
        },
    },
}

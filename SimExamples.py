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
        "mixer": {"shape": "mixer-0", "modules": 2, "interval": 2, "range": 120},
        "store": {"shape": "store-0", "modules": 2, "interval": 2, "range": 160},
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
        [(13, 2), "mixer", "Aaa", 2, "AB"],
        [(15, 5), "store", "Aaa", 2, ["AC", "BC", "AB", "A", "B", "C"]],
        [(15, 8), "store", "Aaa", 2, ["AC", "AC", "AC", "A"]],
        [(18, 8), "store", "Aaa", 2, []],
    ],
    "terrains": [
        ("base", "desert-0"),
        ("polygon", "crater-crown-0",
         (-14.94, 14.87),
         (-15.05, 16.33),
         (-14.23, 17.25),
         (-12.55, 17.96),
         (-10.65, 18.17),
         (-10.76, 16.6),
         (-11.74, 14.97),
         ),
        ("polygon", "crater-crown-0",
         (-14.68, 15.06),
         (-14.38, 13.46),
         (-14.24, 11.27),
         (-15.94, 10.04),
         (-17.9, 9.44),
         (-18.67, 12.4),
         (-17.37, 14.2),
         ),
        ("polygon", "crater-crown-0",
         (-14.92, 13.48),
         (-13.71, 13.8),
         (-13.52, 15.41),
         (-14.8, 14.95),
        ),
        ("polygon", "crater-crown-0",
         (-20.99, 7.27),
         (-23.83, 6.04),
         (-24.66, 4.1),
         (-24.33, 1.39),
         (-22.35, 1.35),
         (-21.12, 3.24),
         (-20.24, 5.17),
        )
    ]
}


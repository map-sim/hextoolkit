library0 = {
    "objects": {
	"drill": {"shape": "drill-0", "radius": 30},
	"mineshaft": {"shape": "mineshaft-0", "radius": 30},
	"input": {"shape": "input-0", "radius": 30},
	"output": {"shape": "output-0", "radius": 30},
	"store": {"shape": "store-0", "radius": 30},
	"mixer": {"shape": "mixer-0", "radius": 30},
	"repeater": {"shape": "repeater-0", "radius": 30},
	"developer": {"shape": "developer-0", "radius": 30, "fuel": "AC"},
	"launcher": {"shape": "launcher-0", "radius": 30, "fuel": "AC"},
	"transmitter": {"shape": "transmitter-0", "radius": 60, "fuel": "AB"},
	"laboratory": {"shape": "laboratory-0", "radius": 30, "fuel": "AB"},
	"radiator": {"shape": "radiator-0", "radius": 60, "fuel": "BC"},
	"barrier": {"shape": "barrier-0", "radius": 30, "fuel": "BC"}
    },
    "resources": {
        "A": {"color": [1.0, 0.1, 0.1]},
        "B": {"color": [0.1, 0.8, 0.1]},
        "C": {"color": [0.1, 0.1, 1.0]},
        "AB": {"color": [1.0, 0.8, 0.1]},
        "AC": {"color": [1.0, 0.1, 1.0]},
        "BC": {"color": [0.1, 0.9, 0.9]}
    },
    "terrains": {
	"desert-0": {"desc": "desert", "color": [1.0, 0.98, 0.95], "level": 10.5},
	"desert-1": {"desc": "desert", "color": [1.0, 0.92, 0.92], "level": 14.2},
	"desert-2": {"desc": "desert", "color": [1.0, 0.84, 0.84], "level": 32.3}
    },
    "players": {
        "Aaa": {"color": [1.0, 1.0, 0.5]},
        "Bbb": {"color": [1.0, 0.5, 1.0]}
    }
}

battlefield0 = {
    "objects": [
        ("mineshaft", -380, -120, "Aaa", 1.0, "A"),
        ("mineshaft", -280, -120, "Bbb", 1.0, "B"),
        ("mineshaft", -180, -120, "Bbb", 1.0, "C"),
        ("drill", -340, -200, "Aaa", 1.0),
        ("drill", 140, -200, "Bbb", 1.0),
        ("drill", -300, -250, "Aaa", 0.1),
        ("input", -140, -200, "Aaa", 1.0, "A"),
        ("output", -100, -250, "Aaa", 0.66, "A"),
        ("store", -300, 50, "Aaa", 0.5, "A", 166.0),
        ("mixer", -200, -250, "Aaa", 0.5, None),
        ("mixer", -200, -450, "Aaa", 0.5, "BC"),
        ("mixer", -100, -450, "Aaa", 1.0, "AB"),
        ("mixer", 0, -450, "Aaa", 0.5, "AC"),
        ("launcher", 200, 250, "Aaa", 1.0, (-300, -250)),
        ("radiator", 100, 250, "Aaa", 1.0, True),
        ("laboratory", 100, 150, "Aaa", 1.0, "tech"),
        ("barrier", 0, 250, "Aaa", 1.0, True),
        ("developer", 200, 150, "Aaa", 1.0, True),
        ("transmitter", 300, 150, "Aaa", 1.0, True),
        ("repeater", 400, 150, "Aaa", 1.0)
    ],
    "resorces": [
    ],
    "terrains": [
        ("base", "desert-0"),
        ("polygon", "desert-1",
         (-1349.37, -657.26),
         (-1593.63, -464.6),
         (-1641.8, -99.94),
         (-1462.9, 240.65),
         (-1177.36, 316.33),
         (-809.26, 75.51),
         (-740.45, -320.11),
         (-884.94, -481.81),
        ),
        ("polygon", "desert-2",
         (-1285.32, -394.14),
         (-1391.15, -291.34),
         (-1427.43, -131.08),
         (-1357.89, 4.98),
         (-1267.18, 56.38),
         (-1158.33, -10.14),
         (-1055.52, -125.04),
         (-1073.67, -324.6),
         )
    ]
}


library0 = {
    "objects": {
	"drill": {"shape": "drill-0", "radius": 30},
	"mineshaft": {"shape": "mineshaft-0", "radius": 30},
	"input": {},
	"output": {},
	"store": {},
	"mixer": {},
	"repeater": {},
	"developer": {},
	"transmitter": {},
	"laboratory": {},
	"launcher": {},
	"radiator": {},
	"barrier": {}
    },
    "terrains": {
	"desert-0": {"desc": "desert", "color": [1.0, 1.0, 1.0],    "level": 10.5},
	"desert-1": {"desc": "desert", "color": [0.92, 0.92, 0.92], "level": 14.2},
	"desert-2": {"desc": "desert", "color": [0.84, 0.84, 0.84], "level": 32.3}
    },
    "players": {
        "Aaa": {"color": [1.0, 1.0, 0.0]}
    }
}

battlefield0 = {
    "objects": [
        ("mineshaft", -380, -120, "Aaa", 1.0),
        ("drill", -340, -200, "Aaa", 1.0),
        ("drill", -300, -250, "Aaa", 0.66)
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


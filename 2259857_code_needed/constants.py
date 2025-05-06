#This is a file that contains all the constants used throughout the project


DB_DRIVER_NAMES = [
    "carlos-sainz-jr",
    "charles-leclerc",
    "alexander-albon",
    "daniel-ricciardo",
    "fernando-alonso",
    "franco-colapinto",
    "george-russell",
    "guanyu-zhou",
    "kevin-magnussen",
    "lance-stroll",
    "lando-norris",
    "lewis-hamilton",
    "liam-lawson",
    "logan-sargeant",
    "max-verstappen",
    "nico-hulkenberg",
    "oscar-piastri",
    "pierre-gasly",
    "sergio-perez",
    "valtteri-bottas",
    "yuki-tsunoda",
    "esteban-ocon"

]

YEARS = [
    2022,
    2023,
    2024
]

API_DRIVER_NAMES = [
    "sainz",
    "albon",
    "leclerc",
    "ricciardo",
    "alonso",
    "colapinto",
    "russell",
    "zhou",
    "kevin_magnussen",
    "stroll",
    "norris",
    "hamilton",
    "lawson",
    "sargeant",
    "max_verstappen",
    "hulkenberg",
    "piastri",
    "gasly",
    "perez",
    "bottas",
    "tsunoda",
    "ocon",
    "de_vries",
]

TYRE_PARAMS =  {
    "netherlands": {
        "soft": {"base": 2.5, "linear": 0.0023, "quadratic": 0.029, "%Threshold": 2.1},
        "medium": {"base": 2.8, "linear": 0.0016, "quadratic": 0.004, "%Threshold": 2.35},
        "hard": {"base": 3, "linear": 0.002, "quadratic": 0.0020, "%Threshold": 2.3},
    },
    "spain": {
        "soft": {"base": 3.0, "linear": 0.0026, "quadratic": 0.0076, "%Threshold": 2.0},
        "medium": {"base": 3.9, "linear": 0.0026, "quadratic": 0.0053, "%Threshold": 1.65},
        "hard": {"base": 4.8, "linear": 0.0028, "quadratic": 0.0022, "%Threshold": 1.5},
    }
}

DEFAULT_BASE_LAP = {
    "bahrain": 90.949,
    "saudi-arabia": 89.527,
    "australia": 78.189,
    "japan": 90.144,
    "china": 96.359,
    "miami": 88.825,
    "emilia-romagna": 76.918,
    "monaco": 73.029,
    "canada": 74.293,
    "spain": 73.510,
    "austria": 66.062,
    "great-britain": 99.805,
    "hungary": 78.167,
    "belgium": 108.000,
    "netherlands": 73.262,
    "italy": 81.446,
    "azerbijan": 104.505,
    "singapore": 92.055,
    "united-states": 94.229,
    "mexico": 78.073,
    "sao-paulo": 72.100,
    "las-vegas": 94.485,
    "qatar": 82.715,
    "abu-dhabi": 84.106
}


DRIVER_TYRE_CONSTANTS = {
    "max-verstappen": 1.012,
    "lando-norris": 1.015,
    "lewis-hamilton": 1.016,
    "charles-leclerc": 1.017,
    "carlos-sainz-jr": 1.019,
    "george-russell": 1.023,
    "oscar-piastri": 1.025,
    "fernando-alonso": 1.028,
    "pierre-gasly": 1.03,
    "sergio-perez": 1.033,
    "nico-hulkenberg": 1.034,
    "yuki-tsunoda": 1.034,
    "alexander-albon": 1.0345,
    "lance-stroll": 1.045,
    "esteban-ocon": 1.046,
    "kevin-magnussen": 1.0465,
    "daniel-ricciardo": 1.0465,
    "franco-colapinto": 1.047,
    "liam-lawson": 1.047,
    "valtteri-bottas": 1.0475,
    "guanyu-zhou": 1.048,
    "logan-sargeant": 1.049,
    "oliver-bearman": 1.048

}

DRIVER_CONSTANTS = {
    "max-verstappen" : {"pace" : 1.012, "starting": 0.990000},
    "lando-norris" : {"pace" : 1.018, "starting": 0.873165},
    "lewis-hamilton" : {"pace" : 1.014, "starting": 0.892806},
    "charles-leclerc" : {"pace" : 1.016, "starting": 0.866615},
    "carlos-sainz-jr" : {"pace" : 1.017, "starting": 0.875504},
    "george-russell" : {"pace" : 1.036, "starting": 0.883948},
    "oscar-piastri" : {"pace" : 1.025, "starting": 0.892791},
    "fernando-alonso" : {"pace" : 1.028, "starting": 0.878837}, 
    "pierre-gasly" : {"pace" : 1.03, "starting": 0.867674},
    "sergio-perez" : {"pace" : 1.033, "starting": 0.862811},
    "nico-hulkenberg" : {"pace" : 1.034, "starting": 0.875116},
    "yuki-tsunoda" : {"pace" : 1.034, "starting": 0.887209},
    "alexander-albon" : {"pace" : 1.0345, "starting": 0.871395},
    "lance-stroll" : {"pace" : 1.045, "starting": 0.886279},
    "esteban-ocon" : {"pace" : 1.046, "starting": 0.887209},
    "kevin-magnussen" : {"pace" : 1.0465, "starting": 0.904899},
    "daniel-ricciardo" : {"pace" : 1.042, "starting": 0.851860},
    "franco-colapinto" : {"pace" : 1.047, "starting": 0.878837},
    "liam-lawson" : {"pace" : 1.047, "starting": 0.872326},
    "valtteri-bottas" : {"pace" : 1.0475, "starting": 0.850000},
    "guanyu-zhou" : {"pace" : 1.048, "starting": 0.895581},
    "logan-sargeant" : {"pace" : 1.049, "starting": 0.893721},
    "oliver-bearman" : {"pace" : 1.048, "starting": 0.850000}
}

DB_RACE_NAMES = [
    "bahrain",
    "saudi-arabia",
    "australia",
    "japan",
    "china",
    "miami",
    "emilia-romagna",
    "monaco",
    "canada",
    "spain",
    "austria",
    "great-britain",
    "hungary",
    "belgium",
    "netherlands",
    "italy",
    "azerbaijan",
    "singapore",
    "united-states",
    "mexico",
    "sao-paulo",
    "las-vegas",
    "qatar",
    "abu-dhabi",
    "france"
]

API_RACE_NAMES = [
        "Bahrain Grand Prix",
        "Saudi Arabian Grand Prix",
        "Australian Grand Prix",
        "Japanese Grand Prix",
        "Chinese Grand Prix",
        "Miami Grand Prix",
        "Emilia Romagna Grand Prix",
        "Monaco Grand Prix",
        "Canadian Grand Prix",
        "Spanish Grand Prix",
        "Austrian Grand Prix",
        "British Grand Prix",
        "Hungarian Grand Prix",
        "Belgian Grand Prix",
        "Dutch Grand Prix",
        "Italian Grand Prix",
        "Azerbaijan Grand Prix",
        "Singapore Grand Prix",
        "United States Grand Prix",
        "Mexico City Grand Prix",
        "São Paulo Grand Prix",
        "Las Vegas Grand Prix",
        "Qatar Grand Prix",
        "Abu Dhabi Grand Prix"
]



def DB_DRIVER_TO_API_NAME(name):
    driver_name_map = {    
    "carlos-sainz-jr": "sainz",
    "alexander-albon": "albon",
    "charles-leclerc": "leclerc",
    "daniel-ricciardo": "ricciardo",
    "fernando-alonso": "alonso",
    "franco-colapinto": "colapinto",
    "george-russell": "russell",
    "guanyu-zhou": "zhou",
    "kevin-magnussen": "kevin_magnussen",
    "lance-stroll": "stroll",
    "lando-norris": "norris",
    "lewis-hamilton": "hamilton",
    "liam-lawson": "lawson",
    "logan-sargeant": "sargeant",
    "max-verstappen": "max_verstappen",
    "nico-hulkenberg": "hulkenberg",
    "oscar-piastri": "piastri",
    "pierre-gasly": "gasly",
    "sergio-perez": "perez",
    "valtteri-bottas": "bottas",
    "yuki-tsunoda": "tsunoda",
    "esteban-ocon": "ocon"
    }
    return driver_name_map.get(name, f"Error: '{name}' not found.")

API_TO_DB_FORMAT = {
    'max_verstappen': 'max-verstappen',
    'ricciardo': 'daniel-ricciardo',
    'leclerc': 'charles-leclerc',
    'perez': 'sergio-perez',
    'sainz': 'carlos-sainz-jr',
    'hamilton': 'lewis-hamilton',
    'russell': 'george-russell',
    'alonso': 'fernando-alonso',
    'bottas': 'valtteri-bottas',
    'stroll': 'lance-stroll',
    'norris': 'lando-norris',
    'ocon': 'esteban-ocon',
    'albon': 'alexander-albon',
    'sargeant': 'logan-sargeant',
    'hulkenberg': 'nico-hulkenberg',
    'tsunoda': 'yuki-tsunoda',
    'piastri': 'oscar-piastri',
    'zhou': 'guanyu-zhou',
    'kevin_magnussen': 'kevin-magnussen',
    'gasly': 'pierre-gasly',
    'lawson': 'liam-lawson',
    'colapinto': 'franco-colapinto',
    'bearman': 'oliver-bearman'
}



AVG_PIT_LOSS = {
    "netherlands" : 21.55,
    "spain" : 22.62
}

AVG_FUEL_LOSS = {
    "netherlands" : 1.51,
    "spain" : 1.65
}

NUMBER_OF_LAPS = {
    "netherlands" : 72,
    "spain" : 66
}

PREV_RACE_RESULTS = {
    "netherlands" : ["lando-norris", "max-verstappen", "charles-leclerc", "oscar-piastri", "carlos-sainz-jr", "sergio-perez", "george-russell", "lewis-hamilton", "pierre-gasly" , 
                     "fernando-alonso", "nico-hulkenberg", "daniel-ricciardo", "lance-stroll", "alexander-albon", "esteban-ocon", "logan-sargeant", "yuki-tsunoda", "kevin-magnussen",
                     "valtteri-bottas", "guanyu-zhou"],
    "spain" : ["max-verstappen", "lando-norris", "lewis-hamilton", "george-russell", "charles-leclerc", "carlos-sainz-jr", "oscar-piastri", "sergio-perez", "pierre-gasly", 
               "esteban-ocon", "nico-hulkenberg", "fernando-alonso", "guanyu-zhou", "lance-stroll", "daniel-ricciardo", "valtteri-bottas", "kevin-magnussen", "alexander-albon", 
               "yuki-tsunoda", "logan-sargeant"]
}


PREV_RACE_OVERTAKES = {
    "netherlands" : 59,
    "spain" : 82
}

AVAILABLE_RACES = ["netherlands", "spain"]
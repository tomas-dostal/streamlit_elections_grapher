import os
from enum import Enum


def map_range_from_to(val, in_min, in_max, out_min, out_max):
    return (val - in_min) / (in_max - in_min) * (out_max - out_min) + out_min


def get_terminal_size():
    try:
        return os.get_terminal_size()[0]
    # output is most likely redirected to an IDE
    except OSError as e:
        return 100


class States(Enum):
    SEARCH = 1
    UPDATE_DATA = 2
    STATUS = 3
    VIEW_GRAPH = 4
    MULTIPLE_OPTIONS = 5
    NO_OPTIONS = 6


def clear():
    return os.system('clear')

NUTS = (
    "CZ0100", "CZ0201", "CZ0202", "CZ0203", "CZ0204", "CZ0205", "CZ0206", "CZ0207", "CZ0208", "CZ0209", "CZ0311",
    "CZ0312",
    "CZ0313", "CZ0314", "CZ0315", "CZ0316", "CZ0317", "CZ0321", "CZ0322", "CZ0323", "CZ0324", "CZ0325", "CZ0326",
    "CZ0327",
    "CZ0411", "CZ0412", "CZ0413", "CZ0421", "CZ0422", "CZ0423", "CZ0424", "CZ0425", "CZ0426", "CZ0427", "CZ0511",
    "CZ0512",
    "CZ0513", "CZ0514", "CZ0521", "CZ0522", "CZ0523", "CZ0524", "CZ0525", "CZ0531", "CZ0532", "CZ0533", "CZ0534",
    "CZ0631",
    "CZ0632", "CZ0633", "CZ0634", "CZ0635", "CZ0641", "CZ0642", "CZ0643", "CZ0644", "CZ0645", "CZ0646", "CZ0647",
    "CZ0711",
    "CZ0712", "CZ0713", "CZ0714", "CZ0715", "CZ0721", "CZ0722", "CZ0723", "CZ0724", "CZ0801", "CZ0802", "CZ0803",
    "CZ0804",
    "CZ0805", "CZ0806"
)

PARTIES = {
    "1": "ODS",
    "2": "ŘN - VU",
    "3": "CESTA",
    "4": "ČSSD",
    "5": "PB",
    "6": "RČ",
    "7": "STAN",
    "8": "KSČM",
    "9": "Zelení",
    "10": "Rozumní",
    "11": "SPDV",
    "12": "Svobodní",
    "13": "BPI",
    "14": "ODA",
    "15": "Piráti",
    "16": "OBČANÉ 2011",
    "17": "Unie H.A.V.E.L.",
    "18": "ČNF",
    "19": "Referendum o EU",
    "20": "TOP 09",
    "21": "ANO",
    "22": "DV 2016",
    "23": "SPRRSČ M.Sládka",
    "24": "KDU-ČSL",
    "25": "ČSNS",
    "26": "REAL",
    "27": "SPORTOVCI",
    "28": "DSSS",
    "29": "SPD",
    "30": "SPO",
    "31": "NáS"
}

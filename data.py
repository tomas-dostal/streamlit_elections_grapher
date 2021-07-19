import pandas as pd
import xmltodict
import requests
import logging
import threading
import os

NUTS = (
    "CZ0100", "CZ0201", "CZ0202", "CZ0203", "CZ0204", "CZ0205", "CZ0206", "CZ0207", "CZ0208", "CZ0209", "CZ0311", "CZ0312",
    "CZ0313", "CZ0314", "CZ0315", "CZ0316", "CZ0317", "CZ0321", "CZ0322", "CZ0323", "CZ0324", "CZ0325", "CZ0326", "CZ0327",
    "CZ0411", "CZ0412", "CZ0413", "CZ0421", "CZ0422", "CZ0423", "CZ0424", "CZ0425", "CZ0426", "CZ0427", "CZ0511", "CZ0512",
    "CZ0513", "CZ0514", "CZ0521", "CZ0522", "CZ0523", "CZ0524", "CZ0525", "CZ0531", "CZ0532", "CZ0533", "CZ0534", "CZ0631",
    "CZ0632", "CZ0633", "CZ0634", "CZ0635", "CZ0641", "CZ0642", "CZ0643", "CZ0644", "CZ0645", "CZ0646", "CZ0647", "CZ0711",
    "CZ0712", "CZ0713", "CZ0714", "CZ0715", "CZ0721", "CZ0722", "CZ0723", "CZ0724", "CZ0801", "CZ0802", "CZ0803", "CZ0804",
    "CZ0805", "CZ0806"
)


class Data:
    def __init__(self):

        self.df = pd.DataFrame(data={})
        # https://volby.cz/pls/ps2017nss/vysledky_okres?nuts=CZ0806

        self.update()

    def update(self):

        self.df.drop(self.df.index, inplace=True)
        self.df = pd.DataFrame(data={})
        for nuts in NUTS:
            self.__fetch_data(nuts)

    def __fetch_data(self, nuts):

        url = "https://volby.cz/pls/ps2017nss/vysledky_okres?nuts={}".format(nuts)
        r = requests.get(url, allow_redirects=True)
        filename = '{}.xml'.format(nuts)
        open(filename, 'wb').write(r.content)

        tmp_data = [] # performing concat once finished is cheaper that an appeind in for cycle
        with open(filename) as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
            res = data_dict.get("VYSLEDKY_OKRES")
            district = res.get("OKRES")
            cities = res.get("OBEC")

            for city in cities:
                votes = city.get("HLASY_STRANA")
                for party in votes:
                    tmp_data.append(
                        {
                            'district_name': district["@NAZ_OKRES"],
                             # 'nuts_code': district["@NUTS_OKRES"],
                             'city_name': city["@NAZ_OBEC"],
                             'party_id': party["@KSTRANA"],
                             'party_votes_percent': party["@PROC_HLASU"],
                             'total_votes': city["UCAST"]["@PLATNE_HLASY"]
                         }
                    )

        os.remove(filename)

        # Finally save everything to the Pandas DataFrame
        #self.df. = pd.DataFrame(list(tmp_data.items()), columns=['district_name', 'city_name', 'party_id', 'party_votes_percent', 'total_votes'])

        self.df = self.df.append(tmp_data)

from multiprocessing.pool import ThreadPool

import pandas as pd
import requests
import xmltodict

from helper import *


class Data:

    def __init__(self):

        self.df = pd.DataFrame(data={})
        # https://volby.cz/pls/ps2017nss/vysledky_okres?nuts=CZ0806
        self.downloaded = 0
        self.to_download = len(NUTS)
        print("Data.update __init___")
        return

    # another approach would be having an index of what cities/towns are in NUTS and then
    # download only needed data.

    def update(self):

        # It there was a change, then without a diff it is cheaper (and much faster) to delete everything
        # and extract again.
        # possible improvements: Keep hashes of already downloaded files.
        # If newly downloaded file has the same hash, I don't need to extract it
        self.df.drop(self.df.index, inplace=True)
        self.df = pd.DataFrame(data={})

        # Multithreading helps a lot here.
        # ~ 2.717305s - with multithreading
        # ~ 18.856571s - without multithreading
        # still very slow though
        print("Downloading data...")

        pool = ThreadPool(processes=32)
        # launching multiple evaluations asynchronously may use more processes
        multiple_results = [pool.apply_async(
            Data.__fetch_data, (self, nuts)) for nuts in NUTS]
        [self.__add_to_dataframe(res.get(timeout=10))
         for res in multiple_results]

        print("\n{} entries imported".format(len(self.df)))

    def __add_to_dataframe(self, x):
        print("#", end="")
        self.df = self.df.append(x)

    def __fetch_data(self, nuts):

        url = "https://volby.cz/pls/ps2017nss/vysledky_okres?nuts={}".format(
            nuts)
        r = requests.get(url, allow_redirects=True)

        while r.status_code != 200:
            r = requests.get(url, allow_redirects=True)
            print('Retrying {}!'.format(nuts))

        filename = '{}.xml'.format(nuts)
        open(filename, 'wb').write(r.content)

        tmp_data = []  # performing concat once finished is cheaper that an append in foreach

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
                            'city_id': city["@CIS_OBEC"],
                            'city_name': city["@NAZ_OBEC"],
                            'party': party["@KSTRANA"],
                            'party_votes_percent': party["@PROC_HLASU"],
                            'total_votes': city["UCAST"]["@PLATNE_HLASY"]
                        }
                    )

        os.remove(filename)
        # need to add data to pandas in the main thread, otherwise it causes data loss
        return tmp_data

    def find_places_by_name(self, qu):
        # qu = "nová ves"
        # todo: make it case insensitive
        res = self.df.loc[self.df['city_name'].str.startswith(qu)]
        # res = self.df.loc[str.lower(self.df['city_name'].str).contains(qu, case=False)]
        options = res[["city_id", "city_name",
                       "district_name"]].drop_duplicates()

        return options

    def get_votes_by_city_id(self, id):
        return self.df.loc[self.df['city_id'] == str(id)]

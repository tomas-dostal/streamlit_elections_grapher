#!/usr/bin/python

# Napište command line utilitu, která pro zadaný název obce zobrazí barevný graf výsledků voleb.
# Zajímá nás procentní zisk politických stran v rámci dané obce.
# Jako zdroj dat použijte https://volby.cz/pls/ps2017nss/ps?xjazyk=CZ
# (strojově čitelná data jsou k dispozici tady https://volby.cz/opendata/ps2017nss/ps2017nss_opendata.htm)
#
# Poznámky:
# - vstup může být interaktivní nebo přes command line argument
# - graf postačí sloupcový, nějaký pěkně formátovaný barevný výstup do konzole
# - předpokládejme, že data volebních zisků jsou proměnná, jako kdyby byla právě sčítána. Jinými slovy, utilita by měla volební zisky vždy načítat ze stránek volby.cz
# - naopak číselník obcí s jejich názvy a kódy můžete považovat za statický
# - názvy obcí v ČR nejsou unikátní, v případě zadaní takového jména ať aplikace nechá uživatele interaktivně vybrat tu správnou.
# - plus bude, pokud pří opakovaném spuštění pro další obce budou zachované barvy u jednotlivých stran.
#
import argparse
import sys

from streamlit import cli as stcli

import app
from data import Data

# init it here to prevent object creating every time a streamlit app window is refreshed
data = Data()
data.update()


def main(args):
    if args.streamlit:
        sys.argv = ["streamlit", "run", "streamlit_app.py"]
        sys.exit(stcli.main())
    else:
        app.App().run(location=args.place)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Elections graphs')
    parser.add_argument(
        '-p', '--place', help="Specify target city/village by name to view election charts")
    parser.add_argument('-s', '--streamlit',
                        help="Run application in the streamlit mode",
                        type=bool,
                        nargs='?',
                        const=True,
                        default=False)
    args = parser.parse_args()
    if args.streamlit and args.place:
        print("Cannot run a streamlit app with parameter --place, ignoring")
    main(args)

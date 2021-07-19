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

import datetime
import getopt, sys
import data

def main(argv):
   # Remove 1st argument from the
   # list of command line arguments
   argumentList = sys.argv[1:]

   # Options
   options = "sp:"

   # Long options
   long_options = ["streamlit", "place"]

   try:
      # Parsing argument
      arguments, values = getopt.getopt(argumentList, options, long_options)

      # checking each argument
      for currentArgument, currentValue in arguments:

         if currentArgument in ("-h", "--help"):
            print("Help")

         elif currentArgument in ("-s", "--streamlit"):
            print("Run as streamlit app in browser", sys.argv[0])

         elif currentArgument in ("-p", "--place"):
            print(("Specify target city/village by name") % (currentValue))

   except getopt.error as err:
      # output error, and return with an error code
      print(str(err))

   start = datetime.datetime.now()
   d = data.Data()
   print(datetime.datetime.now() - start)


if __name__ == "__main__":
   main(sys.argv[1:])


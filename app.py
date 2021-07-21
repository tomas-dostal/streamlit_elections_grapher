import os
import datetime
from data import Data
from data import PARTIES
from simple_term_menu import TerminalMenu
from termgraph import termgraph as tg
from helper import map_range_from_to
from helper import get_terminal_size
from helper import States


class App:
    def __init__(self):
        # insert name of the place
        pass

    def run(self, location=None):

        # Final state machine
        # type in place / receive in an argument
        # If unique result found, view graph
        #   - return to start
        #   - exit
        # If multiple options available, select one
        #   - exit
        # If no options available,
        #   - re-fetch data
        #   - return to start
        #   - exit

        def clear():
            return os.system('clear')

        current_state = States.UPDATE_DATA
        next_state = States.SEARCH

        while True:
            if current_state == States.SEARCH:
                clear()
                print("Elections grapher")
                # if not argument in console:
                if not location:
                    place = input("Search place... ")
                else:
                    place = location  # parsed argument from command line
                if place != '':
                    options = self.d.find_places_by_name(place)
                    next_state = States.STATUS
                else:
                    print("No input")
                    no_input = TerminalMenu(["Search again", "Exit"])
                    index = no_input.show()
                    if index == 1:
                        exit(0)
                    elif index == 0:
                        next_state = States.SEARCH

            elif current_state == States.UPDATE_DATA:
                start = datetime.datetime.now()
                self.d = Data()
                print(datetime.datetime.now() - start)

                next_state = States.SEARCH

            elif current_state == States.STATUS:
                if len(options) > 1:
                    next_state = States.MULTIPLE_OPTIONS
                elif len(options) == 1:
                    votes = self.d.get_votes_by_city_id(
                        int(options["city_id"]))
                    if location:
                        next_state = States.MULTIPLE_OPTIONS
                    else:
                        next_state = States.VIEW_GRAPH
                else:
                    next_state = States.NO_OPTIONS

            elif current_state == States.VIEW_GRAPH:
                # party names
                clear()
                print("Viewing elections results in {} [{}]".format(votes.iloc[0]["city_name"],
                                                                    votes.iloc[0]["district_name"]))
                print("------------------------------------")
                # change to parties names
                involved_parties_color = [
                    int(x) + 80 for x in list(votes["party"])]
                involved_parties = votes["party"].replace(
                    PARTIES)  # replace ID by NAME
                labels = list(involved_parties)

                percents = [float(x)
                            for x in list(votes["party_votes_percent"])]
                # no every party candidated in specific region.
                # parties_names = map(PARTIES.get, place["party_id"].values.tolist())
                # place["party/"]
                data = [[x] for x in percents]

                # let's scale graph according to the current width of terminal.
                normal_data = [
                    [map_range_from_to((x), 0, 100, 0, get_terminal_size())] for x in percents]
                len_categories = 1
                args = {
                    'filenam': 'data/ex4.dat',
                    'title': "Viewing elections results in {} [{}]".
                        format(
                        votes.iloc[0]["city_name"],
                        votes.iloc[0]["district_name"]
                    ), 'width': 80,
                    'format': '{:<5.2f}',
                    'suffix': '',
                    'no_labels': False,
                    'color': True,
                    'vertical': False,
                    'stacked': True,
                    'different_scale': False,
                    'calendar': False,
                    'start_dt': None,
                    'custom_tick': '',
                    'delim': '',
                    'verbose': True,
                    'version': False
                }
                tg.stacked_graph(labels, data, normal_data,
                                 len_categories, args, involved_parties_color)

                multiple_options = TerminalMenu(
                    ["Search again", "Exit"]
                )
                view_index = multiple_options.show()
                if view_index == 1:
                    exit(0)
                elif view_index == 0:
                    next_state = States.SEARCH

            elif current_state == States.MULTIPLE_OPTIONS:
                clear()
                print(
                    "Multiple possibilities for input '{}', please specify: ".format(place))
                show_options = min(len(options), 9)

                options_str = ["{} [{}]".format(options.iloc[i]["city_name"], options.iloc[i]["district_name"]) for i in
                               range(0, show_options)] + ["Search again", "Exit"]

                multiple_options = TerminalMenu(
                    options_str
                )
                view_index = multiple_options.show()
                if view_index == (show_options - 1) + 2:
                    exit(0)
                elif view_index == (show_options - 1) + 1:
                    location = None  # clear location I got from command line
                    next_state = States.SEARCH
                else:
                    votes = self.d.get_votes_by_city_id(
                        int(options.iloc[view_index]["city_id"]))
                    next_state = States.VIEW_GRAPH

            elif current_state == States.NO_OPTIONS:
                print("Nothing found. ")

                multiple_options = TerminalMenu(
                    ["Search again", "Update local data", "Exit"]
                )
                index = multiple_options.show()
                if index == 2:
                    exit(0)
                elif index == 1:
                    next_state = States.UPDATE_DATA
                elif index == 0:
                    location = None  # clear location I got from command line
                    next_state = States.SEARCH
            current_state = next_state

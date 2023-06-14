from dataset_reader import AFFINITY_GRAPH_PATH, get_friends
from edge_rank import get_sorted_statuses
from affinity_graph import AffinityGraph
from user_interface import *
from logging import *
import time

LOGGING = False
USER = 'Chad Bruce'

if LOGGING:
    basicConfig(format='%(message)s')
    StreamHandler.terminator = '\r'
    getLogger().setLevel(INFO)


def main():
    affinity_graph = AffinityGraph()
    # affinity_graph.generate_graph()
    # affinity_graph.save_graph(AFFINITY_GRAPH_PATH)
    affinity_graph.load_graph(AFFINITY_GRAPH_PATH)
    users = get_friends(True)

    while True:
        while True:
            option = welcome_menu()
            if option == None:
                exit()
            user = None if option == 1 else login(users)
            if user == None or user != '':
                break

        sorted_statuses = get_sorted_statuses(affinity_graph, user)

        while True:
            option = app_menu()
            if option == None:
                break
            elif option == 1:
                show_feed(sorted_statuses)
            elif option == 2:
                show_search(sorted_statuses)

        print(option)


if __name__ == "__main__":
    start_time = time.time()
    main()
    info('\033[K\nTotal:  %.4f seconds\n\n\n' % (time.time() - start_time))

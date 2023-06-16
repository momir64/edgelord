from dataset_reader import AFFINITY_GRAPH_PATH, get_friends, get_statuses
from affinity_graph import AffinityGraph
from status_trie import StatusTrie
from user_interface import *
from logging import info
from edgerank import *
import time


def main():
    users = get_friends(True)
    statuses = get_statuses()
    affinity_graph = AffinityGraph()
    statuses_trie = StatusTrie(statuses)
    affinity_graph.load_graph(AFFINITY_GRAPH_PATH)

    while True:
        while True:
            option = welcome_menu()
            if option == None:
                exit()
            user = None if option == 1 else login(users)
            if user == None or user != '':
                break

        statuses_edgerank = get_edgeranked_statuses(affinity_graph, user, statuses)

        while True:
            option = app_menu()
            if option == None:
                break
            elif option == 1:
                show_statuses(sort_by_edgerank(statuses_edgerank))
            elif option == 2:
                show_search(statuses_trie)


if __name__ == "__main__":
    start_time = time.time()

    # search = '"donald j. trump" trump'
    # suggestions = statuses_trie.get_suggestion('tru')
    # statuses_search, underline_words = statuses_trie.search(search)
    # show_statuses(sort_by_search_and_edgerank(statuses_sorted), underline_words)

    main()
    info('\033[K\nTotal:  %.4f seconds\n\n\n' % (time.time() - start_time))

from dataset_reader import AFFINITY_GRAPH_PATH, get_friends, get_statuses
from affinity_graph import AffinityGraph
from status_trie import StatusTrie
from operator import itemgetter
from user_interface import *
from logging import info
from edgerank import *
import time


def main():
    affinity_graph = AffinityGraph()
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

        statuses_edgerank = sort_edgeranked_statuses(get_edgeranked_statuses(affinity_graph, user))

        while True:
            option = app_menu()
            if option == None:
                break
            elif option == 1:
                show_statuses(statuses_edgerank)
            elif option == 2:
                show_search(statuses_edgerank)

        print(option)


if __name__ == "__main__":
    start_time = time.time()

    affinity_graph = AffinityGraph()
    affinity_graph.load_graph(AFFINITY_GRAPH_PATH)

    statuses = get_statuses()
    statuses_edgerank = get_edgeranked_statuses(affinity_graph, None, statuses)

    statuses_trie = StatusTrie()
    for status in statuses.values():
        statuses_trie.add_status(status)

    statuses_search = statuses_trie.search('pet')

    statuses_result = {}
    for id, search_score in statuses_search.items():
        statuses_edgerank[id]['search'] = search_score
        statuses_result[id] = statuses_edgerank[id]

    statuses_sorted = sorted(statuses_result.values(), key=itemgetter('search', 'edgerank'), reverse=True)
    show_statuses(sort_edgeranked_statuses(statuses_edgerank))

    # main()
    info('\033[K\nTotal:  %.4f seconds\n\n\n' % (time.time() - start_time))

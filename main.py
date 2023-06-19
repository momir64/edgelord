from dataset_reader import AFFINITY_GRAPH_PATH, get_friends, get_statuses
from affinity_graph import AffinityGraph
from status_trie import StatusTrie
from user_interface import *
from edgerank import *


def main():
    users = get_friends(True)
    statuses = get_statuses()
    affinity_graph = AffinityGraph()
    statuses_trie = StatusTrie(statuses)
    affinity_graph.load_graph(AFFINITY_GRAPH_PATH)

    while True:
        while True:
            option = login_menu()
            if option == None:
                show_cursor()
                exit()
            user = None if option == 1 else login_prompt(users)
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
                while True:
                    search = show_search(statuses_trie)
                    if search == None or search == '':
                        break

                    statuses_search, underline_words = statuses_trie.search(search, statuses_edgerank)
                    show_statuses(sort_by_search_and_edgerank(statuses_search), underline_words)


if __name__ == "__main__":
    main()
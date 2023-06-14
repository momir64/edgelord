from dataset_reader import AFFINITY_GRAPH_PATH
from edge_rank import get_sorted_statuses
from affinity_graph import AffinityGraph
from logging import *
import time

LOGGING = True
USER = 'Chad Bruce'

if LOGGING:
    basicConfig(format='%(message)s')
    StreamHandler.terminator = '\r'
    getLogger().setLevel(INFO)


def main():
    affinity_graph = AffinityGraph()

    # affinity_graph.generate_graph()
    # affinity_graph.save_graph(AFFINITY_GRAPH_FILENAME)

    affinity_graph.load_graph(AFFINITY_GRAPH_PATH)

    sorted_statuses = get_sorted_statuses(affinity_graph, USER)

    print(sorted_statuses)

if __name__ == "__main__":
    start_time = time.time()
    main()
    info('\033[K\nTotal:  %.4f seconds\n\n\n' % (time.time() - start_time))

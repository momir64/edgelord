from affinity_graph import AffinityGraph
from dataset_reader import get_statuses
from logging import *
import time

LOGGING = True
AFFINITY_GRAPH_FILENAME = 'affinity.graph'

if LOGGING:
    basicConfig(format='%(message)s')
    StreamHandler.terminator = '\r'
    getLogger().setLevel(INFO)

def load_statuses():
    info(f'█  Loading statuses')
    start_time = time.time()
    statuses = get_statuses()
    info(f'✓  {"Loading statuses:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n\n')
    return statuses

def main():
    # statuses = load_statuses()
    affinity_graph = AffinityGraph()
    affinity_graph.load_graph(AFFINITY_GRAPH_FILENAME)
    print(affinity_graph)
    # affinity_graph.generate_graph(statuses)
    # affinity_graph.save_graph(AFFINITY_GRAPH_FILENAME)

if __name__ == "__main__":
    start_time = time.time()
    main()
    info('\033[K\nTotal:  %.4f seconds\n\n\n' % (time.time() - start_time))

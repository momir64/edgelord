from dataset_reader import AFFINITY_GRAPH_PATH
from affinity_graph import AffinityGraph
from logging import *
import time

LOGGING = True
if LOGGING:
    basicConfig(format='%(message)s')
    StreamHandler.terminator = '\r'
    getLogger().setLevel(INFO)

def main():
    affinity_graph = AffinityGraph()
    affinity_graph.generate_graph()
    affinity_graph.save_graph(AFFINITY_GRAPH_PATH)

if __name__ == "__main__":
    start_time = time.time()
    main()
    info('\033[K\nTotal:  %.4f seconds\n\n\n' % (time.time() - start_time))

from dataset_reader import get_statuses
from time_decay import get_time_decay
from operator import itemgetter
from datetime import datetime
from logging import info
import time

REACTION_AFFINITY_WEIGHT = 2
COMMENT_AFFINITY_WEIGHT = 5
SHARE_AFFINITY_WEIGHT = 10
AFFINITY_REDUCTION = 500
WEIGHT_REDUCTION = 3000


def get_sorted_statuses(affinity_graph=None, user=None):
    info(f'█  Loading statuses')
    start_time = time.time()
    statuses = get_statuses(True)
    info(f'✓  {"Loading statuses:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')

    info(f'█  Sorting statuses')
    start_time = time.time()
    current_date = datetime.now()
    for status in statuses:
        status['affinity'] = 1 if not affinity_graph or not user else (affinity_graph.get_affinity(user, status['author']) / AFFINITY_REDUCTION)
        status['weight'] = (status['reactions'] * REACTION_AFFINITY_WEIGHT + status['comments'] * COMMENT_AFFINITY_WEIGHT + status['shares'] * SHARE_AFFINITY_WEIGHT) / WEIGHT_REDUCTION
        status['time_decay'] = get_time_decay(status['date'], current_date)
        status['edgerank'] = status['affinity'] * status['weight'] * status['time_decay']
    sorted_statuses = sorted(statuses, key=itemgetter('edgerank'), reverse=True)
    info(f'✓  {"Sorting statuses:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n\n')

    return sorted_statuses

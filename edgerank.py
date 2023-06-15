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


def get_edgeranked_statuses(affinity_graph=None, user=None, statuses=None):
    if not statuses:
        info(f'█  Loading statuses')
        start_time = time.time()
        statuses = get_statuses()
        info(f'✓  {"Loading statuses:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')

    info(f'█  Calculating edgerank score')
    start_time = time.time()
    current_date = datetime.now()
    for status in statuses.values():
        status['affinity'] = 1 if not affinity_graph or not user else (affinity_graph.get_affinity(user, status['author']) / AFFINITY_REDUCTION)
        status['weight'] = (status['reactions'] * REACTION_AFFINITY_WEIGHT + status['comments'] * COMMENT_AFFINITY_WEIGHT + status['shares'] * SHARE_AFFINITY_WEIGHT) / WEIGHT_REDUCTION
        status['time_decay'] = get_time_decay(status['date'], current_date)
        status['edgerank'] = status['affinity'] * status['weight'] * status['time_decay']
    info(f'✓  {"Calculating edgerank score:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n\n')

    return statuses


def sort_by_edgerank(statuses):
    return sorted(statuses.values(), key=itemgetter('edgerank'), reverse=True)


def sort_by_search_and_edgerank(statuses):
    return sorted(statuses.values(), key=itemgetter('search', 'edgerank'), reverse=True)

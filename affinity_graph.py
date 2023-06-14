from time_decay import get_time_decay
from datetime import datetime
from dataset_reader import *
from logging import info
import numpy as np
import pickle
import time


class AffinityGraph:
    def __init__(self, friend_affinity_weight=1000, reaction_affinity_weight=25, comment_affinity_weight=50, share_affinity_weight=100, affinity_of_friends_weight=0.05, affinity_of_friends_friends_weight=0.005):
        self.__friend_affinity_weight__ = friend_affinity_weight
        self.__reaction_affinity_weight__ = reaction_affinity_weight
        self.__comment_affinity_weight__ = comment_affinity_weight
        self.__share_affinity_weight__ = share_affinity_weight

        self.__affinity_of_friends_weight__ = int(1 / affinity_of_friends_weight)
        self.__affinity_of_friends_friends_weight__ = int(1 / affinity_of_friends_friends_weight)

        self.__adjacency_matrix__ = np.zeros(0)
        self.__name_to_index__ = {}
        self.__nodes_count__ = 0


    def __add_friend_affinity__(self, friends):
        start_time = time.time()
        for i, user in enumerate(friends):
            for friend in friends[user]:
                self.__adjacency_matrix__[self.__name_to_index__[user], self.__name_to_index__[friend]] += self.__friend_affinity_weight__
            info(f'█  {"Friends:".ljust(32)}{(str(i + 1) + "/" + str(self.__nodes_count__)).rjust(20)}')
        info(f'✓  {"Friends:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')


    def __add_affinity_of_friends__(self, affinity_graph_original, friends):
        start_time = time.time()
        for i, user in enumerate(friends):
            for friend in friends[user]:
                self.__adjacency_matrix__[self.__name_to_index__[user]] += affinity_graph_original[self.__name_to_index__[friend]] // self.__affinity_of_friends_weight__
            info(f'█  {"Affinity of friends:".ljust(32)}{(str(i + 1) + "/" + str(self.__nodes_count__)).rjust(20)}')
        info(f'✓  {"Affinity of friends:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')


    def __add_affinity_of_friends_friends__(self, affinity_graph_original, friends):
        start_time = time.time()
        for i, user in enumerate(friends):
            friends_count = len(friends[user])
            for j, friend in enumerate(friends[user]):
                for friend_of_friend in friends[friend]:
                    self.__adjacency_matrix__[self.__name_to_index__[user]] += affinity_graph_original[self.__name_to_index__[friend_of_friend]] // self.__affinity_of_friends_friends_weight__
                remaining = ((time.time() - start_time) / (i + 1) * (self.__nodes_count__ - i - 1)) // 60
                info(f'█  {"Affinity of friends friends:".ljust(32)}{(str(i + 1) + "/" + str(self.__nodes_count__)).rjust(10)}{(str(j + 1) + "/" + str(friends_count)).rjust(10)}   ETA: {"%d minute" % remaining}{"s" if remaining != 1 else ""}\033[K')
        info(f'✓  {"Affinity of friends friends:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')


    def __add_action_affinity__(self, statuses, activites, activity_weight, activity_name="Activities"):
        start_time = time.time()
        activity_count = len(activites)
        for i, activity in enumerate(activites):
            self.__adjacency_matrix__[self.__name_to_index__[activity['author']], self.__name_to_index__[statuses[activity['status']]['author']]] += activity_weight * get_time_decay(activity['date'], self.__current_date__)
            info(f'█  {(activity_name + ":").ljust(32)}{(str(i + 1) + "/" + str(activity_count)).rjust(20)}')
        info(f'✓  {(activity_name + ":").ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')


    def generate_graph(self):
        self.__current_date__ = datetime.now()

        info('Loading data:\n')

        info(f'█  Statuses')
        start_time = time.time()
        statuses = get_statuses()
        info(f'✓  {"Statuses:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n\n')

        info(f'█  Friends')
        start_time = time.time()
        self.__nodes_count__, self.__name_to_index__, friends = get_friends()
        info(f'✓  {"Friends:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')

        info(f'█  Comments')
        start_time = time.time()
        comments = get_comments()
        info(f'✓  {"Comments:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')

        info(f'█  Reactions')
        start_time = time.time()
        reactions = get_reactions()
        info(f'✓  {"Reactions:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')

        info(f'█  Shares')
        start_time = time.time()
        shares = get_shares()
        info(f'✓  {"Shares:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')

        self.__adjacency_matrix__ = np.zeros((self.__nodes_count__, self.__nodes_count__), dtype=np.int32)

        info('\nAdding affinity for:\n')
        self.__add_friend_affinity__(friends)
        self.__add_action_affinity__(statuses, comments, self.__comment_affinity_weight__, 'Comments')
        self.__add_action_affinity__(statuses, reactions, self.__reaction_affinity_weight__, 'Reactions')
        self.__add_action_affinity__(statuses, shares, self.__share_affinity_weight__, 'Shares')

        affinity_graph_original = self.__adjacency_matrix__.copy()
        self.__add_affinity_of_friends__(affinity_graph_original, friends)

        # za uračunavanje i afiniteta prijatelja od prijatelja je potrebno ~50 minuta
        # self.add_affinity_of_friends_friends(affinity_graph_original, friends)


    def get_affinity(self, of_user, towards_user):
        return self.__adjacency_matrix__[self.__name_to_index__[of_user], self.__name_to_index__[towards_user]].item()


    def save_graph(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.__adjacency_matrix__, self.__name_to_index__, self.__nodes_count__), file)


    def load_graph(self, filename):
        with open(filename, 'rb') as file:
            self.__adjacency_matrix__, self.__name_to_index__, self.__nodes_count__ = pickle.load(file)

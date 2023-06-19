from time_decay import get_time_decay
from datetime import datetime
import multiprocessing as mp
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


    def __add_affinity_of_friends_friends_thread__(self, affinity_graph_original, users, friends):
        tmp_adjacency_matrix = np.zeros((self.__nodes_count__, self.__nodes_count__), dtype=np.int32)
        for user in users:
            for friend in friends[user]:
                for friend_of_friend in friends[friend]:
                    tmp_adjacency_matrix[self.__name_to_index__[user]] += affinity_graph_original[self.__name_to_index__[friend_of_friend]] // self.__affinity_of_friends_friends_weight__
        return tmp_adjacency_matrix


    def __add_affinity_of_friends_friends_parallel__(self, affinity_graph_original, friends):
        start_time = time.time()
        info(f'█  {"Affinity of friends friends:".ljust(32)}{"...parallel".rjust(20)}')
        parts = [(affinity_graph_original, users_part, friends) for users_part in np.array_split(list(friends.keys()), mp.cpu_count())]
        results = mp.Pool(mp.cpu_count()).starmap(self.__add_affinity_of_friends_friends_thread__, parts)
        self.__adjacency_matrix__ += np.sum(results, 0)
        info(f'✓  {"Affinity of friends friends:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')


    def __add_action_affinity__(self, statuses, activites, activity_weight, activity_name="Activities"):
        start_time = time.time()
        activity_count = len(activites)
        for i, activity in enumerate(activites):
            self.__adjacency_matrix__[self.__name_to_index__[activity['author']], self.__name_to_index__[statuses[activity['status']]['author']]] += activity_weight * get_time_decay(activity['date'], self.__current_date__)
            info(f'█  {(activity_name + ":").ljust(32)}{(str(i + 1) + "/" + str(activity_count)).rjust(20)}')
        info(f'✓  {(activity_name + ":").ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')


    def __add_action_affinity_thread__(self, statuses, activites, activity_weight):
        tmp_adjacency_matrix = np.zeros((self.__nodes_count__, self.__nodes_count__), dtype=np.int32)
        for activity in activites:
            tmp_adjacency_matrix[self.__name_to_index__[activity['author']], self.__name_to_index__[statuses[activity['status']]['author']]] += activity_weight * get_time_decay(activity['date'], self.__current_date__)
        return tmp_adjacency_matrix


    def __add_action_affinity_parallel__(self, statuses, activites, activity_weight, activity_name="Activities"):
        start_time = time.time()
        info(f'█  {(activity_name + ":").ljust(32)}{"...parallel".rjust(20)}')
        parts = [(statuses, activites_part, activity_weight) for activites_part in np.array_split(activites, mp.cpu_count())]
        results =  mp.Pool(mp.cpu_count()).starmap(self.__add_action_affinity_thread__, parts)
        self.__adjacency_matrix__ += np.sum(results, 0)
        info(f'✓  {(activity_name + ":").ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')


    def generate_graph(self):
        self.__current_date__ = datetime.now()

        info('Loading data:\n')

        info(f'█  {"Statuses:".ljust(32)}{"...loading".rjust(20)}')
        start_time = time.time()
        statuses = get_statuses()
        info(f'✓  {"Statuses:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')

        info(f'█  {"Friends:".ljust(32)}{"...loading".rjust(20)}')
        start_time = time.time()
        self.__nodes_count__, self.__name_to_index__, friends = get_friends()
        info(f'✓  {"Friends:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')

        info(f'█  {"Comments:".ljust(32)}{"...loading".rjust(20)}')
        start_time = time.time()
        comments = get_comments()
        info(f'✓  {"Comments:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')

        info(f'█  {"Reactions:".ljust(32)}{"...loading".rjust(20)}')
        start_time = time.time()
        reactions = get_reactions()
        info(f'✓  {"Reactions:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')

        info(f'█  {"Shares:".ljust(32)}{"...loading".rjust(20)}')
        start_time = time.time()
        shares = get_shares()
        info(f'✓  {"Shares:".ljust(32)}{("%.4f seconds" % (time.time() - start_time)).rjust(20)}\033[K\n')

        self.__adjacency_matrix__ = np.zeros((self.__nodes_count__, self.__nodes_count__), dtype=np.int32)

        info('\nAdding affinity for:\n')
        self.__add_friend_affinity__(friends)
        self.__add_action_affinity__(statuses, comments, self.__comment_affinity_weight__, 'Comments')
        self.__add_action_affinity_parallel__(statuses, reactions, self.__reaction_affinity_weight__, 'Reactions')
        self.__add_action_affinity_parallel__(statuses, shares, self.__share_affinity_weight__, 'Shares')

        affinity_graph_original = self.__adjacency_matrix__.copy()
        self.__add_affinity_of_friends__(affinity_graph_original, friends)

        # za uračunavanje i afiniteta prijatelja od prijatelja je potrebno ~7 minuta, a bez toga ~58 sekundi za ceo original dataset
        # self.__add_affinity_of_friends_friends_parallel__(affinity_graph_original, friends)


    def get_affinity(self, of_user, towards_user):
        return self.__adjacency_matrix__[self.__name_to_index__[of_user], self.__name_to_index__[towards_user]].item()


    def save_graph(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.__adjacency_matrix__, self.__name_to_index__, self.__nodes_count__), file)


    def load_graph(self, filename):
        with open(filename, 'rb') as file:
            self.__adjacency_matrix__, self.__name_to_index__, self.__nodes_count__ = pickle.load(file)

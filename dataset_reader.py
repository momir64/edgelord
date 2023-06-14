import pandas as pd

TESTING = False
FOLDER_PATH = 'dataset'
FRIENDS_PATH = 'friends.csv'
FILE_PREFIX = 'test' if TESTING else 'original'
SHARES_PATH = f'{FILE_PREFIX}_shares.csv'
STATUSES_PATH = f'{FILE_PREFIX}_statuses.csv'
COMMENTS_PATH = f'{FILE_PREFIX}_comments.csv'
REACTIONS_PATH = f'{FILE_PREFIX}_reactions.csv'
AFFINITY_GRAPH_PATH = 'affinity.graph'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_statuses(as_list=False):
    data = pd.read_csv(f'{FOLDER_PATH}/{STATUSES_PATH}', encoding='utf-8', index_col=None if as_list else 0, parse_dates=['status_published'], date_format=DATETIME_FORMAT)
    [['status_message', 'status_link', 'status_published', 'author', 'num_reactions', 'num_comments', 'num_shares',
      'num_likes', 'num_loves', 'num_wows', 'num_hahas', 'num_sads', 'num_angrys', 'num_special']]
    data.rename(columns={'status_message': 'message', 'status_link': 'link', 'status_published': 'date', 'num_reactions': 'reactions', 'num_comments': 'comments', 'num_shares': 'shares',
                         'num_likes': 'likes', 'num_loves': 'loves', 'num_wows': 'wows', 'num_hahas': 'hahas', 'num_sads': 'sads', 'num_angrys': 'angrys', 'num_special': 'special'}, inplace=True)
    return data.to_dict('records' if as_list else 'index')


def get_comments():
    data = pd.read_csv(f'{FOLDER_PATH}/{COMMENTS_PATH}', encoding='utf-8', parse_dates=['comment_published'], date_format=DATETIME_FORMAT)[['status_id', 'comment_published', 'comment_author']]
    data.rename(columns={'status_id': 'status', 'comment_published': 'date', 'comment_author': 'author'}, inplace=True)
    return data.to_dict('records')


def get_reactions():
    data = pd.read_csv(f'{FOLDER_PATH}/{REACTIONS_PATH}', encoding='utf-8', parse_dates=['reacted'], date_format=DATETIME_FORMAT)[['status_id', 'reacted', 'reactor']]
    data.rename(columns={'status_id': 'status', 'reacted': 'date', 'reactor': 'author'}, inplace=True)
    return data.to_dict('records')


def get_shares():
    data = pd.read_csv(f'{FOLDER_PATH}/{SHARES_PATH}', encoding='utf-8', parse_dates=['status_shared'], date_format=DATETIME_FORMAT)[['status_id', 'status_shared', 'sharer']]
    data.rename(columns={'status_id': 'status', 'status_shared': 'date', 'sharer': 'author'}, inplace=True)
    return data.to_dict('records')


def get_friends():
    data = pd.read_csv(f'{FOLDER_PATH}/{FRIENDS_PATH}', encoding='utf-8', converters={'friends': lambda x: x.split(';')})[['person', 'friends']]
    data['index'] = data.index
    data = data.set_index('person').to_dict('dict')
    return len(data['index']), data['index'], data['friends']

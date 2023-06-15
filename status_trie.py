from operator import itemgetter
import re

PHRASE_WEIGHT = 15
WORD_WEIGHT = 5
PART_WEIGHT = 1


class StatusTrieNode:
    def __init__(self, char, word):
        self.char = char
        self.word = word
        self.count = 0
        self.statuses = {}
        self.children = {}
        self.is_word = False


class StatusTrie:
    def __init__(self, statuses):
        self.root = StatusTrieNode('', '')
        for status in statuses.values():
            self.add_status(status)


    def add_status(self, status):
        text = status['message'].lower()
        node = self.root
        position = 0
        word = ''

        for char in text:
            if char.isalnum():
                word += char

                if char in node.children:
                    node = node.children[char]
                else:
                    node.children[char] = StatusTrieNode(char, word)
                    node = node.children[char]

                if status['id'] not in node.statuses:
                    node.statuses[status['id']] = {'parts_count': 0, 'word_positions': []}
                node.statuses[status['id']]['parts_count'] += 1
            elif word:
                node, position, word = self.__new_word_helper__(node, status['id'], position)

        if node.char != '':
            self.__new_word_helper__(node, status['id'], position)


    def __new_word_helper__(self, node, status, position):
        node.statuses[status]['word_positions'].append(position)
        node.statuses[status]['parts_count'] -= 1
        node.is_word = True
        node.count += 1
        return self.root, position + 1, ''


    def __get_node__(self, word):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node


    def search(self, prompt, edgerank):
        statuses = {}
        prompt += '"' if prompt.count('"') % 2 else ''
        phrases = re.findall('"([^"]*)"', prompt)
        prompt = re.sub('("[^"]*")', '', prompt)

        for phrase in phrases:
            statuses_phrase = self.__search_phrase__(phrase)
            for id in statuses_phrase:
                statuses[id] = statuses.setdefault(id, 0) + statuses_phrase[id]

        statuses_normal = self.__search_normal__(prompt)
        for id in statuses_normal:
            statuses[id] = statuses.setdefault(id, 0) + statuses_normal[id]

        statuses_result = {}
        for id, search_score in statuses.items():
            edgerank[id]['search'] = search_score
            statuses_result[id] = edgerank[id]
            
        return statuses_result, phrases + (prompt.split() if prompt != '' else [])


    def __search_normal__(self, prompt):
        statuses = {}
        words = re.sub(r'\s\s+', ' ', re.sub(r'[^\w\s]+', ' ', prompt)).strip().lower().split()
        if not len(words):
            return {}

        for word in words:
            node = self.__get_node__(word)
            if node == None or node.char == '':
                continue
            for id, value in node.statuses.items():
                statuses[id] = statuses.setdefault(id, 0) + len(value['word_positions']) * WORD_WEIGHT + value['parts_count'] * PART_WEIGHT

        return statuses


    def __search_phrase__(self, phrase):
        statuses = {}
        words = re.sub(r'\s\s+', ' ', re.sub(r'[^\w\s]+', ' ', phrase)).strip().lower().split()
        if not len(words):
            return {}

        for i, word in enumerate(words):
            node = self.__get_node__(word)
            if node == None or node.char == '':
                return {}
            if not i:
                for id, value in node.statuses.items():
                    statuses[id] = value['word_positions']
            else:
                statuses_tmp = {}
                for id in statuses:
                    positions = []
                    if id in node.statuses:
                        for position in statuses[id]:
                            if position + 1 in node.statuses[id]['word_positions']:
                                positions.append(position + 1)
                    if positions:
                        statuses_tmp[id] = positions
                statuses = statuses_tmp

        for id, value in statuses.items():
            statuses[id] = len(value) * PHRASE_WEIGHT

        return statuses


    def __dfs__(self, node):
        words = [(node.word, node.count)] if node.is_word else []
        for child in node.children.values():
            words += self.__dfs__(child)
        return words


    def get_suggestion(self, prefix):
        node = self.__get_node__(prefix)
        if node == None or node.char == '':
            return ''
        return [t[0] for t in sorted(self.__dfs__(node), key=itemgetter(1), reverse=True)]

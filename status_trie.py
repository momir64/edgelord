import re

WORD_WEIGHT = 5
PART_WEIGHT = 1


class StatusTrieNode:
    def __init__(self, char):
        self.char = char
        self.counter = 0
        self.statuses = {}
        self.children = {}
        self.is_word = False


class StatusTrie:
    def __init__(self):
        self.root = StatusTrieNode('')


    def add_status(self, status):
        text = status['message'].lower()
        node = self.root
        new_word = False
        position = 0

        for char in text:
            if char.isalnum():
                new_word = True

                if char in node.children:
                    node = node.children[char]
                else:
                    node.children[char] = StatusTrieNode(char)
                    node = node.children[char]

                if status['id'] not in node.statuses:
                    node.statuses[status['id']] = {'parts': 0, 'words': []}
                node.statuses[status['id']]['parts'] += 1
            elif new_word:
                node, position, new_word = self.new_word_helper(node, status['id'], position)
    
        if node.char != '':
            self.new_word_helper(node, status['id'], position)


    def new_word_helper(self, node, status, position):
        node.statuses[status]['words'].append(position)
        node.statuses[status]['parts'] -= 1
        node.is_word = True
        node.counter += 1
        return self.root, position + 1, False


    def get_node(self, word):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node


    def search(self, prompt):
        statuses = {}
        words = re.sub(r'\s\s+', ' ', re.sub(r'[^\w\s]+', ' ', prompt)).strip().lower().split()

        if not len(words):
            return {}

        for word in words:
            node = self.get_node(word)
            if node == None or node.char == '':
                continue
            for status, value in node.statuses.items():
                statuses[status] = statuses.setdefault(status, 0) + len(value['words']) * WORD_WEIGHT + value['parts'] * PART_WEIGHT

        return statuses



    def search_phrase(self, phrase):
        pass

    def get_suggestion(self, prefix):
        pass

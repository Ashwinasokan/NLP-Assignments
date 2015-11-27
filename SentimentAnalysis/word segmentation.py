class Trie(object):
    def __init__(self):
        self.children = {}
        self.count = 0  # Frequency

    def add(self, char):
        self.children[char] = Trie()

    def insert(self, word, count):
        node = self
        for char in word:
            if char not in node.children:
                node.add(char)
            node = node.children[char]
        node.count = count

    def max_match(self, word):
        node = self
        i = 0
        start = 0
        end = 0
        my_word_count = 0
        word_list = []
        while i <= len(word):
            if i == len(word):
                if my_word_count > 0:
                    word_list.append(word[start:end+1])
                    my_word_count = 0
                    start = i = end+1
                else:
                    if start < len(word):
                        word_list.append(word[start])
                    my_word_count = 0
                    start += 1
                    i = start
                continue
            char = word[i]
            if char in node.children:
                node = node.children[char]
                if node.count != 0:
                    my_word_count = node.count
                    end = i
                i += 1
            else:
                if my_word_count > 0:
                    word_list.append(word[start:end+1])
                    my_word_count = 0
                    start = i = end+1
                else:
                    word_list.append(word[start])
                    my_word_count = 0
                    start += 1
                    i = start
                node = self
        return word_list


    def min_match(self, word):
        """  Matched immediate words rather than waiting for longest word, just opposite to max match strategy"""
        node = self
        i = 0
        start = 0
        end = 0
        my_word_count = 0
        word_list = []
        while i <= len(word):
            if i == len(word):
                if my_word_count > 0:
                    word_list.append(word[start:end+1])
                    my_word_count = 0
                    start = i = end+1
                else:
                    if start < len(word):
                        word_list.append(word[start])
                    my_word_count = 0
                    start += 1
                    i = start
                continue
            char = word[i]
            if char in node.children:
                node = node.children[char]
                if node.count != 0:
                    end = i
                    word_list.append(word[start:end+1])
                    my_word_count = 0
                    i += 1
                    start = end = i
                else:
                    i += 1
            else:
                if my_word_count > 0:
                    word_list.append(word[start:end+1])
                    my_word_count = 0
                    start = i = end+1
                else:
                    word_list.append(word[start])
                    my_word_count = 0
                    start += 1
                    i = start
                node = self
        return word_list


def min_edit_distance(source, target):
    """ Computes the min edit distance from source to target"""
    source_words = source.split()
    target_words = target.split()
    m = len(source_words)
    n = len(target_words)

    distance = [[0 for i in range(n+1)] for j in range(m+1)]

    for i in range(1, m+1):
        distance[i][0] = distance[i-1][0] + 1

    for j in range(1, n+1):
        distance[0][j] = distance[0][j-1] + 1

    for i in range(1, m+1):
        for j in range(1, n+1):
            distance[i][j] = min(distance[i-1][j]+1, distance[i][j-1]+1,
                                 distance[i-1][j-1] + (0 if source_words[i-1] == target_words[j-1] else 1))

    return distance[m][n]


def word_error_rate(output, ideal):
    """ Computes the word error rate between output and ideal
    word error rate = minimum edit distance/no of words in ideal sentence """
    return min_edit_distance(output, ideal)/len(ideal.split())

dictionary = Trie()
big_word_list_file = open("bigwordlist.txt")
for i in range(1, 75001):
    words = big_word_list_file.readline().split()
    dictionary.insert(words[0], int(words[1]))
hash_tags_file = open("hashtags-test-2015.txt")
target = open("asokan-out-assgn1.txt", 'w')
for line in hash_tags_file:
    line = line.replace("#", "")
    words = dictionary.max_match(line)
    target.write(" ".join(words))

test_word_list_file = open("asokan-out-assgn1.txt")
reference_word_list_file = open("hashtags-train-reference.txt")
count = 0
cumulative_error_rate = 0
for test_sentence in test_word_list_file:
    reference_sentence = reference_word_list_file.readline()
    count += 1
    edit_distance = min_edit_distance(test_sentence, reference_sentence)
    error_rate = word_error_rate(test_sentence, reference_sentence)
    cumulative_error_rate += error_rate
    print(test_sentence,reference_sentence,edit_distance,error_rate)
print("Average WER" + str(cumulative_error_rate/count))
import math
import collections
import porter
import re
ps = porter.PorterStemmer()
negationRegex = re.compile("^.*(\bnot\b|n't|\bno\b|\bnever\b).*$")


def stem(lines, negate):
    result = []
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", lines)
    for sentence in sentences:
        seen_negative = False
        ws = sentence.split()
        for w in ws:
            stemmed = ps.stem(w, 0, len(w)-1)
            if seen_negative:
                result.append("!" + stemmed)
            else:
                result.append(stemmed)
            if negationRegex.match(stemmed) and negate:
                seen_negative = True
    return result
positiveWordCount = 0
positiveWords =[ ]
file = open('hotelPosT-train.txt', 'r')
for line in file:
    positiveWords.extend(set(stem(" ".join(line.lower().split()[1:]), True)))
positiveWordsCounter = collections.Counter(positiveWords)

negativeWordCount = 0
negativeWords =[ ]
file = open('hotelNegT-train.txt', 'r')
for line in file:
    negativeWords.extend(set(stem(" ".join(line.lower().split()[1:]), True)))
negativeWordsCounter = collections.Counter(negativeWords)

# file = open('test1[Random Sample].txt', 'r')
file = open('hotelDeceptionTest.txt', 'r')
result = open('hotelDeceptionTestSentiment.txt', 'a')
for line in file:
    positiveWeight = negativeWeight = 0
    positiveMiss = negativeMiss = 0
    words = line.lower().split()
    sent = " ".join(words[1:])
    words = set(stem(sent, True))
    for word in words:
        if word in positiveWordsCounter:
            pWeight = math.log(float(positiveWordsCounter.get(word) + 1)
                                         / float(len(positiveWords) + len(positiveWordsCounter.keys())))
        else:
            pWeight = math.log(1/float(len(positiveWords) + len(positiveWordsCounter.keys())))
            positiveMiss += 1
        if word in negativeWordsCounter:
            nWeight = math.log(float(negativeWordsCounter.get(word) + 1)
                                         / float(len(negativeWords) + len(negativeWordsCounter.keys())))
        else:
            nWeight = math.log(1/float(len(negativeWords) + len(negativeWordsCounter.keys())))
            negativeMiss += 1
        # print(word,pWeight,nWeight)
        positiveWeight += pWeight
        negativeWeight += nWeight
    print(line)
    print(positiveWeight,negativeWeight)
    print(positiveMiss,negativeMiss)
    print({True: 'Positive', False: 'Negative'}[positiveWeight>negativeWeight])
    result.write("{0} {1}\n".format({True: '1', False: '0'}[positiveWeight>negativeWeight],line))
result.close()
import math
import collections
import porter
import re
import random
ps = porter.PorterStemmer()


def stem(lines):
    result = []
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", lines)
    for sentence in sentences:
        ws = sentence.split()
        for w in ws:
            stemmed = ps.stem(w, 0, len(w)-1)
            result.append(stemmed)
    return result

testLineNos = []
testSentences = []
while len(testLineNos) < 16:
    rand = random.randint(1,214)
    if rand not in testLineNos:
        testLineNos.append(rand)
i = 1
trueReviewWordCount = 0
trueReviewWords =[ ]
file = open('hotelT-train.txt', 'r', encoding="utf8")
for line in file:
    if i in testLineNos:
        testSentences.append("5 " + " ".join(line.lower().split()[1:]))
    else:
        trueReviewWords.extend(set(stem(" ".join(line.lower().split()[1:]))))
    i += 1
trueReviewWordsCounter = collections.Counter(trueReviewWords)
i = 1
falseReviewWordCount = 0
falseReviewWords =[ ]
file = open('hotelF-train.txt', 'r', encoding="utf8")
for line in file:
    if i in testLineNos:
        testSentences.append("2 " + " ".join(line.lower().split()[1:]))
    else:
    	falseReviewWords.extend(set(stem(" ".join(line.lower().split()[1:]))))
    i += 1
falseReviewWordsCounter = collections.Counter(falseReviewWords)

# file = open('test1[Random Sample].txt', 'r')
# file = open('test.txt', 'r', encoding="utf8")
# result = open('result.txt', 'a')
tp = tn = fp = fn = 0
for line in testSentences:
    trueReviewWeight = falseReviewWeight = 0
    trueReviewMiss = falseReviewMiss = 0
    words = line.lower().split()
    x = int(words[0])
    sent = " ".join(words[1:])
    words = set(stem(sent))
    for word in words:
        if word in trueReviewWordsCounter:
            tWeight = math.log10((trueReviewWordsCounter.get(word) + 1)
                                         / (len(trueReviewWords) + len(trueReviewWordsCounter.keys())))
        else:
            tWeight = math.log10(1/(len(trueReviewWords) + len(trueReviewWordsCounter.keys())))
            trueReviewMiss += 1
        if word in falseReviewWordsCounter:
            fWeight = math.log10((falseReviewWordsCounter.get(word) + 1)
                                         / (len(falseReviewWords) + len(falseReviewWordsCounter.keys())))
        else:
            fWeight = math.log10(1/(len(falseReviewWords) + len(falseReviewWordsCounter.keys())))
            falseReviewMiss += 1
        # print(word,pWeight,nWeight)
        trueReviewWeight += tWeight
        falseReviewWeight += fWeight
    print(line)
    print(trueReviewWeight,falseReviewWeight)
    print(trueReviewMiss,falseReviewMiss)
    print({True: 'True', False: 'False'}[trueReviewWeight>falseReviewWeight])
    if trueReviewWeight>falseReviewWeight and x > 3:
        tp += 1
    elif trueReviewWeight>falseReviewWeight and x < 3:
        fp += 1
    elif trueReviewWeight<falseReviewWeight and x > 3:
        fn += 1
    elif trueReviewWeight<falseReviewWeight and x < 3:
        tn += 1
print (tp, fp, fn, tn)
precision = tp/(tp+fp)
recall = tp/(tp+fn)
accuracy = (tp+tn)/(tp+fp+tn+fn)
fMeasure = (2 * precision * recall)/(precision+recall)
print("Precision",precision)
print("Recall",recall)
print("Accuracy",accuracy)
print("fMeasure",fMeasure)

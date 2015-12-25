import math
import collections
import porter
import re
import random
ps = porter.PorterStemmer()


def stem(lines,sentiment):
    result = []
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", lines)
    for sentence in sentences:
        ws = sentence.split()
        for w in ws:
            stemmed = ps.stem(w, 0, len(w)-1)
            result.append(str(sentiment) + stemmed)
    return result

testLineNos = []
testSentences = []
while len(testLineNos) < 15:
    rand = random.randint(1,214)
    if rand not in testLineNos:
        testLineNos.append(rand)
i = 1
trueReviewWordCount = 0
trueReviewWords =[ ]
positiveTrueReviews = 0
negativeTrueReviews = 0
f = open('hotelT-train-sentiment.txt', 'r')
for line in f:
    if i in testLineNos:
        testSentences.append("1 " + " ".join(line.lower().split()))
    else:
        words = line.lower().split()
        sentiment = int(words[0])
        if(sentiment == 1):
            positiveTrueReviews += 1
        else:
            negativeTrueReviews += 1
        trueReviewWords.extend((stem(" ".join(words[1:]),sentiment)))
    i += 1

i = 1
falseReviewWordCount = 0
falseReviewWords =[ ]
positiveFalseReviews = 0
negativeFalseReviews = 0
f = open('hotelF-train-sentiment.txt', 'r')
for line in f:
    if i in testLineNos:
        testSentences.append("0 " + " ".join(line.lower().split()))
    else:
        words = line.lower().split()
        sentiment = int(words[0])
        if(sentiment == 1):
            positiveFalseReviews += 1
        else:
            negativeFalseReviews += 1
        falseReviewWords.extend((stem(" ".join(words[1:]),sentiment)))
    i += 1
trueReviewWordsCounter = collections.Counter(trueReviewWords)
falseReviewWordsCounter = collections.Counter(falseReviewWords)
f = open('hotelDeceptionTestSentiment.txt', 'r')
# file = open('test.txt', 'r', encoding="utf8")
result = open('result3.csv', 'a')
tWeight = fWeight = 0
tp = tn = fp = fn = 0
for line in f:
    trueReviewWeight = falseReviewWeight = 0.0
    words = line.lower().split()
    if(len(words) == 0):
        continue
    trueReview = int(words[0])
    sentiment = int(words[1]) 
    words = stem(" ".join(words[2:]),sentiment)
    for word in words:
        if word in trueReviewWordsCounter:
            tWeight = math.log((float(trueReviewWordsCounter.get(word) + 1)
                                         / float(len(trueReviewWords) + len(trueReviewWordsCounter.keys()))))
        else:
            tWeight = math.log(float(1)/float(len(trueReviewWords) + len(trueReviewWordsCounter.keys())))
        if word in falseReviewWordsCounter:
            fWeight = math.log(float(falseReviewWordsCounter.get(word) + 1)
                                         / float(len(falseReviewWords) + len(falseReviewWordsCounter.keys())))
        else:
            fWeight = math.log(float(1)/float(len(falseReviewWords) + len(falseReviewWordsCounter.keys())))
        trueReviewWeight += tWeight
        falseReviewWeight += fWeight
    print(line)
    print(trueReviewWeight,falseReviewWeight)
    print({True: 'True', False: 'False'}[trueReviewWeight>falseReviewWeight])
    if trueReviewWeight>falseReviewWeight and trueReview == 1:
        tp += 1
    elif trueReviewWeight>falseReviewWeight and trueReview == 0:
        fp += 1
    elif trueReviewWeight<falseReviewWeight and trueReview == 1:
        fn += 1
    elif trueReviewWeight<falseReviewWeight and trueReview == 0:
        tn += 1
print (tp, fp, fn, tn)
print (tp+tn,fp+fn)
precision = float(tp)/float(tp+fp)
recall = float(tp)/float(tp+fn)
accuracy = float(tp+tn)/float(tp+fp+tn+fn)
fMeasure = float(2 * precision * recall)/float(precision+recall)
print("Precision",precision)
print("Recall",recall)
print("Accuracy",accuracy)
print("fMeasure",fMeasure)
result.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}\n'.format(tp,tn,fp,fn,precision,recall,accuracy,fMeasure))
result.close()
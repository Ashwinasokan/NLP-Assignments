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

trueReviewWordCount = 0
trueReviewWords =[ ]
positiveTrueReviews = 0
negativeTrueReviews = 0
f = open('hotelT-train-sentiment.txt', 'r')
for line in f:
    words = line.lower().split()
    sentiment = int(words[0])
    if(sentiment == 1):
        positiveTrueReviews += 1
    else:
        negativeTrueReviews += 1
    trueReviewWords.extend((stem(" ".join(words[1:]),sentiment)))
falseReviewWordCount = 0
falseReviewWords =[ ]
positiveFalseReviews = 0
negativeFalseReviews = 0
f = open('hotelF-train-sentiment.txt', 'r')
for line in f:
    words = line.lower().split()
    sentiment = int(words[0])
    if(sentiment == 1):
        positiveFalseReviews += 1
    else:
        negativeFalseReviews += 1
    falseReviewWords.extend((stem(" ".join(words[1:]),sentiment)))
trueReviewWordsCounter = collections.Counter(trueReviewWords)
falseReviewWordsCounter = collections.Counter(falseReviewWords)
f = open('hotelDeceptionTestSentiment.txt', 'r')
# file = open('test.txt', 'r', encoding="utf8")
result = open('result4.txt', 'a')
tWeight = fWeigh = 0
for line in f:
    trueReviewWeight = falseReviewWeight = 0.0
    words = line.lower().split()
    if(len(words) == 0):
        continue
    sentiment = int(words[0]) 
    reviewId = line.split()[1] 
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
    result.write('{0}\t{1}\n'.format(reviewId,{True: 'T', False: 'F'}[trueReviewWeight>falseReviewWeight]))
result.close()
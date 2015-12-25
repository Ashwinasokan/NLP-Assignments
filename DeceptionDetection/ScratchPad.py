import porter
import re
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

trueReviewWords =[ ]
falseReviewWords =[ ]
T = open('hotelT-train.txt', 'r')
F = f = open('hotelF-train.txt', 'r')
t = 0
f = 0 
for line in T:
        trueReviewWords.extend((stem(" ".join(line.lower().split()[1:]))))
        t += 1
for line in F:
        falseReviewWords.extend((stem(" ".join(line.lower().split()[1:]))))
        f += 1
print (len(trueReviewWords)/t)
print (len(falseReviewWords)/f)
print (len(set(trueReviewWords))/t)
print (len(set(falseReviewWords))/f)

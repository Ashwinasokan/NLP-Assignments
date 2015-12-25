import random
import collections
bigramMatrix = collections.Counter()
trigramMatrix = collections.Counter()
emissionMatrix = collections.Counter()
tags = collections.Counter()
words = collections.Counter()
uniqueWords = collections.Counter()
testLineNos = []
testSentences = []
while len(testLineNos) < 25:
    rand = random.randint(1,13000)
    if rand not in testLineNos:
        testLineNos.append(rand)
i = 1
f = open('gene.train.smooth2.txt', 'r')
for currentLine in f:
    currentLine = currentLine.split()
    if i in testLineNos:
        testSentences.append(" ".join(currentLine))
        if currentLine[0] == "<post>":
            i += 1
        continue
    if currentLine[0] == "<pre>":
        # Count unigrams
        tags[currentLine[1]] += 1
        words[currentLine[0]] += 1
        previousLine = currentLine
    elif currentLine[0] == "<start>":
        # Count unigrams
        tags[currentLine[1]] += 1
        words[currentLine[0]] += 1
        # Count bigrams
        bigramMatrix[previousLine[1] + " " + currentLine[1]] += 1
        if(emissionMatrix[currentLine[0] + " " + currentLine[1]] == 0):
            uniqueWords[currentLine[1]] += 1
        emissionMatrix[currentLine[0] + " " + currentLine[1]] += 1
        oldLine = previousLine
        previousLine = currentLine
    else:
        # Count unigrams
        tags[currentLine[1]] += 1
        words[currentLine[0]] += 1
        # Count bigrams
        bigramMatrix[previousLine[1] + " " + currentLine[1]] += 1
        if(emissionMatrix[currentLine[0] + " " + currentLine[1]] == 0):
            uniqueWords[currentLine[1]] += 1
        emissionMatrix[currentLine[0] + " " + currentLine[1]] += 1
        # Count trigrams
        trigramMatrix[oldLine[1] + " " + previousLine[1] + " " + currentLine[1]] += 1
        oldLine = previousLine
        previousLine = currentLine
    if currentLine[0] == "<post>":
        i += 1
uniGramWeight = 0.0
biGramWeight = 0.0
triGramWeight = 0.0
for trigramKey in trigramMatrix.keys():
    (t1,t2,t3) = trigramKey.split()
    triGramW = float(trigramMatrix[ t1 + " " + t2 + " " + t3 ] - 1)/float(bigramMatrix[ t1 + " " + t2 ] - 1)
    biGramW = float(bigramMatrix[ t2 + " " + t3 ] - 1)/float(tags[t2] - 1)
    unigramW = float(tags[t3] - 1)/float(sum(tags.values()) - 1)
    if(max(triGramW,biGramW,unigramW) == triGramW):
        triGramWeight += trigramMatrix[ t1 + " " + t2 + " " + t3 ]
    elif(max(triGramW,biGramW,unigramW) == biGramW):
        biGramWeight += trigramMatrix[ t1 + " " + t2 + " " + t3 ]
    else:
        uniGramWeight += trigramMatrix[ t1 + " " + t2 + " " + t3 ]
totalWeight = uniGramWeight + biGramWeight + triGramWeight
triGramWeight = triGramWeight/totalWeight
biGramWeight = biGramWeight/totalWeight
uniGramWeight = uniGramWeight/totalWeight
def getTransmissionPB(t1,t2,t3):
    uni = float(uniGramWeight) * float(tags[t3])/float(sum(tags.values()))
    bi = float(biGramWeight) * float(bigramMatrix[t2 + " " + t3])/float(tags[t2])
    if t1 + " " + t2 in bigramMatrix:
        tri = float(triGramWeight) * float(trigramMatrix[ t1 + " " + t2 + " " + t3 ])/float(bigramMatrix[t1 + " " + t2])
    else:
        tri = 0
    return (uni + bi + tri)
def getBigramTransmissionPB(t1,t2):
    return (float(bigramMatrix[t1 + " " + t2] + 1)/float(tags[t1] + len(tags.keys())))
def getEmissionPB(w,t):
    if w in words:
        return (float(emissionMatrix[w + " " + t])/float(tags[t]))
    else:
        return (float(uniqueWords[t])/float(sum(uniqueWords.values())))
viterbiMatrix = collections.OrderedDict()
backpointer = collections.OrderedDict()
i = 0
sentence = []
gold = []
answers = []
goldOutput = open('gold.txt', 'w')
result = open('result.txt', 'w')
for currentLine in testSentences:
    currentLine = currentLine.split()
    if currentLine[0] == "<pre>":
        previousLine = currentLine
        continue
    elif currentLine[0] == "<start>":
        for previous in tags.keys():
            for tag in tags.keys():
                if previous == previousLine[0] and tag == currentLine[0]:
                    viterbiMatrix[str(i)+ " " + previous + " " + tag] = 1
                else:
                    viterbiMatrix[str(i)+ " " + previous + " " + tag] = 0
        oldLine = previousLine
        previousLine = currentLine
        i += 1
        continue
    elif currentLine[0] == "<stop>":
        k = i-1
        answers = [""] * k
        maxi = float('-inf')
        for previous in tags.keys():
            for tag in tags.keys():
                value = float(viterbiMatrix[str(k)+ " "+ previous + " " + tag]) * float(getTransmissionPB(previous,tag,currentLine[1]))
                if(maxi < value):
                        maxi = value
                        (answers[k-2],answers[k-1]) = (previous,tag)
        k -= 2
        while k > 0:
            answers[k-1] = backpointer[str(k+2) + " " + answers[k] + " " + answers[k+1]]
            k -= 1
        i=0
        while i< len(sentence):
            goldOutput.write(sentence[i] + "\t" + gold[i] + "\n");
            result.write(sentence[i] + "\t" + answers[i] + "\n");
            i += 1
    elif currentLine[0] == "<post>":
        sentence = []
        gold = []
        answers = []
        viterbiMatrix.clear()
        backpointer.clear()
        i = 0
    else:
        sentence.append(currentLine[0])
        gold.append(currentLine[1])
        for previous in tags.keys():
            for tag in tags.keys():
                maxi = float('-inf')
                for old in tags.keys():
                    value = float(viterbiMatrix[str(i-1)+ " "+ old + " " + previous]) * float(getTransmissionPB(old,previous,tag)) * float(getEmissionPB(currentLine[0],tag))
                    if(maxi < value):
                        maxi = value
                        backpointer[str(i) + " " + previous + " " + tag] = old
                        viterbiMatrix[str(i)+ " "+ previous + " " + tag] = value
        oldLine = previousLine
        previousLine = currentLine
        i += 1
goldOutput.close()
result.close()
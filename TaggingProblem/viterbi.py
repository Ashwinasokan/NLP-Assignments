import random
import collections
transmissionMatrix = collections.Counter()
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
f = open('gene.train.smooth.txt', 'r')
for currentLine in f:
    currentLine = currentLine.split()
    if i in testLineNos:
        testSentences.append(" ".join(currentLine))
        if currentLine[0] == "<stop>":
            i += 1
        continue
    if currentLine[0] == "<start>":
        tags[currentLine[1]] += 1
        words[currentLine[0]] += 1
        previousLine = currentLine
        continue
    transmissionMatrix[previousLine[1] + " " + currentLine[1]] += 1
    if(emissionMatrix[currentLine[0] + " " + currentLine[1]] == 0):
        uniqueWords[currentLine[1]] += 1
    emissionMatrix[currentLine[0] + " " + currentLine[1]] += 1
    tags[currentLine[1]] += 1
    words[currentLine[0]] += 1
    if currentLine[0] == "<stop>":
        i += 1
        previousLine = ["<start>","<start>"]
    else:
        previousLine = currentLine
def getTransmissionPB(t1,t2):
    return (float(transmissionMatrix[t1 + " " + t2] + 1)/float(tags[t1] + len(tags.keys())))
def getEmissionPB(w,t):
    if w in words:
        return (float(emissionMatrix[w + " " + t])/float(tags[t]))
    else:
        return (float(uniqueWords[t])/float(sum(uniqueWords.values())))
viterbiMatrix = collections.OrderedDict()
backpointer = collections.OrderedDict()
i = 0
gold = []
goldOutput = open('gold.txt', 'w')
result = open('result.txt', 'w')
previousLine = testSentences[0].split()
for currentLine in testSentences[1:]:
    gold.append(currentLine)
    currentLine = currentLine.split()
    if currentLine[0] == "<start>":
        previousLine = currentLine
        i += 1
        continue
    if previousLine[0] == "<start>":
        for tag in tags.keys():
            viterbiMatrix[str(i)+ " " + currentLine[0] + " " + tag] = float(getTransmissionPB(previousLine[1],tag)) * float(getEmissionPB(currentLine[0],tag))
            backpointer[str(i)+ " " + currentLine[0] + " " + tag] = previousLine[1]
        previousLine = currentLine
        i += 1
        continue
    for tag in tags.keys():
        maxi = float('-inf')
        for previous in tags.keys():
            value = (float(viterbiMatrix[str(i-1)+ " " + previousLine[0] + " " + previous]) * float(getTransmissionPB(previous,tag)))
            if(maxi < value):
                maxi = value
                backpointer[str(i) + " " + currentLine[0] + " " + tag] = previous
        viterbiMatrix[str(i) + " " + currentLine[0] + " " + tag] = maxi * getEmissionPB(currentLine[0],tag)
    if currentLine[0] == "<stop>":
        line = gold[-1].split()
        answer = backpointer[str(i) + " " + line[0] + " " + "<stop>"]
        i -= 1
        for line in reversed(gold[1:-1]):
            line = line.split()
            goldOutput.write(line[0] + "\t" + line[1] + "\n");
            result.write(line[0] + "\t" + answer + "\n");
            print (line[0],line[1],answer)
            answer = backpointer[str(i) + " " + line[0] + " " + answer]
            i -= 1
        gold = []
        viterbiMatrix.clear()
        backpointer.clear()
        previousLine = ["<start>","<start>"]
    else:
        previousLine = currentLine
    i += 1
goldOutput.close()
result.close()
#!/usr/bin/python

# call from unix shell as
# eval.py goldstandardfile.txt yoursystemoutput.txt
#

import sys

def eval(keys, predictions,result):
    """ Given a stream of gold standard word/tag pairs and a stream of system pairs. Figure out the the recall, precision and F1 """


    goldStandardEntities = findEntities(taggedData(keys))     # get the entities in the gold standard
    systemEntities = findEntities(taggedData(predictions))    # and the entities in the system output

    numEntities = len(goldStandardEntities)                   # number of entities there should be
    numReturned = len(systemEntities)                         # number actually tagged by system
    numTruePositives = len(set.intersection(goldStandardEntities,systemEntities))    # number of those that were right

    precision = float(numTruePositives)/numReturned
    recall = float(numTruePositives)/numEntities
    f1 = 2 * (precision * recall)/(precision + recall)

    print numEntities, " entities in gold standard."
    print numReturned, " total entities found."
    print numTruePositives, " of which were correct."
    
    print "Precision: ", precision, "Recall: ", recall, "F1-measure: ", f1
    result.write('{0}, {1}, {2}, {3}, {4}, {5}\n'.format(numEntities,numReturned,numTruePositives,precision,recall,f1))

def findEntities(data):
    """ Find all the IOB delimited entities in the data.  Return as a set of (begin, end) tuples. Data is sequence of word, tag pairs. """

    entities = set()

    entityStart = 0
    entityEnd = 0
    
    currentState = "Q0"
    count = 0
    
    for word, tag in data:
        count = count + 1
        if currentState == "Q0":
            if tag == 'B':
                currentState = "Q1"
                entityStart = count
        elif currentState == "Q1":
            if tag == "B":
                entityEnd = count - 1
                entities.add((entityStart, entityEnd))
                entityStart = count
            if tag == "O":
                entityEnd = count - 1
                entities.add((entityStart, entityEnd))
                currentState = "Q0"

    if currentState == "Q1":
        entities.add((entityStart, entityEnd))

    return entities

def taggedData(file):
    for line in file:
        if line == '\n':
            yield(['</s>', 'O'])
        else:
            yield line.strip().split()

if __name__ == "__main__":
      keys = open(sys.argv[1], 'rU')
      predictions = open(sys.argv[2], 'rU')
      output = open(sys.argv[3], 'a')
      eval(keys, predictions,output)

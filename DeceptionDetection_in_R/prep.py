import random
testLineNos = []
testSentences = []
while len(testLineNos) < 16:
    rand = random.randint(1,214)
    if rand not in testLineNos:
        testLineNos.append(rand)
train = open('hotel-train.csv', 'w')
test = open('hotel-test.csv', 'w')
train.write("Deceptive|Text|\n");
test.write("Deceptive|Text|\n");
i = 1
file = open('hotelT-train.txt', 'r')
for line in file:
    if i in testLineNos:
        test.write("0|" + " ".join(line.lower().split()[1:]) + "|\n")
    else:
        train.write("0|" + " ".join(line.lower().split()[1:]) + "|\n")
    i += 1
i = 1
file = open('hotelF-train.txt', 'r')
for line in file:
    if i in testLineNos:
        test.write("1|" + " ".join(line.lower().split()[1:]) + "|\n")
    else:
    	train.write("1|" + " ".join(line.lower().split()[1:]) + "|\n")
    i += 1
train.close()
test.close()

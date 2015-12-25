# Load the data from the csv file
dataDirectory <- "/home/ashwin/Documents/Practice/DeceptionDetection/" # put your own folder here
data <- read.csv(paste(dataDirectory, 'hotel-train.csv', sep=""), header = TRUE, sep="|")
# Create the document term matrix
dtMatrix <- create_matrix(data["Text"])
# Configure the training data
container <- create_container(dtMatrix, data$Deceptive, trainSize=1:397, virgin=FALSE)
# train a SVM Model
model <- train_model(container, "SVM", kernel="linear", cost=1)
# new data
testData <- read.csv(paste(dataDirectory, 'hotel-test.csv', sep=""), header = TRUE, sep = "|")
predictionData <- testData$Text
# create a prediction document term matrix
predMatrix <- create_matrix(predictionData, originalMatrix=dtMatrix)
# create the corresponding container
predSize = length(predictionData);
predictionContainer <- create_container(predMatrix, labels=rep(0,predSize), testSize=1:predSize, virgin=FALSE)
# predict
results <- classify_model(predictionContainer, model)
results$Deceptive <- testData$Deceptive
predict <- list(results$SVM_LABEL)
true <- list(testData$Deceptive)
retrieved <- sum(predict)
precision <- sum(predict & true) / retrieved
recall <- sum(predict & true) / sum(true)
Fmeasure <- 2 * precision * recall / (precision + recall)
results
retrieved
precision
recall
Fmeasure
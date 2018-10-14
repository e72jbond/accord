#!/usr/bin/python

from os import listdir
from os.path import isfile, join

from sklearn import svm

ddir = '/home/agreig/Documents/git_repos/accord/data/test'

files = [f for f in listdir(ddir) if isfile(join(ddir, f))]

files.sort()

#print files

cows = {}
for f in files:
    fh = open("{0}/{1}".format(ddir, f))
    for line in fh:
        lineList = line.split(',')
        name = lineList[0]
        price = lineList[5]
        if name in cows:
            cows[name].append(price)
        else:
            cows[name] = [price]
    fh.close()

maxPoints = 0
for cow in cows:
    points = len(cows[cow])
    #print "{0}: {1}".format(cow, points)
    if points > maxPoints:
        maxPoints = points

#print "Max: {0}".format(maxPoints)

# filter out missing points
rangeCows = {}
numCows = 0
for cow in cows:
    points = len(cows[cow])
    if points == maxPoints:
        rangeCows[cow] = cows[cow]
        numCows += 1

#print "Range Total: {0}".format(numCows) 

# filter 1st point < $1
valueCows = {}
numCows = 0
for cow in rangeCows:
    #print "Point: {0}".format(rangeCows[cow][0])
    if float(rangeCows[cow][0]) >= 1.0:
        valueCows[cow] = rangeCows[cow]
        numCows += 1

#print "Value Total: {0}".format(numCows) 

trainCows = 274
#trainCows = 10
trainPoints = 126

cowArray = []
for cow in valueCows:
    cowArray.append(cow)

cowArray.sort()
#print "SORT: {0}".format(cowArray)
cowClassifications = []
cowClassificationsTest = []
cowData = []
cowTest = []

trainCount = 0
for cow in cowArray:
    if trainCount < trainCows:
        cowData.append(cows[cow][0:trainPoints])

        if cows[cow][-1] > cows[cow][trainPoints]:
            cowClassifications.append(1) #increase
        else:
            cowClassifications.append(0) #decrease
    else:
        cowTest.append(cow)

        if cows[cow][-1] > cows[cow][trainPoints]:
            cowClassificationsTest.append(1) #increase
        else:
            cowClassificationsTest.append(0) #decrease

    trainCount += 1

#cowCount = 0
#for cow in cowArray:
#    if cowCount == trainCows:
#        break
#
#    print "COW: {0}".format(cow)
#    print "CLASS: {0}".format(cowClassifications[cowCount])
#    print "END VALUE: {0}".format(cows[cow][-1])
#    print "DATA: {0}".format(cowData[cowCount])
#
#    cowCount += 1

#clf = svm.SVC(gamma='auto')
#kernels = ['rbf', 'linear', 'poly', 'sigmoid']

kernel = 'rbf'

#gammaVal = (1 / float(trainPoints)) - 0.005
gammaVal = 0.0001
gammaValMax = (1 / float(trainPoints)) + 0.5
while gammaVal < gammaValMax:
    #print "KERNEL {0}, GAMMA: {1}".format(kernel, gammaVal)
    clf = svm.SVC(kernel=kernel, gamma=gammaVal)
    
    clf.fit(cowData, cowClassifications)
    
    predictArray = []
    for cow in cowTest:
        predictArray.append(cows[cow][0:trainPoints])
    
    predictions = clf.predict(predictArray)
    #print "PRED: {0}".format(predictions)
    
    predCount = 0
    correctCount = 0
    incPredCount = 0
    incCorrectCount = 0
    for cow in cowTest:
        #print "COW: {0}: {1}, actual: {2}".format(cow, predictions[predCount], cowClassificationsTest[predCount])
    
        if predictions[predCount] == cowClassificationsTest[predCount]:
            correctCount += 1
    
            if predictions[predCount] == 1:
                incCorrectCount += 1
    
        if predictions[predCount] == 1:
            incPredCount += 1
    
        predCount += 1
    
    correctPerc = float(correctCount) / float(predCount)
    #print "{0}% overall correct from {1}".format(correctPerc * float(100), predCount)
    
    incCorrectPerc = float(incCorrectCount) / float(incPredCount)
    #print "{0}% increase correct from {1}".format(incCorrectPerc * float(100), incPredCount)

    print "K:{0},GAMMA:{1},T:{2},TC:{3},I:{4},IC:{5}".format(kernel, gammaVal, predCount, correctPerc * float(100), incPredCount, incCorrectPerc * float(100))

    gammaVal += 0.0001

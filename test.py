#!/usr/bin/python

from os import listdir
from os.path import isfile, join

from sklearn import svm

ddir = '/home/agreig/Documents/git_repos/accord/data/test'

files = [f for f in listdir(ddir) if isfile(join(ddir, f))]

files.sort()

print files

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
    print "{0}: {1}".format(cow, points)
    if points > maxPoints:
        maxPoints = points

print "Max: {0}".format(maxPoints)

# filter out missing points
rangeCows = {}
numCows = 0
for cow in cows:
    points = len(cows[cow])
    if points == maxPoints:
        rangeCows[cow] = cows[cow]
        numCows += 1

print "Range Total: {0}".format(numCows) 

# filter 1st point < $1
valueCows = {}
numCows = 0
for cow in rangeCows:
    #print "Point: {0}".format(rangeCows[cow][0])
    if float(rangeCows[cow][0]) >= 1.0:
        valueCows[cow] = rangeCows[cow]
        numCows += 1

print "Value Total: {0}".format(numCows) 

trainPoints = 126



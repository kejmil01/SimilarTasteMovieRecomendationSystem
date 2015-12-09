# -*- coding: utf-8 -*-

import numpy as np

def splitDataset(udata_array, test_factor):
    udataArrayLenght = len(udata_array)
    testCount = int(test_factor * udataArrayLenght)
    
    arrays = np.split(udata_array, [testCount, udataArrayLenght])
    testArray = arrays[0]
    trainingArray = arrays[1]
    
    return trainingArray, testArray

def saveDataSet(array, name):
    file_ = open(name, 'w')
    
    lenght = len(array)
    
    for i in range(len(array)):
        if(i < lenght - 1):
            file_.write("%s %s %s %s\n" % (array[i, 0], array[i, 1], array[i, 2], array[i, 3]))
        elif(i < lenght):
            file_.write("%s %s %s %s" % (array[i, 0], array[i, 1], array[i, 2], array[i, 3]))
    
    file_.close()
    

def mainFuction(udataArray, testFactorList):
    for i in range(len(testFactorList)):
        testFactor = testFactorList[i]
        trainingArray, testArray = splitDataset(udataArray, testFactor)

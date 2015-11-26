# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import time

import common
import randomRS
import averageRatingRS

CORELATION_1 = 1
CORELATION_2 = 2
CORELATION_3 = 3

MIN_CORELATION_FACTOR1 = 0.7
MIN_CORELATION_FACTOR2 = 0.76
MIN_CORELATION_FACTOR3 = 0.82
MIN_TASTE_SIMILAR_USERS = 5
MIN_TASTE_SIMILAR_USER1 = 10
MIN_MOVIES_TO_TEST = 3

class TasteUserTrainingModel:
    def __init__(self, ratings, corelationType):
        self.ratings = ratings;
        self.corelationType = corelationType;
        
class SimilarTasteUsersModel:
    def __init__(self):
        self.usersCorelation1 = {};
        self.usersCorelation2 = {};
        self.usersCorelation3 = {};
    
def groupData(udata_array):
    usersDict = {}
    
    for i in range(len(udata_array)):
        userId = udata_array[i, 0].item()
        movieId = udata_array[i, 1].item()
        rating = udata_array[i, 2].item()
        
        userRatingsList = usersDict.get(userId)
        if(userRatingsList == None):
            userRatingsList = []
            usersDict[userId] = userRatingsList
        userRatingsList.append([movieId, rating])
        
    return usersDict
    
def generateSameMoviesRatingList(otherUserRatingList, userRatingList):
    firstList = []
    secondList = []
    
    da = dict(userRatingList)
    db = dict(otherUserRatingList)
      
    for k in set(da.keys()).intersection(db.keys()):
        firstList.append(da[k])
        secondList.append(db[k])   
            
    return firstList, secondList
    
def getQuantizedList(mList):
    qList = []
    for i in range(len(mList)):
        qList.append(common.getQuantizedRating(mList[i]))
    return qList
    
def getCorrelationFactor(list1, list2):
    qList1 = getQuantizedList(list1)
    qList2 = getQuantizedList(list2)
    
    count = len(qList1)
    summ = 0
    for i in range(len(qList1)):
        if(qList1[i] == qList2[i]):
            summ += 1
    factor = float(summ/count)
    return factor
    
def containsMovie(ratings, movieId):
    contains = False
    for iterator in range(len(ratings)):
        if(ratings[iterator][0] == movieId):
            contains = True
            break
    return contains
    
def setupDict(corelationTypeDict, ratings):
    for i in range(len(ratings)):
        ratingList = corelationTypeDict.get(ratings[i][0])
        if(ratingList == None):
            ratingList = []
            corelationTypeDict[ratings[i][0]] = ratingList
        ratingList.append(ratings[i][1])

def getTasteSimilarUsers(groupedBaseData, userRatingList, movieId, userId):
    usersToReturn = SimilarTasteUsersModel()
    for k, v in groupedBaseData.items():
        if(k != userId):
            fList, sList = generateSameMoviesRatingList(v, userRatingList)
            if(len(fList) >= MIN_MOVIES_TO_TEST):
                factor = getCorrelationFactor(fList, sList)
                if(factor >= MIN_CORELATION_FACTOR3):
                    setupDict(usersToReturn.usersCorelation3, v)
                elif (factor >= MIN_CORELATION_FACTOR2):
                    setupDict(usersToReturn.usersCorelation2, v)
                elif (factor >= MIN_CORELATION_FACTOR1):
                    setupDict(usersToReturn.usersCorelation1, v)
        
    return usersToReturn
    
def getBestFitSimilarUsersDictionary(ratingsCorelation3, ratingsCorelation2, ratingsCorelation1):        
    bestUsersRatings = []
    
    bestUsersRatings.extend(ratingsCorelation3)
    if(len(bestUsersRatings) < MIN_TASTE_SIMILAR_USERS):
        bestUsersRatings.extend(ratingsCorelation3)
        bestUsersRatings.extend(ratingsCorelation2)
        if(len(bestUsersRatings) < MIN_TASTE_SIMILAR_USERS):
            bestUsersRatings.extend(ratingsCorelation3)
            bestUsersRatings.extend(ratingsCorelation2)
            bestUsersRatings.extend(ratingsCorelation1)
    
    return bestUsersRatings
    
def getNormalizedAveragedRatingFromSimilarTaste(ratingsCorelation3, ratingsCorelation2, ratingsCorelation1, rating):
    bestUsersRatings = getBestFitSimilarUsersDictionary(ratingsCorelation3, ratingsCorelation2, ratingsCorelation1)
    summ = 0
    count = len(bestUsersRatings)
    for i in range(count):
        summ += bestUsersRatings[i]        
     
    avgRating = float(summ)/float(count)
    return common.getQuantizedRating(avgRating)
    
def getNormalizedAvgRatingPotinFromSimilarTaste(ratingsCorelation3, ratingsCorelation2, ratingsCorelation1, rating):
    normalizedOtherRating = getNormalizedAveragedRatingFromSimilarTaste(ratingsCorelation3, ratingsCorelation2, ratingsCorelation1, rating)
    normalizedRating = common.getQuantizedRating(rating)
    #print(str(normalizedRating) + " " + str(normalizedOtherRating))
    if(normalizedOtherRating == normalizedRating):
        return 1
    else:
        return 0
    
def getTasteSimilarRSPrecisionRecall(base_udata_array, test_udata_array):
    userGroupedTrainingData = groupData(base_udata_array)
    
    precisionList = []
    recallList = []
    finalCount = len(test_udata_array)
    
    summ = 0
    count = 0
    
    summ1 = 0
    count1 = 0
    
    summ2 = 0
    count2 = 0
    
    arrayWithAverageRatings = averageRatingRS.getAverageMoviesRatings(base_udata_array)
    
    currentUser = -1
    similarTasteUsers = None

    for i in range(len(test_udata_array)):
        userId = test_udata_array[i][0]
        movieId = test_udata_array[i][1]
        rating = test_udata_array[i][2]
        userBaseRatings = userGroupedTrainingData.get(userId)
        
        print("count: " + str(count))
        
        if(userBaseRatings == None or len(userBaseRatings) < MIN_MOVIES_TO_TEST):
            f = averageRatingRS.getQuantizedAverageRecomendationPoint(arrayWithAverageRatings, rating, movieId)
            summ += f
            summ1 += f
            count1 += 1
        else:
            if(userId != currentUser):
                similarTasteUsers = getTasteSimilarUsers(userGroupedTrainingData, userBaseRatings, movieId, userId)
                currentUser = userId

            ratingsCorelation3 = []
            ratingsCorelation2 = []
            ratingsCorelation1 = []
            
            mRatings = similarTasteUsers.usersCorelation3.get(movieId)
            if(mRatings != None):
                ratingsCorelation3 = mRatings
            mRatings = similarTasteUsers.usersCorelation2.get(movieId)
            if(mRatings != None):
                ratingsCorelation2 = mRatings
            mRatings = similarTasteUsers.usersCorelation1.get(movieId)
            if(mRatings != None):
                ratingsCorelation1 = mRatings
            
            countC32 = len(ratingsCorelation3) + len(ratingsCorelation2)
            countC321 = countC32 + len(ratingsCorelation1)
            
            if(countC32 >= MIN_TASTE_SIMILAR_USERS or countC321 >= MIN_TASTE_SIMILAR_USER1):
                f = getNormalizedAvgRatingPotinFromSimilarTaste(ratingsCorelation3, ratingsCorelation2, ratingsCorelation1,  rating)
                summ += f
                summ2 += f
                count2 += 1
            else:
                f = averageRatingRS.getQuantizedAverageRecomendationPoint(arrayWithAverageRatings, rating, movieId)
                summ += f
                summ1 += f
                count1 += 1
        count += 1
        precisionList.append(summ/count)
        recallList.append(summ/finalCount)
        
            
    print("|||||||||||||||| SIM |||||||||||||||")
    print(summ2)
    print(count2)
    if(count2 != 0):
        print(summ2/count2)
    print("|||||||||||||||| AVG |||||||||||||||")
    print(summ1)
    print(count1)
    print(summ1/count1)
    print("|||||||||||||||| ALL |||||||||||||||")
    print(summ)
    print(count)
    print(summ/count)
    print("||||||||||||||||||||||||||||||||||||")
    return common.PrecisionRecallModel(precisionList, recallList)

def showChart(dataAxis, returnModel, name):
    plt.plot(dataAxis, returnModel.precision, 'r', dataAxis, returnModel.recall)
    plt.show()
    print(name + " " + str(returnModel.recall[len(returnModel.precision) - 1]))
    
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

test_udata_array = common.loadUdata('test.txt')
base_udata_array = common.loadUdata('base.txt')

data = np.arange(len(test_udata_array))

start = time.time()
similarModel = getTasteSimilarRSPrecisionRecall(base_udata_array, test_udata_array)
end = time.time()
print("time: " + str(end - start))

randomRecomendationSystemModel = randomRS.getRandomRSPrecisionRecall(test_udata_array)
averageBasedRecomendationSystemModel = averageRatingRS.getAverageRatingBasedRSPrecisionRecall(base_udata_array, test_udata_array)

showChart(data, randomRecomendationSystemModel, "random")
showChart(data, averageBasedRecomendationSystemModel, "average")
showChart(data, similarModel, "similar")
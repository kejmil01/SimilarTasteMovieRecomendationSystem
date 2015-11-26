# -*- coding: utf-8 -*-

import common
import numpy as np

MOVIE_COUNT = 1682

# returns one dimensional array with average movie rating where iterator = movieId, and value = avgMovieRating
def getAverageMoviesRatings(udata_array):
    
    #summ of ratings, rating count
    #iterator = movieId
    array = np.zeros(shape=(MOVIE_COUNT, 2), dtype = int)
    
    for i in range(len(udata_array)):
        movieId = udata_array[i, 1]
        rating = udata_array[i, 2]
        normalized_rating = common.getQuantizedRating(rating)

        array[movieId - 1, 1] += 1
        array[movieId - 1, 0] += normalized_rating
        
    arrayWithAverageRatings = np.zeros(shape=(MOVIE_COUNT, 1), dtype = int)
    for i in range(MOVIE_COUNT):
        ratingCount = array[i, 1]
        ratingSumm = array[i, 0]
        
        avg = 0.0
        if(ratingCount > 0):
            avg = float(ratingSumm)/ratingCount
        if(avg > 0.5):
            arrayWithAverageRatings[i] = 1
    return arrayWithAverageRatings
    
def getQuantizedAverageRecomendationPoint(arrayWithAverageRatings, user_rating, movieId):
    normalized_user_rating = common.getQuantizedRating(user_rating)
    if(normalized_user_rating == int(arrayWithAverageRatings[movieId - 1])):
        return 1
    else:
        return 0
    
def getAverageRatingBasedRSPrecisionRecall(base_udata_array, test_udata_array):
    arrayWithAverageRatings = getAverageMoviesRatings(base_udata_array)
    
    count = 0
    summ = 0
    
    finalCount = len(test_udata_array)
    
    precisionList = []
    recallList = []
    
    for row in test_udata_array:
        movieId = row[1]
        user_rating = row[2]
        
        count += 1
        summ += getQuantizedAverageRecomendationPoint(arrayWithAverageRatings, user_rating, movieId)
        
        precisionList.append(summ/count)
        recallList.append(summ/finalCount)
        
    return common.PrecisionRecallModel(precisionList, recallList)
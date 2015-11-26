# -*- coding: utf-8 -*-

import random
import common

#udata_array - two-dimensional (nd)array with [i][0]userId, [i][1]itemId, and [i][2]rating in row 
def getRandomRSPrecisionRecall(udata_array):
    count = 0
    summ = 0
    
    finalCount = len(udata_array)
    
    precisionList = []
    recallList = []
    
    for row in udata_array:
        user_rating = common.getQuantizedRating(row[2])
        system_rating = common.getQuantizedRating(random.randint(1, 5))
        
        count += 1
        if(user_rating == system_rating):
            summ += 1
        precisionList.append(summ/count)
        recallList.append(summ/finalCount)
    
    return common.PrecisionRecallModel(precisionList, recallList)
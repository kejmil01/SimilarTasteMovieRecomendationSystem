# -*- coding: utf-8 -*-

import os
import numpy as np

#script folder path
DIR_PATH = os.path.dirname(__file__)

class PrecisionRecallModel:
    def __init__(self, precision, recall):
        self.precision = precision;
        self.recall = recall;

# loads data from u.data structured file to a two-dimensional (nd)array
# {iterator: userId, movieId, rating}
def loadUdata(filename):
    with open(os.path.join(DIR_PATH, filename)) as file:
        array = np.ndarray(shape=(0, 3), dtype=int)
        count = 0
        for row in file.readlines():
        #sample row = 4	328	3	892001537
           count = count + 1
           array.resize((count, 3))           
           sourceLines = row.split()
           array[count - 1, 0] = int(sourceLines[0])
           array[count - 1, 1] = int(sourceLines[1])
           array[count - 1, 2] = int(sourceLines[2])
           
        return array
        
def getQuantizedRating(ratingValue):
    if(ratingValue > 3.0):
        return 1
    else:
        return 0
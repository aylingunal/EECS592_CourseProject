
''' this file is for general helper functions '''

import collections
import math

''' get cosine similarity between two texts '''
def compute_cosine_sim(vec1, vec2):
    # sentences to vectors
    vec1 = collections.Counter(vec1)
    vec2 = collections.Counter(vec2)
    # compute magnitudes of each vector
    mag1 = 0
    mag2 = 0
    for key in vec1.keys():
        mag1 += math.pow(vec1[key],2)
    for key in vec2.keys():
        mag2 += math.pow(vec2[key],2)
    mag1 = math.sqrt(mag1)
    mag2 = math.sqrt(mag2)
    # compute numerator
    numerator = 0
    for term in set(list(vec1.keys()) + list(vec2.keys())):
        numerator += vec1[key] * vec2[key]
    # check case for 0 in-common terms
    if mag1 * mag2 == 0:
        return 0

    return float(numerator / (mag1*mag2))
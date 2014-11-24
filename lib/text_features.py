from itertools import product

# http://stackoverflow.com/questions/18259128/r-k-skip-ngram-generalazation-of-for-loops
def kskipngrams(sentence,skip,ngram):
    if ngram == 0 or len(sentence) == 0:
        return None
    grams = []
    for i in range(len(sentence)-ngram+1):
        grams.extend(initial_kskipngrams(sentence[i:],skip,ngram))
    return grams

def initial_kskipngrams(sentence,skip,ngram):
    if ngram == 1:
        return [[sentence[0]]]
    grams = []
    for j in range(min(skip+1,len(sentence)-1)):
        kmjskipnm1grams = initial_kskipngrams(sentence[j+1:],skip-j,ngram-1)
        if kmjskipnm1grams is not None:
            for gram in kmjskipnm1grams:
                grams.append([sentence[0]]+gram)
    return grams
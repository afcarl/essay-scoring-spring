from essay_feature import EssayFeature

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
    
class EssaySkipgram(EssayFeature):
    def __init__(self,name,source,base,nskip,ngram,cumulative=False):
        self.name = name
        self.source = source
        self.base = base 
        self.nskip = nskip
        self.ngram = ngram
        self.cumulative = cumulative
        
    def generate(self,essay):
        features = {}
        text = essay.texts[self.source]
        skipgrams = kskipngrams(self.base(text), self.nskip, self.ngram)
        if skipgrams is not None and len(skipgrams) > 0:
            for skipgram in list(set(map(tuple,skipgrams))):
                feature_name = "%s_%s_%d_%d_%s" % (self.name,self.source,self.nskip,self.ngram,"_".join(skipgram))
                if not self.cumulative:
                    features[feature_name] = 1
                else:
                    try:
                        features[feature_name] += 1
                    except KeyError:
                        features[feature_name] = 1
        return features
        

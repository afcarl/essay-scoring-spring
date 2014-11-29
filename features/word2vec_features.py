import numpy as np

from essay_feature import EssayFeature

import gensim
word2vec_model = gensim.models.Word2Vec.load_word2vec_format("GoogleNews-vectors-negative300.bin.gz",binary=True)

class EssayWord2Vec(EssayFeature):
    def __init__(self,source):
        self.source = source
    
    def generate(self,essay):        
        text = essay.texts[self.source]
        vec = []
        for word in text.split():
            try:
                vec.append(word2vec_model[word.lower()])
            except KeyError:
                pass
        
        features = {}    
        if len(vec) > 0:        
            vec = np.vstack(vec).T.mean(axis=1)
            for n in range(len(vec)):
                features["word2vec_%d" % (n+1)] = vec[n]
    
        return features
        
class EssayWord2VecFirstWords(EssayFeature):
    def __init__(self,source,n_words):
        self.source = source
        self.n_words = n_words
    
    def generate(self,essay):        
        text = essay.texts[self.source]
        vec = []
        for word in text.split()[:self.n_words]:
            try:
                vec.append(word2vec_model[word.lower()])
            except KeyError:
                pass
    
        features = {}    
        if len(vec) > 0:        
            vec = np.hstack(vec)
            for n in range(len(vec)):
                features["word2vec_first_words_%d" % (n+1)] = vec[n]
        return features
        return features

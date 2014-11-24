import gensim
import pandas as pd
from sklearn.cluster import KMeans

#"/home/pawel/Downloads/GoogleNews-vectors-negative300.bin.gz"
from essay_feature import EssayTextConversionBatch

class EssayTextToW2VClusters(EssayTextConversionBatch):
    def __init__(self,source,dest,n_clusters,w2v_path):
        self.source = source
        self.dest = dest
        self.n_clusters = n_clusters
        self.w2v_path = w2v_path
        
    def fit(self,essays):
        word2vec_model = gensim.models.Word2Vec.load_word2vec_format(self.w2v_path,binary=True)        
        
        worddict = []
        for essay in essays:
            text = essay.texts[self.source]
            for word in text.split():
                word = word.lower()
                worddict.append(word)
        worddict = list(set(worddict))
        
        wordvectors = {}
        for word in worddict:
            if word in word2vec_model:
                wordvectors[word] = word2vec_model[word]
        
        n_clusters = self.n_clusters(len(wordvectors))
        wordvectors_df = pd.DataFrame(wordvectors).T
            
        # kmeans
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(wordvectors_df)    
        clusters = kmeans.predict(wordvectors_df)
        
        #for n in range(n_clusters):
        #    print n, sum(clusters==n), list(wordvectors_df.index[clusters==n])
        
        self.word2cluster = dict(zip(wordvectors_df.index,map(str,clusters)))
        
    def apply(self,essay):
        text = essay.texts[self.source].lower()
        text_new = []
        for word in text.split():
            try:
                text_new.append(self.word2cluster[word])
            except KeyError:
                text_new.append("OTHER_WORD")
        essay.texts[self.dest] = " ".join(text_new)
import pandas as pd
from textblob import TextBlob, Word

from features.skipgrams import EssaySkipgram
from features.essay_feature import EssayFeature, FunctionalTextEssayFeature, EssayTextConversion, EssayAddVector
from features.text_features import *
from features.word2vec_word_clusters import EssayTextToW2VClusters
from features.wiki_ngram_coverage import check_1gram_coverage, check_2gram_coverage, check_3gram_coverage
from features.convert_text_to_definitions import convert_text_to_definitions

#from features.word2vec_features import EssayWord2Vec, EssayWord2VecFirstWords
from lib.math.text_to_math import text_to_math
from lib.math.math_helpers import get_math_expressions_features, leave_only_math_expressions
from lib.clean_text import safe_clean_text
from lib.spellcheck.spell_corrector import correct_text
from lib.porter import stemmer
import langid

pipeline_1 = {
    "name":"DATASET_1",
    "steps":[
         EssayTextConversion(source="raw",dest="clean",fun=safe_clean_text)
        ,EssayTextConversion(source="clean",dest="clean",fun=text_to_math)
        
        ,FunctionalTextEssayFeature(feature_name="n_words_raw", fun=lambda essay: n_words(essay.texts["raw"])/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_raw", fun=lambda essay: (text_length(essay.texts["raw"]))/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_2nd_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.50)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_4th_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.25)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_4_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],4)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_6_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],6)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_8_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],8)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_10_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_12_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],12)/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_mean_raw", fun=lambda essay: words_length_mean(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_variance_raw", fun=lambda essay: words_length_variance(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="unique_words_norm_raw", fun=lambda essay: unique_words_norm(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_10_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_18_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],18)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_25_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],25)/100.0)
        
        ,EssaySkipgram(name="LETTER",source="clean",base=lambda text: text, nskip=0, ngram=3)
        ,EssaySkipgram(name="WORD",source="clean",base=lambda text: text.split(), nskip=0, ngram=1)
    ]
}

pipeline_2 = {
    "name":"DATASET_2",
    "steps":[
         EssayTextConversion(source="raw",dest="clean",fun=safe_clean_text)
        ,EssayTextConversion(source="clean",dest="clean",fun=text_to_math)
        ,EssayTextConversion(source="clean",dest="stem",fun=lambda text: " ".join([stemmer(t) for t in text.split()]))
        ,EssayTextConversion(source="clean",dest="pos",fun=lambda text: " ".join([k[1] for k in TextBlob(text).tags]))
        
        ,EssayFeature(fun=lambda essay: get_math_expressions_features(essay.texts["clean"]))
        ,FunctionalTextEssayFeature(feature_name="n_words_raw", fun=lambda essay: n_words(essay.texts["raw"])/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_raw", fun=lambda essay: (text_length(essay.texts["raw"]))/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_2nd_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.50)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_4th_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.25)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_4_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],4)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_6_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],6)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_8_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],8)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_10_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_12_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],12)/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_mean_raw", fun=lambda essay: words_length_mean(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_variance_raw", fun=lambda essay: words_length_variance(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="unique_words_norm_raw", fun=lambda essay: unique_words_norm(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_10_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_18_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],18)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_25_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],25)/100.0)
        
        ,FunctionalTextEssayFeature(feature_name="wiki_1gram_coverage", fun=lambda essay: check_1gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_2gram_coverage", fun=lambda essay: check_2gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_3gram_coverage", fun=lambda essay: check_3gram_coverage(essay.texts["raw"]))
    
        # sentiment
        ,FunctionalTextEssayFeature(feature_name="sentiment_polarity", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.polarity)
        ,FunctionalTextEssayFeature(feature_name="sentiment_subj", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.subjectivity)
        
        # ngrams    
        ,EssaySkipgram(name="LETTER1",source="raw",base=lambda text: text, nskip=0, ngram=1) # count of each character        
        ,EssaySkipgram(name="LETTER2",source="clean",base=lambda text: text, nskip=0, ngram=3)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=1)
        ,EssaySkipgram(name="POS1",source="pos",base=lambda text: text.split(), nskip=0, ngram=1)
    ]
}

pipeline_3 = {
    "name":"DATASET_3",
    "steps":[
         EssayTextConversion(source="raw",dest="clean",fun=safe_clean_text)
        ,EssayTextConversion(source="clean",dest="clean",fun=text_to_math)
        ,EssayTextConversion(source="clean",dest="stem",fun=lambda text: " ".join([stemmer(t) for t in text.split()]))
        ,EssayTextConversion(source="clean",dest="pos",fun=lambda text: " ".join([k[1] for k in TextBlob(text).tags]))
        
        ,EssayTextToW2VClusters(source="clean",dest="w2v",n_clusters=lambda d: int(d/4),w2v_path="/home/pawel/McGraw/v2/features/GoogleNews-vectors-negative300.bin")
    
        ,EssayFeature(fun=lambda essay: get_math_expressions_features(essay.texts["clean"]))
        ,FunctionalTextEssayFeature(feature_name="n_words_raw", fun=lambda essay: n_words(essay.texts["raw"])/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_raw", fun=lambda essay: (text_length(essay.texts["raw"]))/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_2nd_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.50)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_4th_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.25)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_4_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],4)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_6_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],6)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_8_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],8)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_10_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_12_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],12)/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_mean_raw", fun=lambda essay: words_length_mean(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_variance_raw", fun=lambda essay: words_length_variance(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="unique_words_norm_raw", fun=lambda essay: unique_words_norm(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_10_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_18_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],18)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_25_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],25)/100.0)
        
        ,FunctionalTextEssayFeature(feature_name="wiki_1gram_coverage", fun=lambda essay: check_1gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_2gram_coverage", fun=lambda essay: check_2gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_3gram_coverage", fun=lambda essay: check_3gram_coverage(essay.texts["raw"]))
    
        # sentiment
        ,FunctionalTextEssayFeature(feature_name="sentiment_polarity", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.polarity)
        ,FunctionalTextEssayFeature(feature_name="sentiment_subj", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.subjectivity)
        
        # ngrams    
        ,EssaySkipgram(name="LETTER1",source="raw",base=lambda text: text, nskip=0, ngram=1) # count of each character        
        ,EssaySkipgram(name="LETTER2",source="clean",base=lambda text: text, nskip=0, ngram=3)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=1)
        ,EssaySkipgram(name="WORD",source="w2v",base=lambda text: text.split(), nskip=0, ngram=1)
        ,EssaySkipgram(name="POS1",source="pos",base=lambda text: text.split(), nskip=0, ngram=1)
    ]
}


# pipeline_2
# + 2grams
# + 3grams
pipeline_4 = {
    "name":"DATASET_4",
    "steps":[
         EssayTextConversion(source="raw",dest="clean",fun=safe_clean_text)
        ,EssayTextConversion(source="clean",dest="clean",fun=text_to_math)
        ,EssayTextConversion(source="clean",dest="stem",fun=lambda text: " ".join([stemmer(t) for t in text.split()]))
        ,EssayTextConversion(source="clean",dest="pos",fun=lambda text: " ".join([k[1] for k in TextBlob(text).tags]))
        
        ,EssayFeature(fun=lambda essay: get_math_expressions_features(essay.texts["clean"]))
        ,FunctionalTextEssayFeature(feature_name="n_words_raw", fun=lambda essay: n_words(essay.texts["raw"])/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_raw", fun=lambda essay: (text_length(essay.texts["raw"]))/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_2nd_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.50)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_4th_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.25)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_4_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],4)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_6_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],6)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_8_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],8)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_10_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_12_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],12)/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_mean_raw", fun=lambda essay: words_length_mean(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_variance_raw", fun=lambda essay: words_length_variance(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="unique_words_norm_raw", fun=lambda essay: unique_words_norm(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_10_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_18_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],18)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_25_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],25)/100.0)
        
        ,FunctionalTextEssayFeature(feature_name="wiki_1gram_coverage", fun=lambda essay: check_1gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_2gram_coverage", fun=lambda essay: check_2gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_3gram_coverage", fun=lambda essay: check_3gram_coverage(essay.texts["raw"]))
    
        # sentiment
        ,FunctionalTextEssayFeature(feature_name="sentiment_polarity", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.polarity)
        ,FunctionalTextEssayFeature(feature_name="sentiment_subj", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.subjectivity)
        
        # ngrams    
        ,EssaySkipgram(name="LETTER1",source="raw",base=lambda text: text, nskip=0, ngram=1) # count of each character        
        ,EssaySkipgram(name="LETTER2",source="clean",base=lambda text: text, nskip=0, ngram=3)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=1)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=2)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=3)
        ,EssaySkipgram(name="POS1",source="pos",base=lambda text: text.split(), nskip=0, ngram=1)
    ]
}

# pipeline_4
# + spell checking
pipeline_5 = {
    "name":"DATASET_5",
    "steps":[
         EssayTextConversion(source="raw",dest="clean",fun=safe_clean_text)
        ,EssayTextConversion(source="clean",dest="clean",fun=text_to_math)
        ,EssayTextConversion(source="clean",dest="clean",fun=correct_text)        
        ,EssayTextConversion(source="clean",dest="stem",fun=lambda text: " ".join([stemmer(t) for t in text.split()]))
        ,EssayTextConversion(source="clean",dest="pos",fun=lambda text: " ".join([k[1] for k in TextBlob(text).tags]))
        
        ,EssayFeature(fun=lambda essay: get_math_expressions_features(essay.texts["clean"]))
        ,FunctionalTextEssayFeature(feature_name="n_words_raw", fun=lambda essay: n_words(essay.texts["raw"])/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_raw", fun=lambda essay: (text_length(essay.texts["raw"]))/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_2nd_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.50)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_4th_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.25)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_4_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],4)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_6_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],6)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_8_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],8)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_10_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_12_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],12)/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_mean_raw", fun=lambda essay: words_length_mean(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_variance_raw", fun=lambda essay: words_length_variance(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="unique_words_norm_raw", fun=lambda essay: unique_words_norm(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_10_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_18_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],18)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_25_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],25)/100.0)

        ,FunctionalTextEssayFeature(feature_name="wiki_1gram_coverage", fun=lambda essay: check_1gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_2gram_coverage", fun=lambda essay: check_2gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_3gram_coverage", fun=lambda essay: check_3gram_coverage(essay.texts["raw"]))
    
        # sentiment
        ,FunctionalTextEssayFeature(feature_name="sentiment_polarity", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.polarity)
        ,FunctionalTextEssayFeature(feature_name="sentiment_subj", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.subjectivity)
        
        # ngrams    
        ,EssaySkipgram(name="LETTER1",source="raw",base=lambda text: text, nskip=0, ngram=1) # count of each character        
        ,EssaySkipgram(name="LETTER2",source="clean",base=lambda text: text, nskip=0, ngram=3)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=1)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=2)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=3)
        #,EssaySkipgram(name="WORD",source="w2v",base=lambda text: text.split(), nskip=0, ngram=1)
        ,EssaySkipgram(name="POS1",source="pos",base=lambda text: text.split(), nskip=0, ngram=1)
    ]
}

# pipeline_2 
# + words definitions expand
pipeline_6 = {
    "name":"DATASET_6",
    "steps":[
         EssayTextConversion(source="raw",dest="clean",fun=safe_clean_text)
        ,EssayTextConversion(source="clean",dest="clean",fun=text_to_math)
        ,EssayTextConversion(source="clean",dest="stem",fun=lambda text: " ".join([stemmer(t) for t in text.split()]))
        ,EssayTextConversion(source="clean",dest="pos",fun=lambda text: " ".join([k[1] for k in TextBlob(text).tags]))
        ,EssayTextConversion(source="clean",dest="clean_def",fun=convert_text_to_definitions)
        ,EssayTextConversion(source="clean_def",dest="clean_def",fun=safe_clean_text)
        
        #,EssayTextConversion(source="clean",dest="clean_spell",fun=correct_text)
        #,EssayTextToW2VClusters(source="clean",dest="w2v",n_clusters=lambda d: int(d/4),w2v_path="/home/pawel/McGraw/v2/features/GoogleNews-vectors-negative300.bin")
    
        ,EssayFeature(fun=lambda essay: get_math_expressions_features(essay.texts["clean"]))
        ,FunctionalTextEssayFeature(feature_name="n_words_raw", fun=lambda essay: n_words(essay.texts["raw"])/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_raw", fun=lambda essay: (text_length(essay.texts["raw"]))/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_2nd_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.50)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_4th_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.25)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_4_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],4)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_6_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],6)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_8_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],8)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_10_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_12_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],12)/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_mean_raw", fun=lambda essay: words_length_mean(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_variance_raw", fun=lambda essay: words_length_variance(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="unique_words_norm_raw", fun=lambda essay: unique_words_norm(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_10_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_18_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],18)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_25_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],25)/100.0)
        
        ,FunctionalTextEssayFeature(feature_name="wiki_1gram_coverage", fun=lambda essay: check_1gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_2gram_coverage", fun=lambda essay: check_2gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_3gram_coverage", fun=lambda essay: check_3gram_coverage(essay.texts["raw"]))
    
        # sentiment
        ,FunctionalTextEssayFeature(feature_name="sentiment_polarity", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.polarity)
        ,FunctionalTextEssayFeature(feature_name="sentiment_subj", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.subjectivity)
        
        # ngrams    
        ,EssaySkipgram(name="LETTER1",source="raw",base=lambda text: text, nskip=0, ngram=1) # count of each character        
        ,EssaySkipgram(name="LETTER2",source="clean",base=lambda text: text, nskip=0, ngram=3)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=1)
        ,EssaySkipgram(name="POS1",source="pos",base=lambda text: text.split(), nskip=0, ngram=1)
        ,EssaySkipgram(name="WORD_DEF",source="clean_def",base=lambda text: text.split(), nskip=0, ngram=1)
    ]
}

# pipeline_2
# + 2grams
# + 3grams
# + mathexpressions
pipeline_7 = {
    "name":"DATASET_7",
    "steps":[
         EssayTextConversion(source="raw",dest="clean",fun=safe_clean_text)
        ,EssayTextConversion(source="clean",dest="clean",fun=text_to_math)
        ,EssayTextConversion(source="clean",dest="stem",fun=lambda text: " ".join([stemmer(t) for t in text.split()]))
        ,EssayTextConversion(source="clean",dest="pos",fun=lambda text: " ".join([k[1] for k in TextBlob(text).tags]))
        ,EssayTextConversion(source="clean",dest="mathexpr",fun=leave_only_math_expressions)

        # math features
        ,EssayFeature(fun=lambda essay: get_math_expressions_features(essay.texts["clean"]))
        
        # text statistics        
        ,FunctionalTextEssayFeature(feature_name="n_words_raw", fun=lambda essay: n_words(essay.texts["raw"])/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_raw", fun=lambda essay: (text_length(essay.texts["raw"]))/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_2nd_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.50)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_4th_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.25)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_4_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],4)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_6_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],6)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_8_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],8)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_10_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_12_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],12)/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_mean_raw", fun=lambda essay: words_length_mean(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_variance_raw", fun=lambda essay: words_length_variance(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="unique_words_norm_raw", fun=lambda essay: unique_words_norm(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_10_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_18_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],18)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_25_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],25)/100.0)
        
        # language probability
        ,FunctionalTextEssayFeature(feature_name="langid_lang_prob_en", fun=lambda essay: dict(langid.rank(essay.texts["raw"]))["en"])
        ,FunctionalTextEssayFeature(feature_name="langid_lang_prob_fr", fun=lambda essay: dict(langid.rank(essay.texts["raw"]))["fr"])
        ,FunctionalTextEssayFeature(feature_name="langid_lang_prob_es", fun=lambda essay: dict(langid.rank(essay.texts["raw"]))["es"])        
        
        # wiki coverage
        ,FunctionalTextEssayFeature(feature_name="wiki_1gram_coverage", fun=lambda essay: check_1gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_2gram_coverage", fun=lambda essay: check_2gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_3gram_coverage", fun=lambda essay: check_3gram_coverage(essay.texts["raw"]))
    
        # sentiment
        ,FunctionalTextEssayFeature(feature_name="sentiment_polarity", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.polarity)
        ,FunctionalTextEssayFeature(feature_name="sentiment_subj", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.subjectivity)
        
        # ngrams    
        ,EssaySkipgram(name="LETTER1",source="raw",base=lambda text: text, nskip=0, ngram=1, cumulative=True) # count of each character        
        ,EssaySkipgram(name="LETTER2",source="raw",base=lambda text: text, nskip=0, ngram=2) # count of each character        
        ,EssaySkipgram(name="LETTER3",source="clean",base=lambda text: text, nskip=0, ngram=3)
        ,EssaySkipgram(name="LETTER4",source="clean",base=lambda text: text, nskip=0, ngram=4)
        
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=1)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=2)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=3)
        ,EssaySkipgram(name="WORD",source="mathexpr",base=lambda text: text.split(), nskip=0, ngram=3)        
        ,EssaySkipgram(name="POS1",source="pos",base=lambda text: text.split(), nskip=0, ngram=1)
    ]
}

pipeline_8 = {
    "name":"DATASET_8",
    "steps":[
         EssayTextConversion(source="raw",dest="clean",fun=safe_clean_text)
        ,EssayTextConversion(source="clean",dest="stem",fun=lambda text: " ".join([stemmer(t) for t in text.split()]))
        ,EssayTextConversion(source="clean",dest="pos",fun=lambda text: " ".join([k[1] for k in TextBlob(text).tags]))
        
        ,FunctionalTextEssayFeature(feature_name="n_words_raw", fun=lambda essay: n_words(essay.texts["raw"])/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_raw", fun=lambda essay: (text_length(essay.texts["raw"]))/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_2nd_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.50)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="text_length_4th_root_raw", fun=lambda essay: (text_length(essay.texts["raw"])**0.25)/1000.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_4_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],4)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_6_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],6)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_8_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],8)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_10_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_words_longer_than_12_raw", fun=lambda essay: n_words_longer_than(essay.texts["raw"],12)/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_mean_raw", fun=lambda essay: words_length_mean(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="words_length_variance_raw", fun=lambda essay: words_length_variance(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="unique_words_norm_raw", fun=lambda essay: unique_words_norm(essay.texts["raw"])/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_10_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],10)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_18_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],18)/100.0)
        ,FunctionalTextEssayFeature(feature_name="n_sentences_longer_than_25_raw", fun=lambda essay: n_sentences_longer_than(essay.texts["raw"],25)/100.0)
    
        # ngrams    
        ,EssaySkipgram(name="LETTER1",source="raw",base=lambda text: text, nskip=0, ngram=1, cumulative=True) # count of each character        
        ,EssaySkipgram(name="LETTER2",source="clean",base=lambda text: text, nskip=0, ngram=3)
        ,EssaySkipgram(name="WORD",source="stem",base=lambda text: text.split(), nskip=0, ngram=1)
        ,EssaySkipgram(name="POS1",source="pos",base=lambda text: text.split(), nskip=0, ngram=1)

        # language probability
        ,FunctionalTextEssayFeature(feature_name="langid_lang_prob_en", fun=lambda essay: dict(langid.rank(essay.texts["raw"]))["en"])
        ,FunctionalTextEssayFeature(feature_name="langid_lang_prob_fr", fun=lambda essay: dict(langid.rank(essay.texts["raw"]))["fr"])
        ,FunctionalTextEssayFeature(feature_name="langid_lang_prob_es", fun=lambda essay: dict(langid.rank(essay.texts["raw"]))["es"])        
        
        # wiki coverage
        ,FunctionalTextEssayFeature(feature_name="wiki_1gram_coverage", fun=lambda essay: check_1gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_2gram_coverage", fun=lambda essay: check_2gram_coverage(essay.texts["raw"]))
        ,FunctionalTextEssayFeature(feature_name="wiki_3gram_coverage", fun=lambda essay: check_3gram_coverage(essay.texts["raw"]))
    
        # sentiment
        ,FunctionalTextEssayFeature(feature_name="sentiment_polarity", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.polarity)
        ,FunctionalTextEssayFeature(feature_name="sentiment_subj", fun=lambda essay: TextBlob(essay.texts["clean"]).sentiment.subjectivity)
    ]
}
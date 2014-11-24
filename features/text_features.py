from __future__ import division

import numpy as np

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 10:52:14 2014

@author: pawel
"""

"""
    ,FunctionalTextEssayFeature(feature_name="n_words_raw", fun=lambda essay: float(len(essay.texts["raw"].split()))/100)
    ,FunctionalTextEssayFeature(feature_name="text_length_raw", fun=lambda essay: float(len(essay.texts["raw"]))/100)
    ,FunctionalTextEssayFeature(feature_name="avg_word_length_raw", fun=lambda essay: (essay.features["text_length_raw"] / essay.features["n_words_raw"])/100)
"""

#http://www.aclweb.org/anthology/D13-1180

def n_words(text):
    return len(text.split())
    
def text_length(text):
    return len(text)
    
def avg_word_length(text):
    return text_length(text) / n_words(text)
    
def n_words_longer_than(text,longer_than):
    return len([k for k in text.split() if len(k) >= longer_than])    
    
def unique_words_norm(text):
    return len(set(text.split())) / n_words(text)
    
def words_length_mean(text):
    return np.mean([len(k) for k in text.split()])    

def words_length_variance(text):
    return np.var([len(k) for k in text.split()])
    
def n_sentences_longer_than(text,longer_than):
    return len([k for k in text.split(".") if len(k) >= longer_than])
    
def spelling_errors(text):
    return 0
    


    

    
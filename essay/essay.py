import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix

import sys
sys.path.append("..")

from features.essay_feature import EssayFeature, FunctionalTextEssayFeature, EssayTextConversion, EssayTextConversionBatch, EssayAddVector

class Essay():
    def __init__(self,essay_type,raw_text,score1,score2,score3=None,student_id=None,test_id=None):
        self.essay_type = essay_type        
        self.texts = {}
        self.texts["raw"] = str(raw_text)
        self.score1 = score1
        self.score2 = score2
        self.score3 = score3
        self.student_id = student_id
        self.test_id = test_id
        self.features = {}

    def copy_text(self,old,new):
        self.texts[new] = self.texts[old]
        
    def add_feature(self,feature_name, feature_value, sumexisting=False):
        if sumexisting and feature_name in self.features:
            self.features[feature_name] += feature_value
        else:
            self.features[feature_name] = feature_value
            
    def add_features(self, features_dict, sumexisting=False):
        for feature_name, feature_value in features_dict.items():
            self.add_feature(feature_name, feature_value, sumexisting)
        
    def get_features(self):
        return features
        


class EssayCollection():
    def __init__(self,path=None,essay_name=None):
        self.essays = []
        self.essay_name = essay_name
        
        if path is not None:
            self.load_essays_from_path(path)
            
    def filter_essays(self,essays_ind):
        new_collection = EssayCollection()
        for i in essays_ind:
            new_collection.add_essay(self.essays[i])
        return new_collection

    def load_essays_from_path(self,path):
        dataraw = pd.read_csv(path)
        dataraw.read_1_score[np.isnan(dataraw.read_1_score)] = 0
        dataraw.read_2_score[np.isnan(dataraw.read_2_score)] = 0        
        #dataraw.read_3_score[dataraw.read_1_score == dataraw.read_2_score] = dataraw.read_1_score[dataraw.read_1_score == dataraw.read_2_score]
        #dataraw.read_3_score[np.isnan(dataraw.read_3_score)] = dataraw.read_1_score[np.isnan(dataraw.read_3_score)]
    
        for rowi,ess in dataraw.iterrows():
            text = str(ess.data_answer)
            if ess.read_1_score == ess.read_2_score:
                score_final = ess.read_1_score
            elif ess.read_3_score != np.nan:
                score_final = ess.read_3_score
            else:
                score_final = ess.read_1_score        
                
            self.add_essay(Essay(essay_type=ess.label
                                ,raw_text=text
                                ,score1=ess.read_1_score
                                ,score2=ess.read_2_score
                                ,score3=score_final
                                ,student_id=ess.data_meta_vendor_student_id
                                ,test_id=ess.data_meta_student_test_id))

    def add_essay(self,essay):
        self.essays.append(essay)
        
    def apply_datasteps(self,datasteps):
        for step in datasteps:
            if isinstance(step,EssayTextConversion):
                for essay in self.essays:    
                    step.apply(essay)
            elif isinstance(step,EssayFeature):
                for essay in self.essays:    
                    features = step.generate(essay)
                    essay.add_features(features)
            elif isinstance(step,EssayTextConversionBatch):
                step.fit(self.essays)
                for essay in self.essays:    
                    step.apply(essay)
            elif isinstance(step,EssayAddVector):
                vector = step.generate(self.essay_name)
                feature_name = step.feature_name
                for essay,value in zip(self.essays, vector):
                    essay.add_features({feature_name:value})
            else:
                raise TypeError, "datastep instance not defined"
  
    def meta_data(self):
        meta_data = pd.DataFrame({
            'essay_type':[e.essay_type for e in self.essays]        
           ,'score1':[e.score1 for e in self.essays]
           ,'score2':[e.score2 for e in self.essays]
           ,'score3':[e.score3 for e in self.essays]
           ,'student_id':[e.student_id for e in self.essays]
           ,'test_id':[e.test_id for e in self.essays]

        })
        meta_data.fillna(0,inplace=True)
        return meta_data
      
    def create_feature_matrix(self,min_sparsity=None):
        # create a list of features
        features = {}
        for essay in self.essays:
            for feature_name in essay.features.keys():
                try:
                    features[feature_name] += 1
                except KeyError:
                    features[feature_name] = 1
        
        # remove sparse features
        if min_sparsity is not None:
            for feature_name, feature_freq in features.items():
                if feature_freq <= min_sparsity:
                    del features[feature_name]
        
        features = features.keys()
        features_set = set(features)
        features_ind_dict = dict(zip(features,range(len(features))))        
        
        # create sparse matrix
        rows = []
        cols = []
        data = []
        
        self.feature_names = []
        for rowi, essay in enumerate(self.essays):
            for feature_name, value in essay.features.items():
                if feature_name in features_set:            
                    coli = features_ind_dict[feature_name]
                    rows.append(rowi)
                    cols.append(coli)
                    data.append(value)
                    self.feature_names.append(feature_name)
                    
        rows = np.array(rows)
        cols = np.array(cols)
        data = np.array(data)
                    
        self.feature_matrix = coo_matrix((data, (rows,cols))).tocsr()
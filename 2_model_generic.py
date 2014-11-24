import sys
from lib.data_frame_utils import get_nonduplicate_columns

from collections import OrderedDict
import string
import glob
import os

import xgboost as xgb
import glob

# models
from multiprocessing import Pool

import numpy as np
import pandas as pd
from sklearn import cross_validation
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from nolearn.dbn import DBN

from lib import kappa
from lib.utils import logit
import re

from pipelines import *
from essay.essay import EssayCollection

def cv(args):
    kf, X_all, y_all, model, n = args
    tr_ind = kf[n][0]
    te_ind = kf[n][1]
    
    X_tr = np.array(X_all[tr_ind,:])
    y_tr = np.array(y_all[tr_ind])   
    X_te = np.array(X_all[te_ind,:])
    
    _ = model.fit(X_tr, y_tr)
    pred = model.predict_proba(X_te)
    return pred
    

MODEL_PATHS = "models/"

def model_generic_1ofK_clas(pipeline,model_name,model_f,essays_paths,parallel = False):
    print model_name
    for essaypath in sorted(essays_paths):
        print essaypath, 
        essayname = essaypath.split("/")[-1].split(".")[0]
        save_as = MODEL_PATHS + essayname + "_" + pipeline["name"] + "_" + model_name 
        if os.path.exists(save_as):
            print "Skipping"
            continue
        
        essays = EssayCollection(essaypath,essayname)
        essays.apply_datasteps(pipeline["steps"])
        essays.create_feature_matrix(min_sparsity=5)
                
        predictions = pd.DataFrame({'id':range(essays.meta_data().shape[0])})
        trainset = np.where(essays.meta_data().essay_type == "TRAINING")[0]
        testset = np.where(essays.meta_data().essay_type == "")[0]
        
        X_all = np.array(essays.feature_matrix.todense(),dtype=np.float32)
        y_all = np.array(essays.meta_data()["score3"].map(int),dtype=np.int32)
        non_duplicated = get_nonduplicate_columns(pd.DataFrame(X_all))
        
        print "orig dimensions", X_all.shape[1],
        X_all = X_all[:,non_duplicated]
        print "reduced dimensions", X_all.shape[1], 
        
        predictions = pd.DataFrame({'id':range(essays.meta_data().shape[0])})
        trainset = np.where(essays.meta_data().essay_type == "TRAINING")[0]
        testset = np.where(essays.meta_data().essay_type == "VALIDATION")[0]          
                  
        for scorer in [3]:
            kf = cross_validation.KFold(len(trainset), n_folds=7, random_state=0)
            kf = [(trainset[tr], trainset[te]) for tr, te in kf] + [(trainset,testset)]
              
            for grade in sorted(essays.meta_data()["score%d" % (scorer)].unique()):
                y_all = np.array(essays.meta_data()["score%d" % (scorer)].map(lambda y: 1 if int(y)==int(grade) else 0))
        
                pred_name = "scorer_%d_grade_%d" % (scorer,grade)
                predictions[pred_name] = 0        

                if parallel:
                    pool = Pool(processes=4)
                    essay_sets = pool.map(cv, [[kf, X_all, y_all, model_f, n] for n in range(8)])
                    pool.close()
        
                    for n, essay_set in enumerate(essay_sets):
                        te_ind = kf[n][1]
                        predictions.ix[te_ind,pred_name] = essay_set[:,1]               
                else:
                    for n,(tr_ind,te_ind) in enumerate(kf):
                        predictions.ix[te_ind,pred_name] = model_f(X_all[tr_ind,:], 
                                                                   y_all[tr_ind],
                                                                   X_all[te_ind,:],
                                                                   feature_names=essays.feature_names)
                    
             
        predictions = predictions.ix[:,sorted(predictions.columns)]
        predictions["pred_scorer_3"] = np.array(predictions.ix[:,[c for c in predictions.columns if c.startswith("scorer_3")]]).argmax(axis=1)
        predictions.to_csv(save_as,index=False)
        print kappa.quadratic_weighted_kappa(essays.meta_data()["score3"][trainset],predictions["pred_scorer_3"][trainset])

def model_generic_DBN(pipeline,model_name,model_f,essays_paths,parallel = False):
    print model_name
    for essaypath in sorted(essays_paths):
        print essaypath, 
        essayname = essaypath.split("/")[-1].split(".")[0]
        save_as = MODEL_PATHS + essayname + "_" + pipeline["name"] + "_" + model_name 
        if os.path.exists(save_as):
            print "Skipping"
            continue
        
        essays = EssayCollection(essaypath,essayname)
        essays.apply_datasteps(pipeline["steps"])
        essays.create_feature_matrix(min_sparsity=5)
                
        predictions = pd.DataFrame({'id':range(essays.meta_data().shape[0])})
        trainset = np.where(essays.meta_data().essay_type == "TRAINING")[0]
        testset = np.where(essays.meta_data().essay_type == "")[0]
        
        X_all = np.array(essays.feature_matrix.todense(),dtype=np.float32)
        y_all = np.array(essays.meta_data()["score3"].map(int),dtype=np.int32)
        non_duplicated = get_nonduplicate_columns(pd.DataFrame(X_all))
        
        print "orig dimensions", X_all.shape[1],
        X_all = X_all[:,non_duplicated]
        print "reduced dimensions", X_all.shape[1], 

        predictions = pd.DataFrame({'id':range(essays.meta_data().shape[0])})
        trainset = np.where(essays.meta_data().essay_type == "TRAINING")[0]
        testset = np.where(essays.meta_data().essay_type == "VALIDATION")[0]          

        scorer = 3
        kf = cross_validation.KFold(len(trainset), n_folds=7, random_state=0)
        kf = [(trainset[tr], trainset[te]) for tr, te in kf] + [(trainset,testset)]

        scores = sorted(essays.meta_data()["score%d" % (scorer)].unique())
        predictions = np.zeros((essays.meta_data().shape[0],len(scores)))
        
        model_f.layer_sizes[0] = X_all.shape[1]
        model_f.layer_sizes[2] = len(scores)        
        
        try:
            for n,(tr_ind,te_ind) in enumerate(kf):
                print n
                scaler = StandardScaler()
                _ = scaler.fit(X_all[tr_ind,:])
                X_tr = scaler.transform(X_all[tr_ind,:]) / 50.0
                X_te = scaler.transform(X_all[te_ind,:]) / 50.0
                model_f.fit(X_tr, y_all[tr_ind])
                print kappa.quadratic_weighted_kappa(essays.meta_data()["score3"][tr_ind],model_f.predict(X_tr))
                print kappa.quadratic_weighted_kappa(essays.meta_data()["score3"][te_ind],model_f.predict(X_te))
                predictions[te_ind,:] = model_f.predict_proba(X_te)                    
        except:
            pass
             
        predictions = pd.DataFrame(predictions)
        predictions.columns = ["scorer_%d_grade_%d" % (scorer,grade) for grade in scores]
        predictions["pred_scorer_3"] = np.array(predictions).argmax(axis=1)
        predictions.to_csv(save_as,index=False)
        print kappa.quadratic_weighted_kappa(essays.meta_data()["score3"][trainset],predictions["pred_scorer_3"][trainset])

              
        
def xgb_model(xgbparam, ntrees):
    def helper(X_tr, y_tr, X_te, feature_names=None):
        xgmat_tr = xgb.DMatrix( X_tr, label=y_tr, missing = -999.0 )
        xgmat_te = xgb.DMatrix( X_te, missing = -999.0 )
        bst = xgb.train(xgbparam, xgmat_tr, ntrees)
        return bst.predict( xgmat_te )    
    return helper
    
def sklearn_prob_model(model_class,scaled=False):
    def helper(X_tr, y_tr, X_te, feature_names=None):
        if scaled:
            scaler = StandardScaler()
            scaler.fit(X_tr)
            X_tr = scaler.transform(X_tr)
            X_te = scaler.transform(X_te)
        model_class.fit(X_tr,y_tr)
        return model_class.predict_proba(X_te)[:,1]
    return helper

def serialize_dict(d):
    return "_".join(["%s=%s" % (k,v) for k,v in d.items()])

def test_essays():
    essays_paths = glob.glob("data/csv/*.csv")
    for essaypath in sorted(essays_paths):
        essayname = essaypath.split("/")[-1].split(".")[0]
        essays = EssayCollection(essaypath,essayname)
        essay_types = essays.meta_data()["essay_type"]
        print essayname, "TR", (essay_types=="TRAINING").sum(), "VA", (essay_types=="VALIDATION").sum() 

if __name__ == "__main__":
    ALL_ESSAYS = glob.glob("data/csv/*.csv")
    HARD_ESSAYS = ["data/csv/%s.csv" % (k) for k in ["24020_1","24027_1","27210_1","29134_1","58921_1"]]
    PIPELINES = [pipeline_1, pipeline_2, pipeline_3, pipeline_4, pipeline_5, pipeline_6, pipeline_7, pipeline_8]

    for pipe in [pipeline_3]:    
        model_generic_1ofK_clas(pipe,
                      model_name="rf_1",
                      model_f=sklearn_prob_model(RandomForestClassifier(n_estimators=200,n_jobs=6)),
                      essays_paths=ALL_ESSAYS,
                      parallel=False)

    for pipe in [pipeline_8]:
        model_generic_DBN(pipeline = pipe, model_name = "nn_3", 
                          model_f = DBN([-1, 800, -1],
                                          learn_rates=0.1,
                                          learn_rate_decays=0.9,
                                          use_re_lu=True,
                                          epochs=200, 
                                          verbose=0,
                                          dropouts=[0.5,0.1,0.0],
                                          momentum=0.9),
                          essays_paths = ALL_ESSAYS)

    for pipe in PIPELINES:    
        for ntrees in [50,100,200,300]:
            xgbparam={'max_depth':6, 'eta':0.1, 'silent':1, 'objective':'binary:logistic', 'nthread':6}
            xgbparamser = serialize_dict(xgbparam) + "_ntrees=%d" % (ntrees)
            model_generic_1ofK_clas(pipe, model_name="xgb_" + xgbparamser, model_f=xgb_model(xgbparam=xgbparam, ntrees=ntrees), essays_paths=ALL_ESSAYS)
    
    # optimize hard essays
    for pipe in PIPELINES:
        for ntrees in [100,200,300,400]:
            for maxdepth in [3,4,5,6,8,10]:
                xgbparam={'max_depth':maxdepth, 'eta':0.1, 'silent':1, 'objective':'binary:logistic', 'nthread':6}
                xgbparamser = serialize_dict(xgbparam) + "_ntrees=%d" % (ntrees)
                model_generic_1ofK_clas(pipe, 
                              model_name="xgb_est_%d_depth_%d" % (ntrees,maxdepth), 
                              model_f=xgb_model(xgbparam=xgbparam, ntrees=ntrees),
                              essays_paths=HARD_ESSAYS)

    for pipe in PIPELINES:        
        model_generic_DBN(pipeline = pipe, model_name = "nn_1", 
                          model_f = DBN([-1, 100, -1],
                                          learn_rates=0.1,
                                          learn_rate_decays=0.9,
                                          epochs=100, 
                                          verbose=0,
                                          momentum=0.9),
                          essays_paths = ALL_ESSAYS)
    
        model_generic_DBN(pipeline = pipe, model_name = "nn_2", 
                          model_f = DBN([-1, 100, -1],
                                          learn_rates=0.1,
                                          output_act_funct="Sigmoid",
                                          learn_rate_decays=0.9,
                                          epochs=100, 
                                          verbose=0,
                                          momentum=0.9),
                          essays_paths = ALL_ESSAYS)

import glob
import os
import numpy as np
import pandas as pd

from essay.essay import EssayCollection
from lib import kappa
from lib.utils import logit
from scipy.optimize import fmin, fmin_bfgs, fmin_cg, fmin_ncg
from sklearn import cross_validation
from sklearn.linear_model import ElasticNet

results = open("results.csv","w")
results.write("essay,model,score\n")
for essaypath in sorted(glob.glob("data/csv/*.csv")):
    print essaypath, 
    essays = EssayCollection(essaypath)
    
    essayname = os.path.split(essaypath)[-1][:-4]
    predictions_all_list = []
    trainset = np.where(essays.meta_data().essay_type=="TRAINING")[0]
    for modelpath in glob.glob("models/*" + essayname + "*"):
        modelname = os.path.split(modelpath)[-1]
        predictions = pd.read_csv(modelpath)
        predictions["modelname"] = modelname
        results.write("%s,%s,%.6f\n" % (essayname, modelname[8:], kappa.quadratic_weighted_kappa(essays.meta_data()["score3"][trainset],predictions["pred_scorer_3"][trainset])))
        predictions_all_list.append(predictions.copy())

    results.write("%s,%s,%.6f\n" % (essayname, "HUMAN", kappa.quadratic_weighted_kappa(essays.meta_data()["score1"][trainset],essays.meta_data()["score2"][trainset])))
    
    predictions_all = pd.concat(predictions_all_list)
    scores = [col for col in predictions_all.columns if col.find("grade") > 0]    
    
    for score_col in scores:
        predictions_all.ix[:,score_col] = predictions_all.ix[:,score_col].map(logit)
    
    unique_models = predictions_all.modelname.unique()
    n_obs = essays.meta_data().shape[0]
    predictions_matrix = np.zeros((len(scores), unique_models.shape[0], n_obs))
    for n_score, score in enumerate(scores):    
        for n_model, model in enumerate(unique_models):
            predictions_matrix[n_score,n_model,:] = predictions_all_list[n_model][score]
    predictions_matrix = predictions_matrix.transpose(2,0,1)

    # set up cross validatio
    cvsets = cross_validation.KFold(len(trainset),10,random_state=0)
    trainset = np.where(essays.meta_data().essay_type == "TRAINING")[0]
    testset = np.where(essays.meta_data().essay_type == "VALIDATION")[0]          
    cvsets = [(trainset[tr], trainset[te]) for tr, te in cvsets] + [(trainset,testset)]

    # set up final dataframe
    predictions_df = pd.DataFrame({'id':range(essays.meta_data().shape[0])
                                ,'student_id': essays.meta_data()["student_id"]
                                ,'test_id': essays.meta_data()["test_id"]
                                ,'essay_type': essays.meta_data()["essay_type"]
                                ,'final_score': None})
    predictions_df = predictions_df.ix[:,['id','essay_type','student_id','test_id','final_score']]

    # add scores probablities columns
    scores_prob_cols = []
    for score_col in range(len(scores)):
        col = "score_%d_prob" % (score_col)
        predictions_df[col] = None
        scores_prob_cols.append(col)
                                
    real_scores = np.array(essays.meta_data()["score3"])

    # direct optimize
    def optimize(selected_obs):
        def opt_fn(coef):
            predictions_vector = np.dot(predictions_matrix[selected_obs],coef)
            predictions_grade = np.argmax(predictions_vector,axis=1)
            weighted_kappa = kappa.quadratic_weighted_kappa(real_scores[selected_obs], predictions_grade)
            return -weighted_kappa
        return opt_fn

    nopt = 40
    for train,test in cvsets:
        coef = np.zeros(len(unique_models))    
        for n in range(nopt):
            coef += fmin(optimize(np.random.choice(train,len(train)/2)), np.zeros(len(unique_models)),disp=False)
        predictions_df.ix[test,scores_prob_cols] = np.dot(predictions_matrix[test,:,:],coef / nopt)

    predictions_df["final_score"] = np.argmax(np.array(predictions_df.ix[:,scores_prob_cols]),axis=1)

    predictions_df.to_csv("ensemble/%s.csv" % (essayname),index=False)

    weighted_kappa = kappa.quadratic_weighted_kappa(real_scores[trainset], predictions_df.final_score[trainset])    
    print weighted_kappa
    
    results.write("%s,%s,%.6f\n" % (essayname, "ENSEMBLE", weighted_kappa))

results.close()

# save some results
results = pd.read_csv("results.csv")
pivot = results.pivot("essay","model","score")
pivot["diff"] = pivot.ENSEMBLE - pivot.HUMAN

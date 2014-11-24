# -*- coding: utf-8 -*-
import cPickle as pickle

import numpy as np
from sklearn.externals import joblib
import glob
import pandas as pd
import os
from lib.utils import logitinv
from scipy.optimize import fmin
from sklearn.metrics import log_loss
from essay.essay import EssayCollection


ALL_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Job_Details xmlns="http://www.imsglobal.org/xsd/imscp_v1p1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ctb_score.xsd" Score_Provider_Name="AI-XX" Case_Count="10" Date_Time="20130815160834">
%s</Job_Details>
"""

ITEM_XML = """   <Student_Details Vendor_Student_ID="%(student_id)s">
      <Student_Test_List>
         <Student_Test_Details Student_Test_ID="%(test_id)s" Grade="%(final_score)s" Total_CR_Item_Count="1">
            <Item_DataPoint_List>
               <Item_DataPoint_Details Item_ID="%(item_id)s" Data_Point="" Item_No="1" Final_Score="%(final_score)d">
                  <Read_Details Read_Number="1" Score_Value="%(final_score)s" Reader_ID="1" Date_Time="20141026134100" />
               </Item_DataPoint_Details>
            </Item_DataPoint_List>
         </Student_Test_Details>
      </Student_Test_List>
   </Student_Details>
"""


for ensemblepath in glob.glob("ensemble/*.csv"):
    preds = pd.read_csv(ensemblepath)
    item_id = os.path.split(ensemblepath)[-1][:5]    
    essays = EssayCollection("data/csv/" + item_id + "_1.csv")
    realscores = essays.meta_data()["score3"]
    scores = [col for col in preds.columns if col.find("prob") > 0]

    # optimize probability
    optpar = np.array([0.0,0.0])
    for grade,col in enumerate(scores): 
        trainpred = np.array(preds.ix[preds.essay_type=="TRAINING",col])
        trainreal = np.array((realscores[preds.essay_type=="TRAINING"]==grade).map(int))
        def fnopt(par):
            loss = log_loss(trainreal, logitinv(par[0]*trainpred+par[1]))
            return loss
        opt = fmin(fnopt, np.array([0.0,0.0]))
        optpar += opt
    
    optpar /= len(scores)
    preds.ix[:,scores] = logitinv(optpar[0]*preds.ix[:,scores]+optpar[1])
    preds_validation = preds.ix[preds.essay_type=="VALIDATION",:]
    
    assert np.all(np.argmax(preds_validation.ix[:,scores].as_matrix(),axis=1)==np.array(preds_validation.final_score))    
    
    items = []
    for _, record in preds_validation.iterrows():
        record = dict(record)
        record["item_id"] = item_id
        item = ITEM_XML % dict(record)
        items.append(item)
            
    preds_validation.ix[:,["student_id","test_id","final_score"] + scores].to_csv("final_scores/" + item_id + "_AI-PJ_scores_probs.csv",index=False)
    out = open("final_scores/" + item_id + "_AI-PJ_scores.xml","w")
    out.write(ALL_XML % ("".join(items)))
    out.close()

import pandas as pd
import numpy as np

from scipy.stats import pearsonr

def convert_to_numerical(df,keep_original=None,remove_useless_variables=True,dtype=np.float32):
    """
    Converts the dataframe to numerical data frame
    Categorical variables are changed to binary
    Categorical variables with only 2 unique values are compressed to binary
    """
    if keep_original is None:
        keep_original = []
    
    new_df = pd.DataFrame({"row_id": range(df.shape[0])})
    new_df.reset_index()
    df["row_id"] = range(df.shape[0])
    cols = list(df.columns)
    column_names = []
    categories = []
    
    for col in cols:
        unique_values = df[col].unique()
        if col in keep_original + ["row_id"]:
            pass
        elif col in keep_original:
            column_name = col
            new_df[column_name] = df[col]
            column_names.append(column_name)   
            categories.append(col)
        elif len(unique_values) == 2:                
            values = df[col].map(str)
            values_max = values.max()
            values = values.map(lambda x: 1 if x == values_max else 0).astype('int8')
            column_name = col
            new_df[column_name] = values
            column_names.append(column_name)
            categories.append(col)
        elif df[col].dtype == "object":
            df["count"] = 1       
            df[col] = df[col].map(str)
            dfp = df.pivot(index="row_id",columns=col,values="count").fillna(0).astype('int8')
            new_column_names = ["CAT_%s_%s" % (col,c) for c in dfp.columns]
            dfp.columns = new_column_names
            new_df = pd.concat([new_df,dfp],axis=1)
            column_names.extend(new_column_names)
            categories.extend([col]*dfp.shape[1])
        else:
            column_name = col
            new_df[column_name] = df[col].astype(dtype)
            column_names.append(column_name)            
            categories.append(col)

    new_df = new_df.drop("row_id",axis=1)
    new_df.columns = column_names
    new_df.categories = categories
    return new_df
    
def factors_target_average(X_tr,y_tr,X_te):
    """    
    data = dataset_2()
    X_tr = data["train"]["X"]    
    y_tr = data["train"]["y"]    
    w_tr = data["train"]["w"]
        
    X_te = data["leaderboard"]["X"]    
    w_te = data["leaderboard"]["w"]
    """
    cols = X_tr.columns    
    y_tr_avg = y_tr.mean()
    
    for col in cols:
        if X_tr[col].dtype == "object":
            dummy_df = pd.DataFrame({"target":y_tr,"col":X_tr[col]})
            means = dummy_df.groupby("col").mean()
            conversion_dict = dict([r for r in means.itertuples()])
            X_tr[col] = X_tr[col].map(lambda v: conversion_dict.get(v,y_tr_avg))            
            X_te[col] = X_te[col].map(lambda v: conversion_dict.get(v,y_tr_avg))
            
    return X_tr, X_te
    
def na_remove(X_tr,X_te):
    for col in range(X_tr.shape[1]):
        col_mean = X_tr[:,col][~np.isnan(arr)].mean()
        X_tr[np.isnan(X_tr[:,col]),col] = col_mean
        X_tr[np.isnan(X_tr[:,col]),col] = col_mean
    return        
    
import hashlib
def hash_array(arr):
   if arr.dtype == "object":
       arr_str = "~PJ~".join(list(map(str,arr))).encode()
       return hashlib.sha1(arr_str).hexdigest()
   else: 
       return hashlib.sha1(np.array(arr).view(arr.dtype)).hexdigest()
       
       
def get_nonduplicate_columns(data):
    import hashlib
    
    hashes = []
    for i,col in enumerate(data.columns):
        hashes.append((i,col,hash_array(data[col])))
        
    # sort hash
    hashes.sort(key = lambda x: x[1])
    
    # diffs
    cols = [(i,col) for i,col,hash_val in hashes]
    hash_vals = pd.Series([hash_val for i,col,hash_val in hashes])
    
    non_duplicated_ind = np.where(~hash_vals.duplicated())[0]
    
    non_duplicated = [cols[i] for i in non_duplicated_ind]
    non_duplicated.sort(key=lambda x: x[0])
    
    return [k[1] for k in non_duplicated]
    
def get_useless_columns(data):
    useless_columns = []
    for col in useless_columns:
        if len(data[col].unique()) == 1:
            print(col)
            useless_columns.append(col)
    

def get_uncorrelated_columns(data,max_correlation = 0.95):
    data_ = np.array(data)
    ncol = data_.shape[1]
    correlated = set()
    for col_a in range(ncol):
        if col_a in correlated:
            continue
        for col_b in range(col_a+1, ncol):
            try:
                c, _ = pearsonr(data_[:,col_a], data_[:,col_b])
                if abs(c) >= max_correlation:
                    correlated.add(col_b)
            except TypeError:
                pass
    non_correlated = sorted(set(range(ncol)) - correlated)
    return non_correlated            

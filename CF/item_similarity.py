# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 13:20:57 2017

@author: sj
"""

import pandas as pd
import numpy as np


train_data = pd.read_csv('datagrand_0517/train.csv')
#train_data.drop(['cate_id','action_time'],axis=1,inplace=True)

trainitem = train_data.item_id.unique()
users = train_data.user_id.unique()
n_trainitem = trainitem.shape[0]
n_users = users.shape[0]

for i in range(n_trainitem):
    i==10
    pv_i = pd.pivot_table(train_data[train_data.item_id==trainitem[i]],index=['user_id'],aggfunc=[np.max],values=['action_type'])
    pv_i.columns = ['action_type_i'] 
    pv_i['user_id']=pv_i.index
    for j in range(i+1,n_users):
#        user_i = train_data[train_data.user_id==users[i]]
#        user_j = train_data[train_data.user_id==users[j]]
        pv_j = pd.pivot_table(train_data[train_data.item_id==trainitem[j]],index=['user_id'],aggfunc=[np.max],values=['action_type'])
        pv_j.columns = ['action_type_j']
        pv_j['user_id']=pv_j.index
        commen = pd.merge(pv_i,pv_j)

        if(j==(i+1)):
            term_dict={trainitem[j]:commen}
        else:
            term_dict[trainitem[j]]=commen
        if(j%100==0):
            print(i,j/n_users)
    if(i==0):
        user_similarity_dict={trainitem[i]:term_dict}
    else:
        user_similarity_dict[trainitem[i]]=term_dict
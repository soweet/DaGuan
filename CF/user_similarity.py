# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 09:10:03 2017

@author: sj
"""

import pandas as pd

train_data = pd.read_csv('datagrand_0517/train.csv')
train_data.drop(['cate_id','action_time'],axis=1,inplace=True)

users = train_data.user_id.unique()
trainitem = train_data.item_id.unique()
n_users = users.shape[0]
n_trainitem = trainitem.shape[0]

#train_data.replace({'action_type':{'view':1,'deep_view':2,'comment':3,'collect':3,'share': 3}},inplace=True)


for i in range(n_users):
    #pv_i = pd.pivot_table(train_data[train_data.user_id==users[i]],index=['item_id'],aggfunc=[np.max],values=['action_type'])
    #pv_i.columns = ['action_type_i'] 
    #pv_i['item_id']=pv_i.index
    useri_items = train_data[train_data.user_id==users[i]]['item_id'].unique()
    for j in range(i+1,n_users):
        userj_items = train_data[train_data.user_id==users[j]]['item_id'].unique()
#        pv_j = pd.pivot_table(train_data[train_data.user_id==users[j]],index=['item_id'],aggfunc=[np.max],values=['action_type'])
#        pv_j.columns = ['action_type_j']
#        pv_j['item_id']=pv_j.index
        #commen = pd.merge(pv_i,pv_j)
        commen = len(set(useri_items)&set(userj_items))
        if(j==(i+1)):
            term_dict={users[j]:commen}
        else:
            term_dict[users[j]]=commen
        if(j%100==0):
            print(i,j/n_users)
    if(i==0):
        user_similarity_dict={users[i]:term_dict}
    else:
        user_similarity_dict[users[i]]=term_dict
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 01:07:51 2017

@author: sj
"""

import pandas as pd
import numpy as np
import timestamp2data

def feature_data(train_data):
    train_data.drop(['action_time'],axis=1,inplace=True)
    train_data.replace({'action_type':{'view':1,'deep_view':2,'comment':3,'collect':3,'share': 3}},inplace=True)
    
    users = train_data.user_id.unique()
    trainitem = train_data.item_id.unique()
    n_users = users.shape[0]
    n_trainitem = trainitem.shape[0]
    
    #user_feature
    user_f=np.zeros([n_users,5])
    #union_feature
    union_f = pd.DataFrame()
    
    for user_i in range(n_users):
        temp=train_data[(train_data.user_id==users[user_i])]
        user_f1 = temp.shape[0] #操作的商品总数
        user_f2 = len(temp.cate_id.unique()) #操作的商品类别数
        user_f3 = temp[temp.action_type==1].shape[0] #view的商品数
        user_f4 = temp[temp.action_type==2].shape[0] #deep_view的商品数
        user_f5 = temp[temp.action_type==3].shape[0] #comment,collect,share的商品数
        user_f[user_i] = [user_f1,user_f2,user_f3,user_f4,user_f5]
        
        useri_cate_pt = pd.pivot_table(temp,columns='cate_id',values='action_type',aggfunc=[np.sum])
        useri_cate_sum = np.sum(useri_cate_pt['sum'])
        useri_cate_pt.columns = ['union_f1'] #用户对该类别操作数
        useri_cate_pt['union_f2'] = list(useri_cate_pt['union_f1']/useri_cate_sum) #用户对该类别操作数/用户总操作数
        useri_cate_pt['cate_id']=list(useri_cate_pt.index)
        useri_cate_pt['user_id']=users[user_i]
        union_f = pd.concat([union_f,useri_cate_pt],axis=0)
        if(user_i%100 == 0):
            print(user_i/n_users)
        
    #user_f = (user_f-np.min(user_f,axis=0))/(np.max(user_f,axis=0)-np.min(user_f,axis=0))
    #item_feature
    temp_cate = train_data.drop(['user_id','item_id'],axis=1)
    temp_cate['count']=1
    p_v_cate = pd.pivot_table(temp_cate,index='cate_id',columns='action_type',values='count',aggfunc=[np.sum])
    p_v_cate.columns = p_v_cate.columns.levels[1]
    p_v_cate = p_v_cate.fillna(0)
    p_v_cate_sum1 = p_v_cate.sum(axis=1)
    p_v_cate_sum2 = p_v_cate_sum1/p_v_cate_sum1.sum()
    del temp_cate
    
    item_f = np.zeros([n_trainitem,10])
    for item_i in range(n_trainitem):
        temp = train_data[(train_data.item_id==trainitem[item_i])]
        item_f1 = temp.shape[0]
        item_f2 = temp[temp.action_type==1].shape[0]
        item_f3 = temp[temp.action_type==2].shape[0]
        item_f4 = temp[temp.action_type==3].shape[0]
        temp_cate = p_v_cate.loc[temp.iloc[0].cate_id]
        if(sum(temp_cate)>0):
            item_f5 = item_f1/sum(temp_cate)
        else:
            item_f5 = 0
        if(temp_cate.iloc[0]>0):
            item_f6 = item_f2/temp_cate.iloc[0]
        else:
            item_f6 = 0
        if(temp_cate.iloc[1]>0):
            item_f7 = item_f3/temp_cate.iloc[1]
        else:
            item_f7 = 0
        if(temp_cate.iloc[2]>0):
            item_f8 = item_f4/temp_cate.iloc[2]
        else:
            item_f8 = 0
        item_f9 = p_v_cate_sum1[temp.iloc[0].cate_id]
        item_f10 = p_v_cate_sum2[temp.iloc[0].cate_id]
        item_f[item_i] = [item_f1,item_f2,item_f3,item_f4,item_f5,item_f6,item_f7,item_f8,item_f9,item_f10]
        if(item_i%100 == 0):
            print(item_i/n_trainitem)
    #item_f = (item_f-np.min(item_f,axis=0))/(np.max(item_f,axis=0)-np.min(item_f,axis=0))
     
    user_feature = pd.DataFrame(user_f,columns=['user_f1','user_f2','user_f3','user_f4','user_f5'])
    user_feature['user_id'] = users
    item_feature = pd.DataFrame(item_f,columns=['item_f1','item_f2','item_f3','item_f4','item_f5','item_f6','item_f7','item_f8','item_f9','item_f10'])
    item_feature['item_id'] = trainitem   

    return user_feature,item_feature,union_f
        
s1 = '2017-02-17 00:00:00'
e1 = '2017-02-18 23:59:59'
s1 = timestamp2data.data2stamp(s1)
e1 = timestamp2data.data2stamp(e1)
train_data = pd.read_csv('datagrand_0517/train.csv')
train_data = train_data[(train_data.action_time>=s1)&(train_data.action_time<=e1)]

user_feature,item_feature,union_f = feature_data(train_data)
user_feature.to_csv('user_feature_17_18.csv')
item_feature.to_csv('item_feature_17_18.csv')
union_f.to_csv('union_feature_17_18.csv')
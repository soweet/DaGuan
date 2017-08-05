# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 06:26:02 2017

@author: sj
"""

import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler

def read_UI():#读取待推荐的用户商品对
    flag=0
    fr = open('feature_tag/prediect_/predict_data.txt')
    lines = fr.readlines()
    for line in lines:
        ele = line.strip().split(':')
        user = ele[0] 
        items = ele[1].split(' ')
        items = [int(x) for x in items]
        if(flag==0):
            user_item_list = {user:items}
            flag = 1
        else:
            user_item_list[user]=items
    return user_item_list
    
    
#加载特征
union_feature = pd.read_csv('feature_tag/prediect_/feature/union_feature.csv')#组合特征
union_feature.drop(['cate_id.1'],axis=1,inplace=True)
item_feature = pd.read_csv('feature_tag/prediect_/feature/item_feature.csv',index_col=0)#咨迅特征
user_feature = pd.read_csv('feature_tag/prediect_/feature/user_feature.csv',index_col=0)#用户特征
item_cate = pd.read_csv('feature_tag/item_cate.csv',index_col=0)  #商品对应的类别

#加载待推荐用户——商品列表
user_item_dic = read_UI()

#加载分类器模型
RFclassifier = joblib.load('save_model/RF.pkl')
GBclassifier = joblib.load('save_model/GB.pkl')

#为每个用户推荐商品
default_rec_items = '557579 558082 558788 557167 558910'  #most popular
i=0
wfr = open('submission0725_user_500.txt','w')
for (user,items) in user_item_dic.items():

    #提取特征
    online_features = pd.DataFrame(items,columns=['item_id']) 
    online_features['user_id'] = user
    online_features = pd.merge(online_features,item_cate,on=['item_id'])
    online_features = pd.merge(online_features,union_feature,on=['user_id','cate_id'])
    online_features = pd.merge(online_features,item_feature,on=['item_id'])
    online_features = pd.merge(online_features,user_feature,on=['user_id'])
    #预测
    if(online_features.shape[0]>0):
        X =  online_features.drop(['item_id','user_id','cate_id'],axis=1)
        del online_features
        y_predprob_RF = RFclassifier.predict_proba(X)
        y_sorted_RF = np.argsort(y_predprob_RF[:,-1])
        rec_items_RF = np.array(items)[y_sorted_RF[:-6:-1]]
    #    y_predprob_GB = GBclassifier.predict_proba(X)
    #    y_sorted_GB = np.argsort(y_predprob_GB[:,-1])
    #    rec_items_GB = np.array(items)[y_sorted_GB[:-6:-1]]
        rec_items_RF = ' '.join([str(x) for x in rec_items_RF])
        wline = user+','+rec_items_RF+'\n'
        wfr.write(wline)
    else:
        wline = user+','+default_rec_items+'\n'
        wfr.write(wline)
    i=i+1
    if(i%100==0):
        print(i/14000)
wfr.close()  #close关闭文件

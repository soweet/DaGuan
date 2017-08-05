# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 16:38:18 2017

@author: sj

得到训练集/测试集：提取正样本，对负样本降采样；将user-item对的标签和特征组合起来。
"""
import pandas as pd
import numpy as np
import timestamp2data

#获得正负样本，rate为负样本采样比例
def tag_data(data_cut,rate):
    data_cut.drop(['action_time','action_type'],axis=1,inplace=True)
    data_cut = data_cut[~data_cut.duplicated()]
    
    users = pd.read_csv('user.csv')
    users = pd.DataFrame(users['user_id'])
    users['user_id']=users['user_id'].apply(lambda x:str(x))
    data_cut = pd.merge(data_cut,users,on='user_id')
    
    #tag
    data_pos = data_cut[['user_id','item_id']]
    #data_pos = data_cut[~data_cut.duplicated()]
    data_pos['tag'] = 1
    
    item_readed_grouped = data_cut['item_id'].groupby([data_cut['user_id'],data_cut['cate_id']])
    data_neg = pd.DataFrame()
    
    flag = 0
    flag1 = data_cut.shape[0]
    for (k1,k2),group in item_readed_grouped:
        neg_num = rate*group.shape[0]
        term_items = np.array(list(set(data_cut[data_cut.cate_id == k2].item_id.unique())-set(group)))
        if(term_items.shape[0]<=neg_num):
            items_neg = pd.DataFrame(term_items)
        else:
            random_neg = np.random.randint(0,term_items.shape[0],size = (1,neg_num))
        #neg_items = term_items[random_neg][0]
            items_neg = pd.DataFrame(term_items[random_neg][0])
        items_neg.columns = ['item_id']
        items_neg['user_id'] = k1
        data_neg = pd.concat([data_neg,items_neg],axis=0)
        if(flag%1000==0):
            print(flag/flag1)
        flag = flag+1
    data_neg['item_id']=data_neg['item_id'].apply(lambda x:int(x))
    data_neg['tag'] = 0
    data_tag = pd.concat([data_pos,data_neg],axis=0)
    
    data_tag.to_csv('train_datatag.csv')
    
    #train_mat = pd.merge(data_tag,user_feature,on='user_id')
    #train_mat = pd.merge(train_mat,item_feature,on='item_id')
    

#将user-item对的标签和相关特征组合在一起，形成完整的训练/测试集
def Union_feature_tag(tag_data):
    
    train_data = pd.read_csv('datagrand_0517/train.csv')
    train_data = train_data[['item_id','cate_id']]
    train_data = train_data[~train_data.duplicated()]
    
    tag_data = pd.merge(tag_data,train_data,on='item_id')
    del train_data
    
    union_feature = pd.read_csv('feature_tag/prediect_/feature/union_feature_17_18.csv')
    union_feature.drop(['cate_id.1'],axis=1,inplace=True)
    
    train_fea_tag = pd.merge(tag_data,union_feature,on=['user_id','cate_id'])
    del union_feature,tag_data
    
    item_feature = pd.read_csv('feature_tag/prediect_/feature/item_feature_17_18.csv',index_col=0)
    user_feature = pd.read_csv('feature_tag/prediect_/feature/user_feature_17_18.csv',index_col=0)
    train_fea_tag = pd.merge(train_fea_tag,item_feature,on=['item_id'])
    train_fea_tag = pd.merge(train_fea_tag,user_feature,on=['user_id'])
    
    train_fea_tag.to_csv('train_fea_tag.csv')



train_data = pd.read_csv('datagrand_0517/train.csv')

s1 = '2017-02-16 00:00:00'
e1 = '2017-02-17 23:59:59'
s1 = timestamp2data.data2stamp(s1)
e1 = timestamp2data.data2stamp(e1)

rate = 7 #负样本采样比例
data_cut = train_data[(train_data.action_time>=s1)&(train_data.action_time<=e1)]
tag_data(data_cut,rate)

tagdata = pd.read_csv('train_datatag.csv',index_col=0)
Union_feature_tag(tag_data)
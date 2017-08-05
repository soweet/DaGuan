# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:13:09 2017

@author: sj

统计每个类别流行度高的资讯
"""

import pandas as pd
import numpy as np

def get_subtrain():  #找到训练集中每个类别最受欢迎的新闻
    wfr = open('sub_train.txt','w')
    
    train_data = pd.read_csv('datagrand_0517/train.csv')
    candidate_news = pd.read_csv('datagrand_0517/news_info.csv')
    train_data.drop(['action_time'],axis=1,inplace=True)
    candidate_news = candidate_news.item_id
    
    #now_news = pd.merge(train_data,candidate_news,on='item_id')  太大了
    train_data.replace({'action_type':{'view':1,'deep_view':1,'comment':1,'collect':1,'share': 1}},inplace=True)
    
    n_cate = train_data.cate_id.unique()
    n_cate = sorted(list(n_cate))
    for ele in n_cate:
        print(ele)
        wfr.write(ele+': ')
        pv_cate = pd.pivot_table(train_data[train_data.cate_id==ele],index=['item_id'],aggfunc=[np.sum],values=['action_type'])
        pv_cate.columns = pv_cate.columns.levels[1]  
        pv_cate.sort_values(by='action_type',ascending=False,inplace=True)
        count = 0
        for i in range(len(pv_cate)):
            if count<5:
                if (pv_cate.index[i] in list(candidate_news)):
                    wfr.write(str(pv_cate.iloc[i].name)+','+str(pv_cate.iloc[i].action_type)+';')
                    count=count+1
            else:
                break
        wfr.write('\n')
    wfr.close()


def get_suball():  #找到所有数据中每个类别最受欢迎的新闻
    candidate_news = pd.read_csv('datagrand_0517/news_info.csv')
    candidate_news = list(candidate_news.item_id)
    
    train_data = pd.read_csv('datagrand_0517/train.csv')
    train_data.drop(['action_time'],axis=1,inplace=True)
    train_data.replace({'action_type':{'view':1,'deep_view':1,'comment':1,'collect':1,'share': 1}},inplace=True)
    
    test_data = pd.read_csv('datagrand_0517/test.csv')
    all_news = pd.read_csv('datagrand_0517/all_news_info.csv')
    all_news.drop(['timestamp'],axis=1,inplace=True)
    
    all_item = list(all_news.item_id)
    all_cate = sorted(list(all_news.cate_id.unique()))
    
    #给test中的item找到类别
    test_data['action_type']=2
    pv_test = pd.pivot_table(test_data,index=['item_id'],aggfunc=[np.sum],values=['action_type'])
    pv_test.columns = pv_test.columns.levels[1]
    pv_test_cateid = []
    #pv_test['cate_id']='0'
    for i in range(len(pv_test)):
        if (pv_test.iloc[i].name in all_item):
        #    pv_test.iloc[i].cate_id = all_news[all_news.item_id==pv_test.iloc[i].name].cate_id.values[0]
            pv_test_cateid.append(all_news[all_news.item_id==pv_test.iloc[i].name].cate_id.values[0])
        else:
            pv_test_cateid.append('0')
    pv_test['cate_id']=pv_test_cateid
    #pv_test = pd.read_csv('test_add_cate.csv')
    pv_test['item_id']=pv_test.index
    
    wfr = open('rec_use.txt','w')
    
    for ele in all_cate:
        pv_test_cate = pd.pivot_table(pv_test[pv_test.cate_id==ele],index=['item_id'],aggfunc=[np.sum],values=['action_type'])
        pv_test_cate.columns = pv_test_cate.columns.levels[1]  
        pv_test_cate['item_id']=list(pv_test_cate.index)
        pv_test_cate.sort_values(by='action_type',ascending=False,inplace=True)
        
        pv_train_cate = pd.pivot_table(train_data[train_data.cate_id==ele],index=['item_id'],aggfunc=[np.sum],values=['action_type'])
        pv_train_cate.columns = pv_train_cate.columns.levels[1]
        pv_train_cate['item_id']=list(pv_train_cate.index)
        pv_train_cate.sort_values(by='action_type',ascending=False,inplace=True)
        
        pv_all=pd.merge(pv_test_cate,pv_train_cate,on='item_id',how='outer')
        pv_all.fillna(0,inplace=True)
        
        pv_all['action_type']=pv_all['action_type_x']+pv_all['action_type_y']
    #    train_data.drop(['action_time'],axis=1,inplace=True)
        pv_all['item_id'] = pv_all['item_id'].astype('int64')
        pv_all['action_type'] = pv_all['action_type'].astype('int64')
        pv_all['action_type_x'] = pv_all['action_type_x'].astype('int64')
        pv_all['action_type_y'] = pv_all['action_type_y'].astype('int64')
        
        pv_all.sort_values(by='action_type',ascending=False,inplace=True)
        
        print(ele)
        wfr.write(ele+': ')
            
        count = 0
        for i in range(len(pv_all)):
            if count<5:
                if (pv_all.iloc[i].item_id in candidate_news):
#                    wfr.write(str(pv_all.iloc[i].item_id)+','+str(pv_all.iloc[i].action_type)+';')
                    wfr.write(str(pv_all.iloc[i].item_id)+' ')
                    count=count+1
            else:
                break
        wfr.write('\n')
    wfr.close()
        
get_subtrain()
get_suball()

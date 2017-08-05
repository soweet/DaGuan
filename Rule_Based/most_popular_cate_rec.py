# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 12:48:28 2017

@author: sj

根据不同类别中的流行度推荐
"""

import pandas as pd
import numpy as np

def read_recuse():
    fr = open('rec_use.txt')
    lines = fr.readlines()
    cate_ids = []
    item_ids = []
    for line in lines:
        ele = line.strip().split(':')
        cate_ids.append(ele[0])
        item_ids.append(ele[1].strip())
    rec_dic = dict(zip(cate_ids,item_ids))
    return rec_dic 
    
train_data = pd.read_csv('datagrand_0517/train.csv')
candidate_user = pd.read_table('datagrand_0517/candidate.txt',sep='\n',header=None,index_col=0)

train_data_replaced = train_data.replace({'action_type':{'view':1,'deep_view':2,'comment':3,'collect':3,'share':3}})
pivot_table = pd.pivot_table(train_data_replaced,index=['user_id'],columns=['cate_id'],aggfunc=[np.sum],values=['action_type'],fill_value=0)
pivot_table.columns = pivot_table.columns.levels[2]

rec_dic = read_recuse()
wfr = open('sub2.txt','w')
for u_id in list(candidate_user.index):
    cate_rec = pivot_table[pivot_table.index==u_id].idxmax(axis=1)[0]
    item_rec = rec_dic[cate_rec]
    wline = u_id+','+item_rec+'\n'
    wfr.write(wline)
wfr.close()
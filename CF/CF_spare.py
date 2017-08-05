# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 21:50:49 2017

@author: sj

用python的spare matrix 构建user-item矩阵，用SVD分解并实现推荐
"""

from scipy import sparse
import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds

train_data = pd.read_csv('datagrand_0517/train.csv')
train_data = train_data[['user_id','item_id']]
train_data = train_data[~train_data.duplicated()]

users = pd.read_csv('users.csv',index_col=0)
users = list(users.user_id)
items = pd.read_csv('items.csv',index_col=0)
items = list(items.item_id)

#rows = list(train_data.user_id)
#row = [users.index(x) for x in rows]
#cols = list(train_data.item_id)
#col = [items.index(x) for x in cols]
row = pd.read_csv('CF_row.csv',index_col=0)
col = pd.read_csv('CF_col.csv',index_col=0)
row = list(row.row_index)
col = list(col.col_index)
data = list(np.ones(len(row)))

user_item_mat = sparse.coo_matrix((data,(row,col)),shape=(len(users),len(items)))

num_main = 1000
u,s,vt = svds(user_item_mat)
s_diag_matrix=np.diag(s[0:1000])
X_pred = np.dot(np.dot(u,s_diag_matrix),vt)


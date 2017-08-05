# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 15:25:03 2017

@author: sj

得到待预测的user-item对
"""
import pandas as pd

train_data = pd.read_csv('datagrand_0517/train.csv')
#候选新闻集合
candidate_news = pd.read_csv('datagrand_0517/news_info.csv')
#选择在train_data中出现过的新闻，这样的新闻才有特征
train_items = pd.DataFrame(train_data.item_id.unique(),columns=['item_id'])
candidate_news_in_train = pd.merge(train_items,candidate_news,on='item_id')
del candidate_news,train_items

#将新闻按照列别聚合
candidate_dito_cate = dict(list(candidate_news_in_train['item_id'].groupby(candidate_news_in_train['cate_id'])))

#统计用户看过的类别
term = train_data[['user_id','cate_id']]
term =term[~term.duplicated()]
users_readed_cates = dict(list(term['cate_id'].groupby(term['user_id']))) 
del term

#将用户看过的新闻按照类别聚合
term = train_data[['user_id','item_id','cate_id']]
term =term[~term.duplicated()]
users_readed_cates_items = dict(list(term['item_id'].groupby([term['user_id'],term['cate_id']]))) 
del term

del train_data

user_100 = pd.read_csv('user_100.csv')
users = user_100['user_id']
#users=users.apply(lambda x:str(x))
n_users = len(users)

#DataFrame存储
#pre_data = pd.DataFrame()
#for i in range (n_users):
#    user_i = users[i]
#    useri_cates = list(users_readed_cates[user_i])
#    useri_pre_data = pd.DataFrame()
#    for cate_term in useri_cates:
#        toread_news = list(set(candidate_dito_cate[cate_term])-set(users_readed_cates_items[(user_i,cate_term)]))
#        if(len(toread_news)>0):
#            term = pd.DataFrame(toread_news,columns=['item_id'])
#            useri_pre_data = pd.concat([useri_pre_data,term],axis=0)
#    useri_pre_data['user_id'] = user_i
#    pre_data = pd.concat([pre_data,useri_pre_data],axis=0)
#    if(i%100==0):
#        print(i/n_users)

#字典存储
#for i in range (n_users):
#    user_i = users[i]
#    useri_cates = list(users_readed_cates[user_i])
#    user_i_predata = []
#    for cate_term in useri_cates:
#        toread_news = list(set(candidate_dito_cate[cate_term])-set(users_readed_cates_items[(user_i,cate_term)]))
#        user_i_predata = user_i_predata+toread_news
#    if(i==0):
#        pre_data = {user_i:user_i_predata}
#    else:
#        pre_data[user_i]=user_i_predata
#    if(i%100==0):
#        print(i/n_users)

#import pickle
#with open('predict_data_user100.txt','wb') as f:
#    pickle.dump(pre_data,f)


#文件存储
wfr = open('predict_data.txt','w')
for i in range (n_users):
    user_i = users[i]
    useri_cates = list(users_readed_cates[user_i])
    if(len(useri_cates)>0):
        user_i_predata = []
        for cate_term in useri_cates:
            if not(cate_term in ['6_1','1_24']):
                toread_news = list(set(candidate_dito_cate[cate_term])-set(users_readed_cates_items[(user_i,cate_term)]))
                user_i_predata = user_i_predata+toread_news
        user_i_predata = [str(x) for x in user_i_predata]
        user_i_predata = ' '.join(user_i_predata)
        wline = user_i+':'+user_i_predata+'\n'
        wfr.write(wline)
    if(i%100==0):
        print(i/n_users)
wfr.close()


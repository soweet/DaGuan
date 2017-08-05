# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 14:14:28 2017

@author: sj

时间戳和日期时间的转换，新闻时效相关信息统计
"""

import pandas as pd
import time

train_data = pd.read_csv('datagrand_0517/train.csv')
candidate_news = pd.read_csv('datagrand_0517/news_info.csv')

def stamp2data(timeStamp):
    timeArray = time.localtime(timeStamp)
    data_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return data_time
    
def data2stamp(data_time):
    stamp_time = time.mktime(time.strptime(data_time,'%Y-%m-%d %H:%M:%S'))
    return stamp_time

s1 = '2017-02-16 00:00:00'
e1 = '2017-02-16 05:00:00'
s1 = data2stamp(s1)
e1 = data2stamp(e1)

s2 = '2017-02-17 00:00:00'
e2 = '2017-02-17 05:00:00'
s2 = data2stamp(s2)
e2 = data2stamp(e2)

s3 = '2017-02-18 00:00:00'
e3 = '2017-02-18 05:00:00'
s3 = data2stamp(s3)
e3 = data2stamp(e3)

#统计新闻的时效性，查看新闻发布时间和用户阅读时间的关系
train_data_cut1 = train_data[(train_data.action_time>=s1)&(train_data.action_time<=e1)]
train_data_cut2 = train_data[(train_data.action_time>=s2)&(train_data.action_time<=e2)]
train_data_cut3 = train_data[(train_data.action_time>=s3)&(train_data.action_time<=e3)]

candidate_news_cut1 = candidate_news[(candidate_news.timestamp>=s1)&(candidate_news.timestamp<=e1)]
candidate_news_cut2 = candidate_news[(candidate_news.timestamp>=s2)&(candidate_news.timestamp<=e2)]
candidate_news_cut3 = candidate_news[(candidate_news.timestamp>=s3)&(candidate_news.timestamp<=e3)]

candidate_news_16_18 = candidate_news[(candidate_news.timestamp>=s1)&(candidate_news.timestamp<=e3)]

train1_news0 = list(set(train_data_cut1['item_id'])&set(candidate_news_16_18['item_id'])) #之前发布，且第一天阅读
train1_news1 = list(set(train_data_cut1['item_id'])&set(candidate_news_cut1['item_id'])) #第一天发布，且第一天阅读
train2_news0 = list(set(train_data_cut2['item_id'])&set(candidate_news_16_18['item_id'])) #之前发布，且第二天阅读
train2_news1 = list(set(train_data_cut2['item_id'])&set(candidate_news_cut1['item_id'])) #第一天发布，且第二天阅读
train2_news2 = list(set(train_data_cut2['item_id'])&set(candidate_news_cut2['item_id'])) #第二天发布，且第二天阅读
train3_news0 = list(set(train_data_cut3['item_id'])&set(candidate_news_16_18['item_id'])) #之前发布，且第三天阅读
train3_news1 = list(set(train_data_cut3['item_id'])&set(candidate_news_cut1['item_id'])) #第一天发布，且第三天阅读
train3_news2 = list(set(train_data_cut3['item_id'])&set(candidate_news_cut2['item_id'])) #第一天发布，且第二天阅读
train3_news3 = list(set(train_data_cut3['item_id'])&set(candidate_news_cut3['item_id'])) #第一天发布，且第三天阅读
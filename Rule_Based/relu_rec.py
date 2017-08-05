# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 07:41:46 2017

@author: sj

根据流行度推荐
"""

import pandas as pd

default_rec = '557579 558082 558788 557167 558910'  #test most popular
night_users_rec = '555684 554202 542524 555820 556700'

night_users = pd.read_csv('night_users.csv')
night_users = list(night_users.user_id.unique())

candidate_user = pd.read_table('datagrand_0517/candidate.txt',sep='\n',header=None,index_col=0)

wfr = open('submission0724nm.txt','w')
for ele in list(candidate_user.index):
    if(ele in night_users):
        wline = ele+','+night_users_rec+'\n'
    else:
        wline = ele+','+default_rec+'\n'
    wfr.write(wline)
wfr.close()
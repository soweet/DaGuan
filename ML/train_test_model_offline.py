# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 16:03:13 2017

@author: sj

训练模型，测试模型
"""
import pandas as pd
#from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.grid_search import GridSearchCV
from sklearn import metrics

train = pd.read_csv('feature_tag/train_data.csv',index_col=0)
train_y = train['tag']
train_x = train.drop(['item_id','tag','user_id','cate_id'],axis=1)

#ss = StandardScaler()
#train_x = ss.fit_transform(train_x)

RF = RandomForestClassifier(n_estimators=10,max_depth=10,oob_score=True)
RF.fit(train_x,train_y)
print(RF.oob_score_)

y_predprob = RF.predict_proba(train_x)
y_pred = y_predprob[:,-1]
print("AUC Score (Train):%f"%metrics.roc_auc_score(train_y,y_pred))

#GB = GradientBoostingClassifier(n_estimators=100)
#GB.fit(train_x,train_y)
#y_pred = GB.predict(train_x)
#y_predprob = GB.predict_proba(train_x)
#print('Accuracy:%4f'%metrics.accuracy_score(train_y,y_pred))
#print("AUC Score (Train):%f"%metrics.roc_auc_score(train_y,y_predprob[:,-1]))
#save model
from sklearn.externals import joblib
joblib.dump(RF,'save_model/RF.pkl')
#joblib.dump(RF,'save_model/RF.pkl')


def Para():
    #=============================调参
    print('=====GridSearch n_estimators paramters=====')
    #对n_estimators进行网格搜索
    param_test1 = {'n_estimators':[x for x in range(40, 61, 10)]}
    gsearch1 = GridSearchCV(estimator=RandomForestClassifier(min_samples_split=100,min_samples_leaf=20,max_depth=8,max_features='sqrt',random_state=10),param_grid=[param_test1],scoring='roc_auc',cv=5)
    gsearch1.fit(train_x,train_y)
    gsearch1.grid_scores_,gsearch1.best_params_,gsearch1.best_score_
    
    n_estimators_best = gsearch1.best_params_['n_estimators']
    
    print('=====GridSearch max_depth,min_samples_split paramters=====')
    param_test2 = {'max_depth':[x for x in range(5,16, 5)],'min_samples_split':[x for x in range(10,70,20)]}
    #param_test2 = {'min_samples_split':[x for x in range(2,11,4)]}
    gsearch2 = GridSearchCV(estimator=RandomForestClassifier(n_estimators= 60,min_samples_leaf=20,max_depth=10,max_features='sqrt',random_state=10),param_grid=[param_test2],scoring='roc_auc',iid=False,cv=5)
    gsearch2.fit(train_x,train_y)
    gsearch2.grid_scores_,gsearch2.best_params_,gsearch2.best_score_
    

def test():
    test_data = pd.read_csv('feature_tag/train_test_/test_data.csv',index_col=0)
    test_y = test_data['tag']
    test_x = test_data.drop(['item_id','tag','user_id','cate_id'],axis=1)
    
    RFclassifier = joblib.load('save_model/RF.pkl')
    y_pred = RFclassifier.predict(test_x)
    print('Accuracy:%4f'%metrics.accuracy_score(test_y,y_pred))
    
    GBclassifier = joblib.load('save_model/GB.pkl')
    y_pred = GBclassifier.predict(test_x)
    print('Accuracy:%4f'%metrics.accuracy_score(test_y,y_pred))

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 19:44:10 2019

@author: Akash
"""

import numpy as np 
import pandas as pd 
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold   #For K-fold cross validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as mlt
import seaborn as sns
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

apps=pd.read_csv('C:\\Users\\Akash\\Desktop\\8bitStore\\apps.csv',encoding = "ISO-8859-1")
#print(apps.head())


apps['App'] = apps['App'].str.replace('?','')
apps['App'] = apps['App'].str.replace('(','')
apps['App'] = apps['App'].str.replace(')','')
apps['Installs'] = apps['Installs'].str.replace(',','')
apps=apps.drop([3750,6333,9306],axis=0)
#apps.replace(['?'],[''])
#print(apps)
#print(apps.iloc[3434])

#length=len(apps)
#for i in range(1,length):
#    if apps.iloc[i]['Rating']== "NaN":
#        apps=apps.drop([i],inplace=True)
#        
#
#print(apps.iloc[23])   

apps=apps[apps.Rating.notnull()]
#print(apps.iloc[120])
#print(apps)
apps=apps.drop([10472],axis=0)
###############################################################################

review=pd.read_csv('C:\\Users\\Akash\\Desktop\\8bitStore\\review.csv',encoding = "ISO-8859-1")
#print(review)


#print(review)
for i in range(200,240):
#    print(review.iloc[i])
    review=review.drop([i],axis=0)

#print(review.iloc[330])
for i in range(1020,1098):
#    print(review.iloc[i])
    review=review.drop([i],axis=0)
    
for i in range(33545,33585):
#    print(review.iloc[i])
    review=review.drop([i],axis=0)
    
'''for i in range(51024,51064):
#    print(review.iloc[i])
    review=review.drop([i],axis=0)'''
    
for i in range(51024,51064):
#    print(review.iloc[i])
    review=review.drop([i],axis=0)

#review['App'] = review['App'].str.replace('â€“','')'''
#print(review.iloc[50906])
review=review[review.Translated_Review.notnull()]
#print(review)
###############################################################################

apps['Installs'] = apps['Installs'].str.replace('+','')
#print(apps.iloc[2])


########################## REQ 1 ##############################################
'''
cat = apps.drop_duplicates(subset='Category', keep='first')

category=[]
for i in cat['Category']:
    category.append(i)
#print(category)
    

installs_sum=[]
for i in category:
    sum=0
    for index,row in apps.iterrows():
        if i==row['Category']:
            sum=sum+int(row['Installs'])
    installs_sum.append(sum)   

#print(installs_sum)

total_sum=0
for i in  installs_sum:
    total_sum=total_sum+i
       
#print(total_sum)   
'''
###############################################################################   


########################## REQ 2 ##############################################
range1=0
range2=0
range3=0
range4=0
range5=0
r=0
for index,rows in apps.iterrows():
    if int(rows['Installs']) >= 10000 and int(rows['Installs']) <50000:
        range1+=1
    elif int(rows['Installs']) >= 50000 and int(rows['Installs']) <150000:
        range2+=1
    elif int(rows['Installs']) >= 150000 and int(rows['Installs']) <500000:
        range3+=1
    elif int(rows['Installs']) >= 500000 and int(rows['Installs']) <5000000:
        range4+=1
    elif int(rows['Installs']) >= 5000000:
        range5+=1
    elif int(rows['Installs']) < 10000:
        r+=1

print(range1)
print(range2)
print(range3)
print(range4)
print(range5)  
print(r) 
        


























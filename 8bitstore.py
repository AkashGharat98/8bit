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

import matplotlib
matplotlib.rcParams['axes.labelsize']=14
matplotlib.rcParams['xtick.labelsize']=12
matplotlib.rcParams['ytick.labelsize']=12
matplotlib.rcParams['text.color']='k'

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import statsmodels.api as sm
import seaborn as sns
from datetime import datetime
import time
from warnings import simplefilter

# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)


###############################################################################

apps=pd.read_csv('C:\\Users\\Akash\\Desktop\\8bitStore\\apps.csv',encoding = "ISO-8859-1")
apps['Last Updated'] = apps['Last Updated'].str.replace(',','')
apps['Last Updated'] = apps['Last Updated'].str.replace('January','Jan')
apps['Last Updated'] = apps['Last Updated'].str.replace('February','Feb')
apps['Last Updated'] = apps['Last Updated'].str.replace('March','Mar')
apps['Last Updated'] = apps['Last Updated'].str.replace('April','Apr')
apps['Last Updated'] = apps['Last Updated'].str.replace('May','May')
apps['Last Updated'] = apps['Last Updated'].str.replace('June','Jun')
apps['Last Updated'] = apps['Last Updated'].str.replace('July','Jul')
apps['Last Updated'] = apps['Last Updated'].str.replace('August','Aug')
apps['Last Updated'] = apps['Last Updated'].str.replace('September','Sep')
apps['Last Updated'] = apps['Last Updated'].str.replace('October','Oct')
apps['Last Updated'] = apps['Last Updated'].str.replace('November','Nov')
apps['Last Updated'] = apps['Last Updated'].str.replace('December','Dec')
apps=apps.drop([10472],axis=0)
apps['App'] = apps['App'].str.replace('?','')
apps['App'] = apps['App'].str.replace('(','')
apps['App'] = apps['App'].str.replace(')','')
apps['Installs'] = apps['Installs'].str.replace(',','')
apps=apps.drop([3750,6333,9306],axis=0)
apps=apps[apps.Rating.notnull()]
apps['Installs'] = apps['Installs'].str.replace('+','')


date=apps['Last Updated']
d=date.values.tolist()  #temp variable

x=[]     #temp variable
for i in d:
        conv=time.strptime(i,"%b %d %Y")
        x.append(time.strftime("%Y-%m-%d",conv))

apps['Last Updated']=x

###############################################################################
'''
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
    
for i in range(51024,51064):
#    print(review.iloc[i])
    review=review.drop([i],axis=0)

#review['App'] = review['App'].str.replace('â€“','')
#print(review.iloc[50906])
review=review[review.Translated_Review.notnull()]
#print(review)
print(review.head())
'''
###############################################################################


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
'''
range1=0
range2=0
range3=0
range4=0
range5=0

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

print(range1)
print(range2)
print(range3)
print(range4)
print(range5)  
'''
###############################################################################   


########################## REQ 3 ##############################################        
'''
avg_cat_download=[]
cat_count=[]

cat = apps.drop_duplicates(subset='Category', keep='first')

category=[]
for i in cat['Category']:
    category.append(i)
print(category)
    

installs_sum=[]
for i in category:
    sum=0
    count=0
    for index,row in apps.iterrows():
        if i==row['Category']:
            sum=sum+int(row['Installs'])
            count+=1
    installs_sum.append(sum)
    cat_count.append(count)

max_cat_download=category[installs_sum.index(max(installs_sum))]
maximum=max(installs_sum)
min_cat_download=category[installs_sum.index(min(installs_sum))]
minimum=min(installs_sum)
#print(min_cat_download)

for i in range(0,33):#length of categories and cat_count
    if float(installs_sum[i]/cat_count[i]) >= 250000:
        avg_cat_download.append(category[i])
    
#print(avg_cat_download)
'''
###############################################################################   


########################## REQ 4 ##############################################
'''
cat = apps.drop_duplicates(subset='Category', keep='first')
category=[]
for i in cat['Category']:
    category.append(i)
#print(category)
   
rating_sum=[]
for i in category:
    sum=0
    counter=0
    avg=0
    for index,row in apps.iterrows():
        if i==row['Category']:
            counter+=1
            sum=sum+int(row['Rating'])
    avg=sum/counter
    rating_sum.append(round(avg,2))  

highest_value = max(rating_sum)
index = rating_sum.index(highest_value)
print(category[index])
'''
###############################################################################   


########################## REQ 5 ##############################################
'''
category=apps.loc[apps['Category']=='ART_AND_DESIGN']
#print(category)

cols=['App','Category','Rating','Reviews','Size','Type','Price','Content Rating','Genres','Current Ver','Android Ver']
category.drop(cols,axis=1,inplace=True)

category=category.sort_values('Last Updated')
x=[]
for i in category['Installs']:
    x.append(int(i))
    
category['Installs']=x   
   
    
category['Last Updated']=pd.to_datetime(category['Last Updated'])
#print(category.dtypes)
category=category.set_index('Last Updated')
print(category.head())

print(category.plot(grid=True))


decomposition=sm.tsa.seasonal_decompose(category,model="additive",freq=30)
fig=decomposition.plot()
from pylab import rcParams
rcParams['figure.figsize']=8,4
plt.show()
'''
###############################################################################   


########################## REQ 8 ##############################################
apps['Last Updated'] = pd.to_datetime(apps['Last Updated'])
apps['year'] = apps['Last Updated'].dt.year
print(apps['year'].tail())
















###############################################################################   


########################## REQ 14 ##############################################
'''temp = review.drop_duplicates(subset='App', keep='first')
app=temp['App']
app_str="10 Best Foods for You"
positive=[]
negative=[]
neutral=[]

rev=review.loc[review['App']==app_str]
#print(rev)
pos=rev.loc[rev['Sentiment']=="Positive"]
positive=pos['Translated_Review']
print(positive)

neu=rev.loc[rev['Sentiment']=="Neutral"]
neutral=neu['Translated_Review']
print(neutral)

neg=rev.loc[rev['Sentiment']=="Negative"]
negative=neg['Translated_Review']
print(negative)
'''
###############################################################################   


########################## REQ 14 ##############################################


# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 19:11:44 2019

@author: Akash
"""

from tkinter import *
from tkinter import messagebox
import re, pymysql
import numpy as np 
import pandas as pd 
import time
from datetime import date
from pylab import rcParams
from textblob import TextBlob
from sklearn.linear_model import LinearRegression

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.rcParams['axes.labelsize']=14
matplotlib.rcParams['xtick.labelsize']=12
matplotlib.rcParams['ytick.labelsize']=12
matplotlib.rcParams['text.color']='k'

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

import statsmodels.api as sm
#import seaborn as sns
#from warnings import simplefilter

#Choose theme of window
color1 ='#CD3333'#TITLE COLOR
bgcolor_middle = '#5F9EA0'#BODY COLOR
color3 = '#00C957'#Button Color
text_color ='white'

#Fonts
title_font="Calibri"
body_font="Open Sans"

def adjustWindow(window):
    ws = window.winfo_screenwidth() # width of the screen
    hs = window.winfo_screenheight() # height of the screen
    w = ws # width for the window size
    h = hs# height for the window size
    x = (ws/2) - (w/2) # calculate x and y coordinates for the Tk window
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w-15, h-40, x, y)) # set the dimensions of the screen and where it is placed
    window.resizable(False, False) # disabling the resize option for the window
    window.configure(background='white')
    
def data_wrangling():
    global apps,review
    #DATA WRANGLING
    #Taking data from database and storing in csv file
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore",use_unicode=True,charset="utf8")
    cursor = conn.cursor()
    query = "Select * from apps"
    results = pd.read_sql_query(query,conn)
    results.to_csv('C:\\Users\\Akash\\Desktop\\8bitStore\\apps.csv',index=False)
    conn.commit()
    conn.close()

    #Data wrangling of apps
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
    
    
 
    apps['App'] = apps['App'].str.replace('?','')
    apps['App'] = apps['App'].str.replace('(','')
    apps['App'] = apps['App'].str.replace(')','')
    apps=apps.drop([3750,6333,9306,10472],axis=0)

    apps=apps[apps.Rating.notnull()]
    
    apps['Installs'] = apps['Installs'].str.replace(',','')
    apps['Installs'] = apps['Installs'].str.replace('+','')
    
    date=apps['Last Updated']
    d=date.values.tolist()  #temp variable
    
    x=[]     #temp variable
    for i in d:
        conv=time.strptime(i,"%b %d %Y")
        x.append(time.strftime("%Y-%m-%d",conv))

    apps['Last Updated']=x
    
    apps['Last Updated'] = pd.to_datetime(apps['Last Updated'])
    apps['year'] = apps['Last Updated'].dt.year
    apps['month'] = apps['Last Updated'].dt.month
    
    #Taking data from database and storing in csv file
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="8bitstore",use_unicode=True,charset="utf8")
    cursor = conn.cursor()
    query = "Select * from reviews"
    results = pd.read_sql_query(query,conn)
    results.to_csv('C:\\Users\\Akash\\Desktop\\8bitStore\\review.csv',index=False)
    conn.commit()
    conn.close()

    #Data wrangling of reviews
    review=pd.read_csv('C:\\Users\\Akash\\Desktop\\8bitStore\\review.csv',encoding = "ISO-8859-1")

    for i in range(200,240):
        review=review.drop([i],axis=0)

    for i in range(1020,1098):
        review=review.drop([i],axis=0)
    
    for i in range(33545,33585):
        review=review.drop([i],axis=0)
       
    for i in range(51024,51064):
        review=review.drop([i],axis=0)

    review=review[review.Translated_Review.notnull()]
        
def initialise():
    global cat_inst,category,installs_sum,installs,types,genres,contentrating
    cat_inst={}
    cat = apps.drop_duplicates(subset='Category', keep='first')
    category=[]
    for i in cat['Category']:
        category.append(i)
        
    inst = apps.drop_duplicates(subset='Installs', keep='first')
    installs=[]
    for i in inst['Installs']:
        installs.append(int(i))
    installs.sort()
    for i in range(0,len(installs)):
        installs[i]=str(installs[i])
    
    typ = apps.drop_duplicates(subset='Type', keep='first')
    types=[]
    for i in typ['Type']:
        types.append(i)
        
    genr = apps.drop_duplicates(subset='Genres', keep='first')
    genres=[]
    for i in genr['Genres']:
        genres.append(i)
        
    contrat = apps.drop_duplicates(subset='Content Rating', keep='first')
    contentrating=[]
    for i in contrat['Content Rating']:
        contentrating.append(i)
        
    installs_sum=[]
    for i in category:
        sum=0
        for index,row in apps.iterrows():
            if i==row['Category']:
                sum=sum+int(row['Installs'])
        installs_sum.append(sum)
    total_sum=0
    for i in  installs_sum:
        total_sum=total_sum+i
    
    i=0
    while(i<len(category)):
        cat_inst[category[i]]=installs_sum[i]
        i=i+1 
        
        
def rel_polarity_subjectivity(x1,y1):
    x=review['Sentiment_Polarity'].values.reshape(-1,1)
    y=review['Sentiment_Subjectivity'].values.reshape(-1,1)
    reg=LinearRegression()
    reg.fit(x,y)
    
    
    m=round(reg.coef_[0][0],5)
    c=round(reg.intercept_[0],5)
    result="Y = "+str(m)+"X + "+str(c)
#    print(result)
    #print("The linear model is : Y = {:.5}X + {:.5}".format(reg.coef_[0][0],reg.intercept_[0]))
    
    
    predictions=reg.predict(x)
    
    f=plt.figure(figsize=(8,6),dpi=70)
    ax3 = f.add_subplot(111)
    
    
    
#    plt.figure(figsize=(6,4))
    ax3.scatter(review['Sentiment_Polarity'],review['Sentiment_Subjectivity'],c='blue',alpha=0.1)
    ax3.plot(review['Sentiment_Polarity'],predictions,c='red',linewidth=2)
    ax3.set_ylabel("Sentiment Subjectivity")
    ax3.set_xlabel("Sentiment Polarity")
    
    Label(screen5, text=result,font=(body_font, 15, 'bold'), fg=text_color, bg=bgcolor_middle,width=40,anchor=W).place(x=x1+20,y=y1+80)
#    plt.show()
    canvas = FigureCanvasTkAgg(f, master=screen5)
    canvas.get_tk_widget().place(x=x1+20,y=y1+120)
    canvas.draw()



def size_installs(x1,y1):
    temp = review.drop_duplicates(subset='App', keep='first')
    app=temp['App'].tolist()
    #print(len(app))
    
    #apps['Size'] = apps['Size'].str.replace('M','')
    
    
    indexNames = apps[ apps['Size'] == "Varies with device" ].index
     
    # Delete these row indexes from dataFrame
    apps.drop(indexNames , inplace=True)
    
    
    temp=apps['Size'].tolist()
    
    size=[]
    for i in temp:
        if 'M' in i:
            x=i.replace("M","")
            size.append(float(x)*1024)
        elif 'k' in i:
            x=i.replace("k","")
            size.append(float(x))
            
    apps['Size']=size
    
    list_apps=apps['Size'].tolist()
    #print(max(list_apps))
    
    
    sum1=0
    sum2=0
    sum3=0
    sum4=0
    sum5=0
    sum6=0
    
    #print(apps['Installs'].dtype)
    
    for index,row in apps.iterrows():
        if row['Size']>=0 and row['Size']<20000:
            sum1+=int(row['Installs'])
        elif row['Size']>=20000 and row['Size']<40000:
            sum2+=int(row['Installs'])
        elif row['Size']>=40000 and row['Size']<60000:
            sum3+=int(row['Installs'])
        elif row['Size']>=60000 and row['Size']<80000:
            sum4+=int(row['Installs'])
        elif row['Size']>=80000 and row['Size']<100000:
            sum5+=int(row['Installs'])
        elif row['Size']>=100000 and row['Size']<120000:
            sum6+=int(row['Installs'])
    
    sum1/=1000000
    sum2/=1000000
    sum3/=1000000
    sum4/=1000000
    sum5/=1000000
    sum6/=1000000
    
    list_installs=[]
    list_installs.append(sum1)
    list_installs.append(sum2)
    list_installs.append(sum3)
    list_installs.append(sum4)
    list_installs.append(sum5)
    list_installs.append(sum6)
    
#    print(list_installs)
    
    
    activities = ['0-20 Mb', '20-40 Mb', '40-60 Mb', '60-80 Mb','80-100 Mb','100-120 Mb']
    colors = ['red', 'yellow', 'green', 'blue','orange','pink'] 
      
    
    f=plt.figure(figsize=(8,6),dpi=70)
    ax4 = f.add_subplot(111)
    
    # plotting the pie chart 
    ax4.pie(list_installs, labels = activities, colors=colors,  
            startangle=0, shadow = True,  
            radius = 1.2, autopct = '%1.1f%%') 
      
    # plotting legend 
    #plt.legend() 
    
    # showing the plot 
#    plt.show()
    
    canvas = FigureCanvasTkAgg(f, master=screen5)
    canvas.get_tk_widget().place(x=x1+20,y=y1+120)
    canvas.draw()
     


def reviewsScreen():
    global screen5
    screen5=Tk()
#    screen5 = Toplevel(screen)
#    search_item = StringVar()
    
    screen5.title("HOME")
    adjustWindow(screen5)
    
    Label(screen5, text="", width='500', height="20", bg=color1).pack() 
    Label(screen5, text="8-BIT ANALYSIS",font=(title_font, 70, 'bold'), fg='white', bg=color1).place(x=455,y=10)
    Button(screen5, text='BACK', width=8, font=(body_font, 13, 'bold'), bg=color3, fg=text_color, command=screen5.destroy).place(x=1080, y=55)

    photo1 = PhotoImage(file="C:\\Users\\Akash\\Desktop\\8bitStore\\review.png")
    label = Label(screen5,borderwidth=0, image=photo1)
    label.place(x=0, y=152)
    
    
    
    x1=30# Change these parameters 
    y1=170# to shift the whole below section
    Label(screen5, text="", width=76, height=40, bg=bgcolor_middle).place(x=x1,y=y1)
    Label(screen5, text="Relation between Sentiment Polarity \n and Sentiment Subjectivity",font=(body_font, 20, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+20,y=y1+5)
    rel_polarity_subjectivity(x1,y1)
    
    
    x1=600# Change these parameters 
    y1=170# to shift the whole below section
    Label(screen5, text="", width=76, height=40, bg=bgcolor_middle).place(x=x1,y=y1)
    Label(screen5, text="Pie Chart of Size of the app \n and no. of downloads",font=(body_font, 20, 'bold'), fg=text_color, bg=bgcolor_middle).place(x=x1+20,y=y1+5)
    size_installs(x1,y1) 
    
    
    
    
    
    
    
    screen5.mainloop()
    
data_wrangling()
initialise()
reviewsScreen()
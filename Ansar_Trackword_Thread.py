'''
In this scrip, we clean data in order to get best result based on jackard Index method

'''

from __future__ import division
import numpy as np
import timeit
start = timeit.default_timer()
import pandas as pd
from datetime import datetime, timedelta
import networkx as nx 
import re

colnames = ['MessageID','ThreadID','ThreadName','MemberID','MemberName','Message','P_Year',
            'P_Month','P_Day','P_Date','ThreadFirstMessageID']
df = pd.read_csv("Ansar1.txt", delimiter="\t",
                 names=['MessageID','ThreadID','ThreadName','MemberID','MemberName','Message','P_Year','P_Month',
                        'P_Day','P_Date','ThreadFirstMessageID'])

sort_by_date = df.sort_values(['P_Date'], ascending=True)
2
Mindate='2008-12-08'
Maxdate='2010-04-20'
Sorted_filtered=sort_by_date[(sort_by_date['P_Date'] >= Mindate) & (sort_by_date['P_Date'] <= Maxdate)]
Date = list(Sorted_filtered['P_Date'])
Date = [str(s).replace(' 00:00:00.000', '') for s in Date]

MessageID = list(Sorted_filtered['MessageID'])
ThreadID = list(Sorted_filtered['ThreadID'])
ThreadName = list(Sorted_filtered['ThreadName'])
MemberID = list(Sorted_filtered['MemberID'])
MemberName = list(Sorted_filtered['MemberName'])
Message = list(Sorted_filtered['Message'])


#==============================================================
#################################################################
### import most frequently used words

MostFrequentlyUsedWords = open('1-1000.txt','r')
Most_Frequently_usedWords = []
for line in MostFrequentlyUsedWords:
    Most_Frequently_usedWords.extend([i for i in line.split()])

Most_Frequently_usedWords_capitalized = []
for item in Most_Frequently_usedWords:
    A = item.capitalize()
    Most_Frequently_usedWords_capitalized.append(A)

#print(Most_Frequently_usedWords_capitalized)
    

AnsarForumsFrequentwords1 = open('Ansar_frequently_used_words_1.txt','r')
FrequentwordsAnsar1 = []
for line in AnsarForumsFrequentwords1:
    FrequentwordsAnsar1.extend([i for i in line.split()])


AnsarForumsFrequentwords2= open('Ansar_frequently_used_words_2.txt','r')
FrequentwordsAnsar2 = []
for line in AnsarForumsFrequentwords2:
    FrequentwordsAnsar2.extend([i for i in line.split()])



#===========================================================make cleaning message list
Message=['missing' if x is np.nan else x for x in Message]  

########################################################################################################
## Cleaning the messages from most frequently used words, numbers, meaningless words
# Make Lists of words for every Message but remove above words that are most common words in daily conversations

wordList_ = {}
for i in range(len(Message)):
    wordList_[i] = re.sub("[^\w]", " ",  Message[i]).split()
    wordList_[i] = [x for x in wordList_[i] if x not in FrequentwordsAnsar1]
    wordList_[i] = [x for x in wordList_[i] if x not in FrequentwordsAnsar2]
    wordList_[i] = [x for x in wordList_[i] if x not in Most_Frequently_usedWords]
    wordList_[i] = [x for x in wordList_[i] if x not in Most_Frequently_usedWords_capitalized]

GOD = ["God","god","GOD","CIA","FBI"]
numbers_={}
for i in range(len(Message)):
    One_letter_words = [word for word in wordList_[i] if len(word) == 1]    
    Two_letter_words = [word for word in wordList_[i] if len(word) == 2]
    Three_letter_words = [word for word in wordList_[i] if len(word) == 3]
    Three_letter_words2 = [word for word in Three_letter_words if word not in GOD]
    numbers_[i] = [s for s in wordList_[i] if s.isdigit()]
    wordList_[i] = [x for x in wordList_[i] if x not in One_letter_words]
    wordList_[i] = [x for x in wordList_[i] if x not in Two_letter_words]    
    wordList_[i] = [x for x in wordList_[i] if x not in Three_letter_words2]
    wordList_[i] = [x for x in wordList_[i] if x not in numbers_[i]]

###################################################Cleaning is finished in above

#print(wordList_ )
vals=[]
vals = list(wordList_.values())
#print(vals)

#===============================================set Id to each node in each month for visualization
Dic_of_Date_Member_Thread = {}
Dic_of_Date_Thread_Message={}
for i in range(len(Date)):
    D = datetime.strptime(Date[i],"%Y-%m-%d")
    if D not in Dic_of_Date_Member_Thread:
        Dic_of_Date_Member_Thread[D] = {}
        Dic_of_Date_Thread_Message[D]={}
    if ThreadID[i] not in Dic_of_Date_Member_Thread[D]:
        Dic_of_Date_Member_Thread[D][ThreadID[i]] = []
        Dic_of_Date_Thread_Message[D][ThreadID[i]] = []
    Dic_of_Date_Member_Thread[D][ThreadID[i]].append(MemberID[i])
    Dic_of_Date_Thread_Message[D][ThreadID[i]].append(vals[i])
#print(Node_Date)



Date_Thread_Members={}
Date_Thread_Messages={}

date1 = datetime.strptime(Date[0],"%Y-%m-%d") 

for x in range(0,len(Date)):
     
    date2 = date1+timedelta(days=31)
    Time=date1.strftime('%Y-%m-%d')
    Date_Thread_Members[Time]= []
    Date_Thread_Messages[Time]= []
    for j in range(len(Dic_of_Date_Member_Thread)):
        
        if  date1 <= Dic_of_Date_Member_Thread.keys()[j] < date2:
            
           
           
            Date_Thread_Members[Time].append(Dic_of_Date_Member_Thread.values()[j])
            Date_Thread_Messages[Time].append(Dic_of_Date_Thread_Message.values()[j])
       
    date1 = date1+timedelta(days=15)
 

#===========================================sort dictionary
from collections import OrderedDict  
Date_Thread_Members= OrderedDict(sorted(Date_Thread_Members.items(), key=lambda t: t[0]))  
Date_Thread_Messages= OrderedDict(sorted( Date_Thread_Messages.items(), key=lambda t: t[0]))    
#print(Date_Thread_Messages)
       
#===================================================create edges between thread if common member 
#---------------------------------------------------comment on at least 2 same thread

select_words=['Allah','killed','Taliban','attack','bomb','military','Iraq']

import matplotlib.pyplot as plt
for i in range(len(Date_Thread_Members)):
    G = nx.Graph()
    Date_Edges=[]
    Date_Nodes=[]
    value=[]
    for item in Date_Thread_Members.values()[i]:
        for k in range(len(item)):
            for l in range(k+1,len(item)):
                  
                if len(set(item.values()[k]) & set(item.values()[l]))>=2:
                    
                    tuple_edge=(item.keys()[k],item.keys()[l])
                    Date_Edges.append(tuple_edge)
                    
                    Date_Nodes.append((item.keys()[k]))
                    Date_Nodes.append((item.keys()[l])) 
                    
    G.add_edges_from(Date_Edges)
    Date_Nodes=list(set(Date_Nodes))
    
    
    for item in Date_Thread_Messages.values()[i]:
        #print(item)
        for node in Date_Nodes:
                    
            for kk in range(len(item)):
                if node==item.keys()[kk]:
                   #print(item.values()[kk])
                   if len(set(item.values()[kk][0]) & set(select_words))>0:
                       dd=(item.keys()[kk],len(set(item.values()[kk][0]) & set(select_words)))
                       value.append(dd)
    print(dict((x, y) for x, y in value))
    val_map =dict((x, y) for x, y in value) 

    values = [val_map.get(node, 0.25) for node in G.nodes()]
    pos=nx.random_layout(G)
    nx.draw(G,pos, cmap=plt.get_cmap('jet'), node_color=values,with_labels=True,font_size=6,font_weight='bold',font_color='w')
    plt.show()
   

         






    
   



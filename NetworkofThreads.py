
'''
This script calculate the network between threads in each duing 30 days, the shift of time step starts from the first comment  and
connection between threads happens during 30 days then time step shifts slowly to the second comment and calculation is done
for the second 30 days, and so on

'''


#===============================================================================================Read Data
import timeit
start = timeit.default_timer()
import pandas as pd
from datetime import datetime, timedelta


df = pd.read_csv('Gawaher-Islamic-Discussion.csv',delimiter=',')
sort_df= df.sort_values(['Date'], ascending=True)

Message = list(sort_df['Message'])
MemberID = list(sort_df['Member'])
ThreadID= list(sort_df['Thread'])
Date = list(sort_df['Date'])
Date_list=[]
    
for date in Date:   
    if ', 20' in date:
        d = datetime.strptime( date , '%B %d, %Y')
        day_string = d.strftime('%Y-%m-%d')
        Date_list.append(day_string)  
    else:
        d = datetime.strptime( date , '%B %d')
        day_string = d.strftime('2018-%m-%d')
        Date_list.append(day_string)

#===============================================set Id to each node in each month for visualization
Dic_of_Date_Member_Thread = {}

for i in range(len(Date)):
    D = datetime.strptime(Date[i],"%Y-%m-%d")
    if D not in Dic_of_Date_Member_Thread:
        Dic_of_Date_Member_Thread[D] = {}
    if ThreadID[i] not in Dic_of_Date_Member_Thread[D]:
        Dic_of_Date_Member_Thread[D][ThreadID[i]] = []
    
    Dic_of_Date_Member_Thread[D][ThreadID[i]].append(MemberID[i])




Date_Thread_Members={}
date1= datetime.strptime(Date_list[0],"%Y-%m-%d")
for x in range(0,250):
    Time=date1.strftime('%Y-%m-%d')
    date2 = date1+timedelta(days=31)
    date2=datetime.strftime(date2, "%Y-%m-%d")
    Date_Members_Threads[Time]= []

    for j in range(len(Dic_of_Date_Member_Thread)):
        
        if  Time <= Dic_of_Date_Member_Thread.keys()[j] < date2:
            
            
           
            Date_Thread_Members[Time].append(Dic_of_Date_Member_Thread.values()[j])
            
  

#===========================================sort dictionary by time
from collections import OrderedDict  
Date_Thread_Members= OrderedDict(sorted(Date_Thread_Members.items(), key=lambda t: t[0]))   

#===================================================create edges between thread if common members comment on at least 2 same threads 
Date_Edges={}
Date_Nodes={}

for i in range(len(Date_Thread_Members)):
    Date_Edges[Date_Thread_Members.keys()[i]]=[]
    Date_Nodes[Date_Thread_Members.keys()[i]]=[]
    for item in Date_Thread_Members.values()[i]:
        for k in range(len(item)):
            for l in range(k+1,len(item)):
                if len(set(item.values()[k]) & set(item.values()[l]))>=2:
                    
                    Date_Edges[Date_Thread_Members.keys()[i]].append([item.keys()[k],item.keys()[l],len(set(item.values()[k]) & set(item.values()[l]))])
                    
                    Date_Nodes[Date_Thread_Members.keys()[i]].append((item.keys()[k]))
                    Date_Nodes[Date_Thread_Members.keys()[i]].append((item.keys()[l])) 


#================================remove keys with empty value from edgelist and node list
Date_Edges=dict((k, v) for k, v in Date_Edges.iteritems() if v)
Date_Nodes=dict((k, v) for k, v in Date_Nodes.iteritems() if v)
#============================================= make graph node list for load in gephi
vals =list(Date_Nodes.values())
keyno= list(Date_Nodes.keys())

VALUES=list(Date_Edges.values())
KEYS=Date_Edges.keys()

IDnode=0
gephinode=[]
gephiEdge=[]

for i in range(0,len(keyno)):   #loop on all key
       
    uniq = list(set(vals[i]))
        
    for j in range(0,len(uniq)):
        
            qq=(IDnode,uniq[j],keyno[i])
            gephinode.append(qq)
            
            IDnode+=1

#====================================================the date is important for labels in Gephi

for ii in range(0,len(KEYS)):   #loop on all key
        SET=[] 
        UniqEdge=VALUES[ii]
        for kkk in range(0,len(gephinode)):
            if (gephinode[kkk][2]==KEYS[ii]):
                zz=(gephinode[kkk][0],gephinode[kkk][1])
                SET.append(zz)
       
        for kk in range(0,len(UniqEdge)):
           
            ss=[x[1] for x in SET].index(UniqEdge[kk][0])
            tt=[x[1] for x in SET].index(UniqEdge[kk][1])
            IDaa=SET[ss][0]   #IDnode
            IDbb=SET[tt][0]  #IDnode
            ww=(IDaa,IDbb,UniqEdge[kk][2],KEYS[ii])
            gephiEdge.append(ww)

#=============================================write csv file 
import csv

with open('Gawaher-NodethreadNetwork_EachMonth.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['Id','Label','Timestamp'])
    for row in gephinode:
        csv_out.writerow(row)

with open('Gawaher-EdgethraedNetwork_EachMonth.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['Source','Target','Weight','Timestamp'])
    for row in gephiEdge:
        csv_out.writerow(row) 
          
#============================================================              






    
   



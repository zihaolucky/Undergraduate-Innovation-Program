import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from pylab import *



cx = sqlite3.connect("followees_info.db")
cx2 = sqlite3.connect("user_info.db")
cu = cx.cursor()
cu2 = cx2.cursor()

# cu.execute("create table user_info (user_id text primary key,followers integer, asks integer, answers integer, goods integer)")





def transform(name):
    line = f.readline()
    while line:
        line = f.readline()
        line.strip()
        data = line.split(',')
        try:
            cx.execute("insert into user_info values (?,?,?,?,?)",data)
            print data
            cx.commit()
        except:
            print "existed.\n"
    
    f.close()

name_list =['allenzhang','baiya','chen-hao-84','commando','fenng','gongjun','hi-id',
'jin-chen-yu','jixin','junyu','kentzhu','linan','raymond-wang','shek']

for name in name_list:
    print name
    f = open(name + ".txt")
    transform(name)


# cu.execute("select COUNT(user_id)from user_info where asks>0")
# result = cu.fetchall()[0][0]

"""
对数图

asks = []
for i in range(200):
    cu.execute("select COUNT(user_id) from user_info where asks="+str(i)+"")
    a = cu.fetchall()[0][0]
    asks.append(a)

asks2 = []
for i in range(200):
    cu2.execute("select COUNT(user_id) from user_info where asks="+str(i)+"")
    a = cu2.fetchall()[0][0]
    asks2.append(a)
    
----------
answers = []
for i in range(200):
    cu.execute("select COUNT(user_id) from user_info where answers="+str(i)+"")
    a = cu.fetchall()[0][0]
    answers.append(a)
    
    
answers2 = []
for i in range(200):
    cu2.execute("select COUNT(user_id) from user_info where answers="+str(i)+"")
    a = cu2.fetchall()[0][0]
    answers2.append(a)
    
------------


followers = []
for i in range(50000):
    cu.execute("select COUNT(user_id) from user_info where followers="+str(i)+"")
    a = cu.fetchall()[0][0]
    print i,'=',a
    followers.append(a)

followers2 = []
for i in range(100000):
    cu2.execute("select COUNT(user_id) from user_info where followers="+str(i)+"")
    a = cu2.fetchall()[0][0]
    followers2.append(a)

---------------
goods = []
for i in range(20000):
    cu.execute("select COUNT(user_id) from user_info where goods="+str(i)+"")
    a = cu.fetchall()[0][0]
    print a
    goods.append(a)

goods2 = []
for i in range(200):
    cu2.execute("select COUNT(user_id) from user_info where goods="+str(i)+"")
    a = cu2.fetchall()[0][0]
    goods2.append(a)

"""





    
for i in range(12000):
    cu.execute("select COUNT(user_id) from user_info where answers="+str(i)+"")
    a = cu.fetchall()[0][0]
    answers.append(a)
    print a     
    
t = range(len(followers))
plt.loglog(t,asks,label="followee")
plt.loglog(t,asks2,label="follower")
plt.legend()
plt.xlabel('number of asks')
plt.ylabel('count')
show()

loglog(t,asks)

plot(t,answers)
loglog(t,answers)

show()
"""



"""
answers = []
cu.execute("select answers from user_info")
a = cu.fetchall()
for i in range(12000):
    b = a[i][0]
    answers.append(b)
    print b
    
    
asks = []
cu.execute("select asks from user_info")
a = cu.fetchall()
for i in range(12000):
    b = a[i][0]
    asks.append(b)
    
    
followers = []
cu.execute("select followers from user_info")
a = cu.fetchall()
for i in range(12000):
    b = a[i][0]
    followers.append(b)    
    
    
goods = []
cu.execute("select goods from user_info")
a = cu.fetchall()
for i in range(12000):
    b = a[i][0]
    goods.append(b)

plot(asks,answers)
loglog(followers,goods)

show()
    
"""
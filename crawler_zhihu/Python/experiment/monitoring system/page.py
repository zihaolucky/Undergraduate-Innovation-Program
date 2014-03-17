# -*- coding: utf-8 -*-
import requests,re
import time,datetime
import sys,os
import math
import codecs
import json


"""
This program is used to listen a specific page in Zhihu.com
"""


login_data = {'email': '137552789@qq.com', 'password': 'God2241226','rememberme':'y',}

# session对象,会自动保持cookies
s = requests.session()


# 考虑到项目进度，暂时不采用数据库进行存储
"""
def build_db(target, answerers):
    if not os.path.exists(r"/Users/white/github/Undergraduate-Innovation-Program/crawler_zhihu/Python/experiment/monitoring system/"+str(target)+".db"):
        print "Creating databse:"+ str(target) + " .\n"
        cx = sqlite3.connect(str(target)+".db")
        cu = cx.cursor()
        cu.execute('CREATE TABLE '+str(target)+' (voter_id text primary key, followers integer, CreatedTime text)')

"""




def collect_data(i):
    print "collecting data.." + "i = " + str(i)
    r = s.get('http://www.zhihu.com/question/22561592')
    global fp
    fp = codecs.open(str(i) + '.txt', 'w', 'utf-8')
    fp.write(r.text)



def main():
    s.post('http://www.zhihu.com/login', login_data)
    print "logined."
    time.sleep(3)
    
    question_urls = ['22561592']
    
    for url in question_urls:
        
    


if __name__=='__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print 'total time consumption: ' + str((end_time - start_time).seconds) + 's'
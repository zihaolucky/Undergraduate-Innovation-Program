# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from time import sleep,ctime

import thread, threading
import time, datetime
import requests
import sqlite3
import codecs
import math
import json
import re


# session对象,会自动保持cookies
s = requests.session()


# auto-login.
def login(login_data):
    # try login.
    print "try login ..\n"
    s.post('http://www.zhihu.com/login', login_data)
    # validate status.
    validation_url = 'http://www.zhihu.com/people/zihaolucky'
    r = s.get(validation_url)
    if(r.url == validation_url):
        print "succeed.\n"
    else:
        print "Something wrong. you may want to login in your browser first."
        print "Try latter!\n"
        
        
#         
# def save2db(db_object, table_name, followee_info):
#     try:
#         followee_name = followee_info[0].replace('-','_')
#         db_object.execute("INSERT INTO "+ str(followee_name) + " VALUES (?,?,?,?,?)", followee_info)
#         cx.commit()
#     except:
#         print "User Existed.\n"
#         
# 
# def buildTable(db_object, table_name):
#     print "creating table "+str(table_name)+"\n"
#     table_name = table_name.replace('-','_')
#     db_object.execute("CREATE TABLE " + str(table_name) + " (user_id text PRIMARY KEY,followers INTEGER, asks INTEGER, answers INTEGER, goods INTEGER)")
#     


    



# 得到回答者信息
def getAnswerer(question_id):
    r = s.get('http://www.zhihu.com/question/' + str(question_id))
    bs = BeautifulSoup(r.text)
    
    # question title
    title = bs.find_all('h2',{'class':'zm-item-title'})
    print title[0].text
    
    # data-aid,用于获取full voter info
    data_aid = re.findall('data-aid="(.*)"',r.text)
    
    # 用户id、用户名
    a = bs.find_all('h3',{'class':'zm-item-answer-author-wrap'})
    answerer_id = []
    answerer_name = []
        # 用户id
    for i in range(len(a)):
        answerer_name.append(a[i].text.strip().split(u'，')[0])
        if(answerer_name[i] != u'匿名用户'):
            answerer_id.append(re.findall('href="/people/(.*)"',str(a[i]))[0])
        else:
            answerer_id.append('anonymous'+str(i))
            
    return answerer_id, data_aid
    
    
    



def getVoter(question_id, answerer_id, data_aid, fp):
    # voter list，通过data_aid得到
    request_url = 'http://www.zhihu.com/node/AnswerFullVoteInfoV2?params=%7B%22answer_id%22%3A%22' + str(data_aid) + '%22%7D'
    voter_list = s.get(request_url)
    voter_name_list = re.findall('title="(.*?)"',voter_list.text)
    voter_id_list = re.findall('/people/(.*)"',voter_list.text)
    
    print str(answerer_id) + ' has received ' + str(len(voter_id_list)) + ' votes.\n'
    
    for i in range(len(voter_id_list)):
        print u'正在抓取用户 '+str(voter_id_list[i])+ u'的关注者列表\n'
        url = 'http://www.zhihu.com/people/' + voter_id_list[i] + '/followees'
        print url
        try:
            r = s.get(url, timeout=20)
        except:
            r = s.get(url, timeout=20)
        user_homepage = r.text
        try:
            followee_list = getFollowee(voter_id_list[i], user_homepage, voter_id_list, question_id, answerer_id)
        except:
            continue
        # check connection.
        status = 0
        for followee in followee_list:
            if(followee in voter_id_list[i:]):
                status = status+1
                fp.write(followee+','+voter_id_list[i])
                fp.write('\n')
                print followee+','+voter_id_list[i]
        if(status==0):
            fp.write(answerer_id+','+voter_id_list[i])
            fp.write('\n')
            print answerer_id+','+voter_id_list[i]
        status = 0 
        print str(voter_id_list[i])+' done. sleep 1s.\n'
        
        
# 模拟点击，发出post请求，以获得用户的followees信息
def getFollowee(voter_id, user_homepage, voter_id_list, question_id, answerer_id):
    
    # 进行加载时的Request URL
    click_url = 'http://www.zhihu.com/node/ProfileFolloweesListV2'
    
    # headers
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Origin':'http://www.zhihu.com',
        'Connection':'keep-alive',
        'Referer':'http://www.zhihu.com/people/' + voter_id + '/followees',
        'Content-Type':'application/x-www-form-urlencoded',
        }
        
    # form data.
    raw_hash_id = re.findall('hash_id(.*)',user_homepage)
    hash_id = raw_hash_id[0][14:46]              # hash_id
    raw_xsrf = re.findall('xsrf(.*)',user_homepage)
    _xsrf = raw_xsrf[0][9:-3]                    # _xsrf
    
    # 需要click的次数
    load_more_times = int(re.findall('<strong>(.*?)</strong>',user_homepage)[2]) / 20
    
    
    # ---- key module ---- #
    followee_list = []
    
        # 用户id, 回答数, 提问数, 关注者数, 赞同数
    followee_id = re.compile('zhihu.com/people/(.*?)"').findall(user_homepage)
    followee_id = followee_id[1:len(followee_id)]
    answers = re.findall('answers" class="zg-link-gray-normal">(.*?) ',user_homepage)
    asks = re.findall('asks" class="zg-link-gray-normal">(.*?) ',user_homepage)
    followers = re.findall('followers" class="zg-link-gray-normal">(.*?) ',user_homepage)
    goods = re.findall('class="zg-link-gray-normal">(.*?) ',user_homepage)
    goods = goods[3:len(goods):4]
    
    
    
        # 检查20个用户信息
    for i in range(len(followee_id)):
        followee_list.append(followee_id[i])
        
    
        # 检查其余用户信息
    for i in range(1,load_more_times+1,1):
        t_start = time.localtime()[5]
        offsets = i*20
            # 由于返回的是json数据,所以用json处理parameters.
        params = json.dumps({"hash_id":hash_id,"order_by":"created","offset":offsets,})
        payload = {"method":"next", "params": params, "_xsrf":_xsrf,}
        
            # debug and improve robustness. Date: 2014-02-12
        try:
            r = s.post(click_url,data=payload,headers=header_info,timeout=10)
        except:
            # 响应时间过程过长则重试
            print u'等待时间过长, repost\n'
            r = s.post(click_url,data=payload,headers=header_info,timeout=30)
        
        
            # parse info.
        
        followee_id = re.findall('href=\\\\"\\\\/people\\\\/(.*?)\\\\',r.text)
        followee_id = followee_id[0:len(followee_id):5]
        user_info = re.findall('class=\\\\"zg-link-gray-normal\\\\">(.*?) ',r.text)
        followers = user_info[0:len(user_info):4]
        asks = followers = user_info[1:len(user_info):4]
        answers = user_info[2:len(user_info):4]
        goods = user_info[3:len(user_info):4]
    
            # 写入
        for i in range(len(followee_id)):
            followee_list.append(followee_id[i])
        
        t_elapsed = time.localtime()[5] - t_start
        print 'got:',offsets,'users.','elapsed: ',t_elapsed,'s.\n'
    
    return followee_list
    

def main():
    login_data = {'email': '137552789@qq.com', 
                'password': 'God2241226',
                'rememberme':'y',}
                
    

    
    # 输入你需要抓取的问题id
    question_list = ['20241368']
    
    # login & varify crawler's running under permission.
    try:
        login(login_data)
        print 'sleep for 3 seconds..\n'
        sleep(3)
    except:
        print 'try latter.\n'
    
    
    
    for question_id in question_list:
        global fp
        fp = codecs.open('/Users/white/github/Undergraduate-Innovation-Program/crawler_zhihu/Python/主题1/infomation diffusion/'+str(question_id)+'.txt','a','utf-8')
        
        # 得到答主id
        (answerer_id, data_aid) = getAnswerer(question_id) 
        for i in range(len(answerer_id)):
            # 得到赞同该答主的voter list.
            print "正在抓取 " + answerer_id[i].strip() + " 的赞同者..\n"
            getVoter(question_id, answerer_id[i], data_aid[i], fp)
                
    
    
if __name__=='__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print 'total time consumption: ' + str((end_time - start_time).seconds) + 's'

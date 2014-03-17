# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import requests
import re
import math
import codecs
import json
import time
from time import sleep,ctime
import datetime
import thread
import threading

#login_data = {'email': 'zihaolucky@gmail.com', 'password': 'shandian123','rememberme':'y',}
login_data = {'email': '137552789@qq.com', 'password': 'God2241226','rememberme':'y',}


# session对象,会自动保持cookies
s = requests.session()


# auto-login.
def login(login_data):
    print "logging in...\n"
    s.post('http://www.zhihu.com/login', login_data)
    


def getAnswerer(question_id):
    # get html of the question page first
    # r = s.get('http://www.zhihu.com/question/22968659')
    r = s.get('http://www.zhihu.com/question/' + str(question_id))
    bs = BeautifulSoup(r.text)
    
    # question title
    a = bs.find_all('h2',{'class':'zm-item-title'})
    print a[0].text
    
    # data-aid,用于获取full voter info
    data_aid = re.findall('data-aid="(.*)"',r.text)
    
    # 用户id、用户名
    a = bs.find_all('h3',{'class':'zm-item-answer-author-wrap'})
    answerer_id = []
    answerer_name = []
    for i in range(len(a)):
        answerer_name.append(a[i].text.strip().split(u'，')[0])
        if(answerer_name[i] != u'匿名用户'):
            answerer_id.append(re.findall('href="/people/(.*)"',str(a[i]))[0])
        else:
            answerer_id.append('anonymous')
            
    for i in range(len(answerer_id)):
        if(answerer_id != 'anonymous'):
            print "正在抓取 " + answerer_id[i].strip() + " 的赞同者..\n"
            Answer_Full_Vote_Info(question_id, answerer_id[i], data_aid[i])
    



def Answer_Full_Vote_Info(question_id, answerer_id, data_aid):
    
    # voter list
    request_url = 'http://www.zhihu.com/node/AnswerFullVoteInfoV2?params=%7B%22answer_id%22%3A%22' + str(data_aid) + '%22%7D'
    voter_list = s.get(request_url)
    voter_name_list = re.findall('title="(.*?)"',voter_list.text)
    voter_id_list = re.findall('/people/(.*)"',voter_list.text)
    
    
    for voter_id in voter_id_list:
        url = 'http://www.zhihu.com/people/' + voter_id + '/followees'
        print url
        r = s.get(url)
        data = r.text
        load_more(voter_id, data, voter_id_list, question_id, answerer_id)
        
        

def load_more(user, data, voter_id_list, question_id, answerer_id):
    
    # 进行加载时的Request URL
    click_url = 'http://www.zhihu.com/node/ProfileFolloweesListV2'
    
    # headers
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Origin':'http://www.zhihu.com',
        'Connection':'keep-alive',
        'Referer':'http://www.zhihu.com/people/' + user + '/followees',
        'Content-Type':'application/x-www-form-urlencoded',
        }
        
    # form data.
    raw_hash_id = re.findall('hash_id(.*)',data)
    hash_id = raw_hash_id[0][14:46]              # hash_id
    raw_xsrf = re.findall('xsrf(.*)',data)
    _xsrf = raw_xsrf[0][9:-3]                    # _xsrf
    
    # 
    load_more_times = int(re.findall('<strong>(.*?)</strong>',data)[2]) / 20
    
    
    # ---- key module ----
        # 写入头20个用户信息
    followees = []    
    
    user_id = re.compile('zhihu.com/people/(.*?)"').findall(data)
    user_id = user_id[1:len(user_id)]
    
    for i in range(len(user_id)):
        followees.append(user_id[i])
    
        # 写入其余用户信息
    
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
            print 'repost'
            r = s.post(click_url,data=payload,headers=header_info,timeout=60)
        
        
            # parse info.
        user_id = re.findall('href=\\\\"\\\\/people\\\\/(.*?)\\\\',r.text)
        user_id = user_id[0:len(user_id):5]
        
        for i in range(len(user_id)):
            followees.append(user_id[i])
        
        
        
        # write_file(user_id,followers,asks,answers,goods)
        # print user_id
        t_elapsed = time.localtime()[5] - t_start
        print 'got:',offsets,'users.','elapsed: ',t_elapsed,'s.\n'      
    
    # append完毕后检查followees中是否含有voter_list中的对象
    
    fp = codecs.open(question_id + '.txt', 'a', 'utf-8')
    match_followees = []
    for target_voter in voter_id_list:
        # print 'target voter: ' + target_voter + '\n'
        if(target_voter in followees):
            global fp
            fp.write(target_voter.strip() + ',' + user.strip()) # source,target
            fp.write('\n')
            match_followees.append(target_voter.strip())
            print target_voter.strip() + ',' + user.strip()
            print '\n'
    if(len(match_followees)==0):
        print 'no match\n'
        fp.write(answerer_id.strip() + ',' + user.strip()) # source,target
        fp.write('\n')
    fp.close()

def main():
    question_list = ['21881838','22561592']
    
    
    
    # login & varify crawler's running under permission.
    login(login_data)
    
    
    for question_id in question_list:
        getAnswerer(question_id)
        
    
    
if __name__=='__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print 'total time consumption: ' + str((end_time - start_time).seconds) + 's'

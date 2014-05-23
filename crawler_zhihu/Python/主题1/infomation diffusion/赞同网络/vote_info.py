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

login_data = {'email': 'zihaolucky@gmail.com', 'password': 'shandian123','rememberme':'y',}


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
            
    for i in range(len(answerer_name)):
        print "正在抓取ta的赞同者..\n"
        print answerer_name[i],data_aid[i]
        print '\n'
        Answer_Full_Vote_Info(question_id, answerer_name[i], data_aid[i])
    



def Answer_Full_Vote_Info(question_id, answerer_name, data_aid):
    
    # headers
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Connection':'keep-alive',
        'Referer':'http://www.zhihu.com/question/' + str(question_id),
        'Content-Type':'application/x-www-form-urlencoded',
        }
    
    # voter list
    request_url = 'http://www.zhihu.com/node/AnswerFullVoteInfoV2?params=%7B%22answer_id%22%3A%22' + str(data_aid) + '%22%7D'
    voter_list = s.get(request_url)
    voter_name_list = re.findall('title="(.*?)"',voter_list.text)
    write_file(question_id, answerer_name, voter_name_list)
    
            
    
    
    
def write_file(question_id, answerer_name, voter_name_list):
    for i in range(len(voter_name_list)):
        fp.write(answerer_name + ',' + voter_name_list[i])
        fp.write('\r\n')
      

def main():
    #question_list = ['22719537']
    question_list = ['23221420']
    
    
    # login & varify crawler's running under permission.
    login(login_data)
    
    #r = s.get('http://www.zhihu.com/people/zihaolucky/followers')
    #if(r.url != 'http://www.zhihu.com/people/zihaolucky/followers'):
    #    break
    
    for question_id in question_list:
        global fp
        fp = codecs.open(question_id + '.txt', 'w', 'utf-8')
        getAnswerer(question_id)
        
    
    
if __name__=='__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print 'total time consumption: ' + str((end_time - start_time).seconds) + 's'

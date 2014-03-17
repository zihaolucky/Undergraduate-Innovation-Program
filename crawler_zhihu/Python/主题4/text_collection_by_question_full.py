# -*- coding: utf-8 -*-
import requests
import re
import math
import codecs
import json
import time
import os
from time import sleep,ctime
import datetime
import thread
import threading
from bs4 import BeautifulSoup

global user_list,login_data

#famous_user_list = ['shisu','wang-wei-63','allenzhang','kentzhu','yangbo','baiya','junyu','wang-xiao-chuan','wangxing','gongjun','zhouyuan','hi-id','shek','commando','chen-hao-84','jin-chen-yu','jixin','linan','raymond-wang']

user_list = []

login_data = {'email': 'zihaolucky@gmail.com', 'password': 'shandian123','rememberme':'y',}
#login_data = {'email': '137552789@qq.com', 'password': 'God2241226','rememberme':'y',}

# session对象,会自动保持cookies
global s
s = requests.session()

# auto-login.
def login(login_data):
    s.post('http://www.zhihu.com/login', login_data)


"""
global search_href
def search(username):
    search_href = []
    r = s.get('http://www.zhihu.com/search?q=' + username + '&type=question')
    bs = BeautifulSoup(r.text)
    a = bs.find_all('a',{'class':'question_link'}) # not clear encoding method.
    global search_href
    for i in range(len(a)):
        if(re.search(u'神胖胖',a[i].text)!=None):
            print a[i].text
            search_href.append(a[i].attrs['href'])
"""        
    

"""
http://www.zhihu.com/node/AnswerCommentBoxV2?params=%7B%22answer_id%22%3A%22 4348163 %22%2C%22load_all%22%3Atrue%7D
http://www.zhihu.com/node/AnswerCommentBoxV2?params=%7B%22answer_id%22%3A%22 4175456 %22%2C%22load_all%22%3Atrue%7D

"""


def parse_comments(question_id, data_aid):
    request_url = 'http://www.zhihu.com/node/AnswerCommentBoxV2?params=%7B%22answer_id%22%3A%22' + str(data_aid) + '%22%2C%22load_all%22%3Atrue%7D'
    
    try:
        comment_list = s.get(request_url,timeout=20)
    except:
        print 'repost.comment.\n'
        comment_list = s.get(request_url,timeout=30)
        
    bs = BeautifulSoup(comment_list.text)
    
    # 评论人地址，暂不需要
    a = bs.find_all('a',{'class':'zg-link'})
    people_url = []
    for i in range(len(a)):
        # print a[i].text
        people_url.append(a[i].attrs['href'])
    
    # 文本信息. 评论人用户名、评论内容、赞同数、时间
    a = bs.find_all('div',{'class':'zm-comment-content-wrap'})
    people_name = []
    comment_text = []
    goods = []
    date = []
    
    for i in range(len(a)):
        b = a[i].text.split('\n\n')
        people_name.append(b[1].split('\n')[0]) # 这里可能需要修缮
        comment_text.append(b[2].strip())
        date.append(b[3].strip())
        goods.append(b[6].strip())
    
    # 写入对应用户回答的评论
    global fp1
    fp1 = codecs.open(r'/Users/white/github/Undergraduate-Innovation-Program/crawler_zhihu/Python/主题4/词库/education.txt', 'a', 'utf-8')
    for j in range(len(comment_text)):
        fp1.write( comment_text[j].strip() )
        fp1.write('\n')
            
        
   
    
    


def getAnswerer_content_comment(question_id):
    # get html of the question page first
    # r = s.get('http://www.zhihu.com/question/22968659')
    try:
        r = s.get('http://www.zhihu.com/question/' + str(question_id),timeout = 30)
    except:
        print 'repost.\n'
        r = s.get('http://www.zhihu.com/question/' + str(question_id),timeout = 30)
    
    bs = BeautifulSoup(r.text)
    
    # question title
    a = bs.find_all('h2',{'class':'zm-item-title'})
    title = a[0].text
    print a[0].text
    
    # data-aid,用于获取full voter info
    data_aids = re.findall('data-aid="(.*)"',r.text)
    
    # 用户id、用户名
    a = bs.find_all('h3',{'class':'zm-item-answer-author-wrap'})
    answerer_id = []
    answerer_name = []
    for i in range(len(a)):
        answerer_name.append(a[i].text.strip().split(u'，')[0])
        
    
    # 读取回答者的回答内容,获得的内容写入.txt文件
    b = bs.find_all('div',{'class':'zm-editable-content'})
    content = []
    for i in range(len(a)):
        content.append(b[2+i].text)
    
    global fp1
    fp1 = codecs.open(r'/Users/white/github/Undergraduate-Innovation-Program/crawler_zhihu/Python/主题4/词库/education.txt', 'a', 'utf-8')
    fp1.write(title.strip())
    fp1.write('\n')
    for i in range(len(answerer_name)):
        fp1.write(content[i])
        fp1.write('\n')
    
    # 读取对应回答者的评论,获得的内容存入(comment).txt文件
    for i in range(len(answerer_name)):
        parse_comments(question_id, data_aids[i])



def crawl_thread1(question_id1):
    for question_id in question_id1:
        try:
            print 'thread1: crawling ' + str(question_id)
            getAnswerer_content_comment(question_id)
        except:
            continue

def crawl_thread2(question_id2):
    for question_id in question_id2:
        try:
            print 'thread2: crawling ' + str(question_id)
            getAnswerer_content_comment(question_id)
        except:
            continue
    


def main():
    # login
    print 'log in...\n'
    try:
        s.post('http://www.zhihu.com/login', login_data)
    except:
        # 响应时间过程过长则重试
        print 'failed.\n'
    
    question_id_thread1 = []
    question_id_thread2 = []
    for url in codecs.open('/Users/white/github/Undergraduate-Innovation-Program/crawler_zhihu/Python/主题4/education_urls.txt','r','utf-8'):
        if(int(url)%2==0):
            question_id_thread1.append(url.strip())
        else:
            question_id_thread2.append(url.strip())
            
    question_id_thread1 = tuple(question_id_thread1)
    question_id_thread2 = tuple(question_id_thread2)
    
    threads = []
    t = threading.Thread(target = crawl_thread1, args = (question_id_thread1,))
    threads.append(t)
    t = threading.Thread(target = crawl_thread2, args = (question_id_thread2,))
    threads.append(t)
    # 多线程
    for i in range(2):
           threads[i].start()
    for i in range(2):
           threads[i].join()
    
    
        
        
     
     
if __name__=='__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print 'total time consumption: ' + str((end_time - start_time).seconds) + 's'
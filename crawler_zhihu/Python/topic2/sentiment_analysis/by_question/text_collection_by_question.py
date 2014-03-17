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


def parse_comments(question_id, userid, data_aid):
    request_url = 'http://www.zhihu.com/node/AnswerCommentBoxV2?params=%7B%22answer_id%22%3A%22' + str(data_aid) + '%22%2C%22load_all%22%3Atrue%7D'
    comment_list = s.get(request_url)
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
    global fp2
    fp2 = codecs.open(r'/Users/white/github/Undergraduate-Innovation-Program/crawler_zhihu/Python/topic2/sentiment_analysis/by_question/'+ str(question_id)+ "/"+ str(userid) + '(comment)' + '.txt', 'w', 'utf-8')
    for j in range(len(people_name)):
        fp2.write( people_name[j].strip() + '\t' + date[j].strip() + '\t' + comment_text[j].strip() + '\t' + goods[j] )
        fp2.write('\n')
            
        
   
    
    


def getAnswerer_content_comment(question_id):
    # get html of the question page first
    # r = s.get('http://www.zhihu.com/question/22968659')
    r = s.get('http://www.zhihu.com/question/' + str(question_id))
    bs = BeautifulSoup(r.text)
    
    # question title
    a = bs.find_all('h2',{'class':'zm-item-title'})
    print a[0].text
    
    # data-aid,用于获取full voter info
    data_aids = re.findall('data-aid="(.*)"',r.text)
    
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
    
    # 读取回答者的回答内容,获得的内容写入.txt文件
    b = bs.find_all('div',{'class':'zm-editable-content'})
    content = []
    for i in range(len(a)):
        content.append(b[2+i].text)
    
    global fp1
    for i in range(len(answerer_id)):
        fp1 = codecs.open(r'/Users/white/github/Undergraduate-Innovation-Program/crawler_zhihu/Python/topic2/sentiment_analysis/by_question/'+ str(question_id)+"/" + answerer_id[i] + '.txt', 'w', 'utf-8')
        fp1.write(content[i])
        fp1.write('\n')
    
    # 读取对应回答者的评论,获得的内容存入(comment).txt文件
    for i in range(len(answerer_id)):
        parse_comments(question_id, answerer_id[i], data_aids[i])






def main():
    # login
    print 'log in...\n'
    try:
        s.post('http://www.zhihu.com/login', login_data)
    except:
        # 响应时间过程过长则重试
        print 'failed.\n'
    
    
    question_ids = ['19551505']
    
    
    for question_id in question_ids:
        print 'crawling question ' + question_id + '\'s text info...\n'
        os.mkdir(question_id)
        # 转跳到用户answer页
        getAnswerer_content_comment(question_id)
        
     
     
if __name__=='__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print 'total time consumption: ' + str((end_time - start_time).seconds) + 's'
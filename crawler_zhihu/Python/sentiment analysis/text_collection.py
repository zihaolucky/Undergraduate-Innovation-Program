# -*- coding: utf-8 -*-
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


def parse_comments(answer_id,title):
    request_url = 'http://www.zhihu.com/node/AnswerCommentBoxV2?params=%7B%22answer_id%22%3A%22' + str(answer_id) + '%22%2C%22load_all%22%3Atrue%7D'
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
    fp2 = codecs.open(title + '_comment.txt', 'w', 'utf-8')
    write_comment(people_name,comment_text,goods,date)

def write_comment(people_name,comment_text,goods,date):
    for i in range(len(people_name)):
        fp2.write( people_name[i] )
        fp2.write('\r\r')
        fp2.write( date[i] )
        fp2.write('\r\r')
        fp2.write( goods[i] )
        fp2.write('\n\n')
        fp2.write( comment_text[i] )
        fp2.write('\n')
        fp2.write('---------------------------------------\n\n')
        
        
    
    
    

    

def parse_answer(userid):
    # 到达对应位置
    target_url = 'http://www.zhihu.com/people/'+ str(userid) + '/answers'
    print 'jump to:' + target_url
    r = s.get(target_url)
    bs = BeautifulSoup(r.text)
    
    # 提取文章标题
    title = bs.find_all('a',{'class':'question_link'})
    title_url = []
    for i in range(len(title)):
        print title[i].text
        title_url.append(title[i].attrs['href'])
    
    # 获得文章url后，打开对应页面，抓取内容：0.问题描述  1.回答  2.评论
    
    for url in title_url:
        target_url = 'http://www.zhihu.com' + url
        r = s.get(target_url)
        bs = BeautifulSoup(r.text)
        # 文章标题
        title = bs.find_all('h2')[0].text.strip()
        print '\n'+title
        # 富文本，内容均在此
        answer_text = bs.find_all('div',{'class':'zm-editable-content'})
        
        question_detail = (answer_text[0].text.strip())
        
        users_answer = (answer_text[2].text.strip())
        
        # 写入回答，标题为文件名
        global fp1
        fp1 = codecs.open(title + '.txt', 'w', 'utf-8')
        write_answer(title,question_detail,users_answer)
        
        # 评论需要另外调用函数抓
        data_aid = re.findall('data-aid="\w{7}',r.text)[0][10:]
        parse_comments(data_aid,title)
        
        
    
def write_answer(title,question_detail,users_answer):
    fp1.write( title )
    fp1.write('\n\n')
    fp1.write( question_detail )
    fp1.write('\n\n')
    fp1.write( users_answer )
    fp1.write('\n\n')
    
    
 






def main():
    # login
    print 'log in...\n'
    try:
        s.post('http://www.zhihu.com/login', login_data)
    except:
        # 响应时间过程过长则重试
        print 'failed.\n'
    
    
    userid = ['shenpp']
    
    for user in userid:
        print 'crawling ' + user + '\'s text info...\n'
        
        # 转跳到用户answer页
        parse_answer(user)
     
     
if __name__=='__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print 'total time consumption: ' + str((end_time - start_time).seconds) + 's'
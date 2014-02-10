# -*- coding: utf-8 -*-
import requests
import re
import math
import codecs
import json
import time
import datetime


global user_list,login_data


#user_list = ['wang-wei-63','allenzhang','kentzhu']
user_list = ['linan']
#user_list = ['hi-id','shek']
#user_list = ['commando','chen-hao-84','jin-chen-yu']

login_data = {'email': 'zihaolucky@gmail.com', 'password': 'Shandian@123', }


# session对象,会自动保持cookies
s = requests.session()

# auto-login.
def login(login_data):
    s.post('http://www.zhihu.com/login', login_data)


def load_more(user,data):
    # 进行加载时的Request URL
    click_url = 'http://www.zhihu.com/node/ProfileFollowersListV2'
    
    # headers
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Origin':'http://www.zhihu.com',
        'Connection':'keep-alive',
        'Referer':'http://www.zhihu.com/people/' + user + '/followers',
        'Content-Type':'application/x-www-form-urlencoded',
        }
        
    # form data.
    raw_hash_id = re.findall('hash_id(.*)',data)
    hash_id = raw_hash_id[0][14:46]              # hash_id
    raw_xsrf = re.findall('xsrf(.*)',data)
    _xsrf = raw_xsrf[0][9:-3]                    # _xsrf
    
    # 
    load_more_times = int(re.findall('<strong>(.*?)</strong>',data)[3]) / 20
    
    
    # ---- key module ----
        # 写入头20个用户信息
    user_id = re.compile('zhihu.com/people/(.*?)"').findall(data)
    user_id = user_id[1:len(user_id)]
    answers = re.findall('answers" class="zg-link-gray-normal">(.*?) ',data)
    asks = re.findall('asks" class="zg-link-gray-normal">(.*?) ',data)
    followers = re.findall('followers" class="zg-link-gray-normal">(.*?) ',data)
    goods = re.findall('class="zg-link-gray-normal">(.*?) ',data)
    goods = goods[3:len(goods):4]
    
    fp.write('user_id,followers,asks,answers,goods')
    fp.write('\r\n')
    write_file(user_id,followers,asks,answers,goods)
        # 写入其余用户信息
    start_time = datetime.datetime.now()
    for i in range(1,load_more_times+1):
        t_start = time.localtime()[5]
        offsets = i*20
        # 由于返回的是json数据,所以用json处理parameters.
        params = json.dumps({"hash_id":hash_id,"order_by":"created","offset":offsets,})
        payload = {"method":"next", "params": params, "_xsrf":_xsrf,}
        r = s.post(click_url,data=payload,headers=header_info)
        
            # parse info.
        user_id = re.findall('href=\\\\"\\\\/people\\\\/(.*?)\\\\',r.text)
        user_id = user_id[0:len(user_id):5]
        user_info = re.findall('class=\\\\"zg-link-gray-normal\\\\">(.*?) ',r.text)
        followers = user_info[0:len(user_info):4]
        asks = followers = user_info[1:len(user_info):4]
        answers = user_info[2:len(user_info):4]
        goods = user_info[3:len(user_info):4]
        
        #print user_id,followers,asks,answers,goods
        #print len(user_id),len(followers),len(asks),len(answers),len(goods)
        
        
        write_file(user_id,followers,asks,answers,goods)
        # print user_id
        t_elapsed = time.localtime()[5] - t_start
        print 'got:',offsets,'users.','elapsed: ',t_elapsed,'s.\n'
    end_time = datetime.datetime.now()
    print 'total time consumption: ' + str((end_time - start_time).seconds) + 's'

    
    
def main():
    # login
    s.post('http://www.zhihu.com/login', login_data)
    
    for user in user_list:
        print 'crawling ' + user + '\'s followers...\n'
        # 写文件
        global fp
        fp = codecs.open(user + '.txt', 'w', 'utf-8')
        
        url = 'http://www.zhihu.com/people/' + user + '/followers'
        # 转跳到用户followers页
        r = s.get(url)
        data = r.text
        load_more(user,data)

    
def write_file(user_id,followers,asks,answers,goods):
    for i in range(len(user_id)):
        global fp
        fp.write( user_id[i].strip()+','+followers[i].strip()+','+asks[i].strip()+','+answers[i].strip()+','+goods[i].strip() )
        fp.write('\r\n') 
        
    
    
if __name__=='__main__':
    main()

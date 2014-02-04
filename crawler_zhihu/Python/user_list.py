# -*- coding: utf-8 -*-
import requests
import re
import math
import codecs
import json
import time

global user_list,login_data
user_list = ['linan','commando']
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
    write_file(user_id)
        # 写入其余用户信息
    for i in range(1,load_more_times+1):
        t_start = time.localtime()[5]
        offsets = i*20
        # 由于返回的是json数据,所以用json处理parameters.
        params = json.dumps({"hash_id":hash_id,"order_by":"created","offset":offsets,})
        payload = {"method":"next", "params": params, "_xsrf":_xsrf,}
        r = s.post(click_url,data=payload,headers=header_info)
        user_id = re.findall('href=\\\\"\\\\/people\\\\/(.*?)\\\\',r.text)
            # parse info.
        user_id = set(user_id) # 去重
        user_id = [i for i in user_id] # 将set变为数组,以便写入
        write_file(user_id)
        t_elapsed = time.localtime()[5] - t_start
        print 'got:',offsets,'users.','elapsed: ',t_elapsed,'s.\n'
        

    
    
def main():
    # login
    s.post('http://www.zhihu.com/login', login_data)
    
    for user in user_list:
        print 'crawling' + user + '\'s followers...\n'
        # 写文件
        global fp
        fp = codecs.open(user + '.txt', 'w', 'utf-8')
        
        url = 'http://www.zhihu.com/people/' + user + '/followers'
        # 转跳到用户followers页
        r = s.get(url)
        data = r.text
        load_more(user,data)

    
def write_file(user_id):
    for i in range(len(user_id)):
        
        global fp
        fp.write( user_id[i].strip() )
        fp.write('\r\n') 
    
    
if __name__=='__main__':
    main()

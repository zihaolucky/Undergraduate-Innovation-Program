# -*- coding: utf-8 -*-
import requests
import re
import math
import codecs
import json

# 写文件
fp = codecs.open('user_list.txt', 'w', 'utf-8')

def write_file(user_id):
    for i in range(len(user_id)):
        fp.write( user_id[i].strip() )
        fp.write('\r\n')


user_list = ['zihaolucky']
login_data = {'email': 'zihaolucky@gmail.com', 'password': 'Shandian@123', }



click_url = 'http://www.zhihu.com/node/ProfileFollowersListV2'

# ---- #

s = requests.session()
s.post('http://www.zhihu.com/login', login_data)
for user in user_list:
    url = 'http://www.zhihu.com/people/' + user + '/followers'
    # headers
    header_info = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Host':'www.zhihu.com',
        'Origin':'http://www.zhihu.com',
        'Connection':'keep-alive',
        # 'Referer':'http://www.zhihu.com/people/' + 'zihaolucky' + '/followers',
        'Referer':'http://www.zhihu.com/people/' + user + '/followers',
        'Content-Type':'application/x-www-form-urlencoded',
        }
    
    # 转跳到用户followers页
    r = s.get(url)
    data = r.text
    
    
    
    # form data.
    raw_hash_id = re.findall('hash_id(.*)',data)
    hash_id = raw_hash_id[0][14:46]
    raw_xsrf = re.findall('xsrf(.*)',data)
    _xsrf = raw_xsrf[0][9:-3]
    
    load_more_times = int(re.findall('<strong>(.*?)</strong>',data)[3]) / 20
    
    
    # key module
    user_id = re.compile('zhihu.com/people/(.*?)"').findall(data)
    print user_id
    write_file(user_id)
    
    for i in range(1,load_more_times+1):
        offsets = i*20
        params = json.dumps({"hash_id":hash_id,"order_by":"created","offset":offsets,})
        payload = {"method":"next", "params": params, "_xsrf":_xsrf,}
        r = s.post(click_url,data=payload,headers=header_info)
        user_id = re.findall('href=\\\\"\\\\/people\\\\/(.*?)\\\\',r.text)
        # parse info.
        user_id = set(user_id)
        user_id = [i for i in user_id]
        print user_id
        write_file(user_id)

# -*- coding: utf-8 -*-
import requests
import re
import math
import codecs
import json
import time
import datetime


global user_list,login_data

login_data = {'email': '137552789@qq.com', 'password': 'God2241226','rememberme':'y',}

# session对象,会自动保持cookies
s = requests.session()



def collect_data(i):
    print "collecting data.." + "i = " + str(i)
    r = s.get('http://www.zhihu.com/question/22777914')
    global fp
    fp = codecs.open(str(i) + '.txt', 'w', 'utf-8')
    fp.write(r.text)

def main():
    s.post('http://www.zhihu.com/login', login_data)
    print "logined."
    for i in range(120):
        collect_data(i)
        time.sleep( 90 )
    


if __name__=='__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print 'total time consumption: ' + str((end_time - start_time).seconds) + 's'
# -*- coding: utf-8 -*-
import sys,os
import codecs
import time
sys.path.append("../")
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

from jieba.analyse import ChineseAnalyzer 

analyzer = ChineseAnalyzer()

log_f = codecs.open("/Users/white/github/Undergraduate-Innovation-Program/crawler_zhihu/Python/主题4/result.txt","w","utf-8")
f = codecs.open('/Users/white/github/Undergraduate-Innovation-Program/crawler_zhihu/Python/主题4/education.txt','r','utf-8')
content = open('/Users/white/github/Undergraduate-Innovation-Program/crawler_zhihu/Python/主题4/education.txt',"rb").read()

t1 = time.time()

line = f.readline()
while line:
    for t in analyzer(line.strip()):
        log_f.write(t.text)
        log_f.write('\n')
    line = f.readline()
    #print line
   
f.close()
log_f.close()

t2 = time.time()
tm_cost = t2-t1
print 'cost',tm_cost
print 'speed' , len(content)/tm_cost, " bytes/second"

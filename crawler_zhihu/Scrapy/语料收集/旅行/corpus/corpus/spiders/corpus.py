# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings

import codecs
 
#使用UTF-8格式保存文件
fp = codecs.open('question_urls.txt', 'w', 'utf-8')
 
class corpus(BaseSpider):
    #设置爬虫名称
    name = "corpus"
    #设置起始URL列表，此处包含了话题下的全部问题链接
    start_urls = ["http://www.zhihu.com/topic/19553176/questions?page=1"]
    for i in range(2,3054,1):
        start_urls.append("http://www.zhihu.com/topic/19553176/questions?page="+str(i))
    
    """
    def start_requests(self):
        return [FormRequest("http://www.zhihu.com/login",
                            formdata={'email': 'zihaolucky@gmail.com', 'password': 'shandian123'},
                            callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        pass
    """
    
    def parse(self, response):
        req = []
        hxs = HtmlXPathSelector(response)
        
        # 通过XPath选出question_urls
        question_urls = hxs.select('//h2[@class="question-item-title"]//@href').extract()
        question_titles = hxs.select('//h2[@class="question-item-title"]/a/text()').extract()
        
        print 'question_urls =', question_urls
        for i in range(len(question_urls)):
            #构建新的URL
            question_id = question_urls[i][10:]
            print question_titles[i]
            fp.write(question_id)
            fp.write('\n')
            
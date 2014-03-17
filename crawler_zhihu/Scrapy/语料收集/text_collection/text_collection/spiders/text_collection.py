# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings

import codecs
 
#使用UTF-8格式保存文件
fp = codecs.open('context_full.txt', 'w', 'utf-8')


class LoginSpider(BaseSpider):
    name = 'text_collection'
    start_urls = ['http://www.zhihu.com/login']
    print start_urls

    def parse(self, response):
        return [FormRequest.from_response(response,
                    formdata={'email': 'zihaolucky@gmail.com', 'password': 'shandian123'},
                    callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return


class text_collection(BaseSpider):
    #设置爬虫名称
    name = "text_collection"
    #设置起始URL列表，此处包含了话题下的全部问题链接
    start_urls = ["http://www.zhihu.com/topic/19551556/top-answers"]
    #for i in range(2,457,1):
    #    start_urls.append("http://www.zhihu.com/topic/19550780/questions?page="+str(i))
    
    
    
    
    def parse(self, response):
        req = []
        hxs = HtmlXPathSelector(response)
        
        # 通过XPath选出question_urls
        question_urls = hxs.select('//h2[@class="question-item-title"]//@href').extract()
        question_titles = hxs.select('//h2[@class="question-item-title"]/a/text()').extract()
        
        
        for url in question_urls:
            #构建新的URL
            new_url = "http://www.zhihu.com" + url
            print "parsing %s ..." % (new_url)
            #创建对应的页面的Request对象，设定回调函数为parse_answer_page，处理返回的页面
            r = Request(new_url, callback=self.parse_answer_page)
            req.append(r)
        return req
        
    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        #利用XPath抽取出线路名称:line_name
        title = hxs.select('//div[@id="zh-question-title"]//text()').extract()[1]
        context = hxs.select('//div[@class="zm-item-rich-text"]//text()').extract()
        #结果写入到记录的文件之中
        
        #每个站点之间用,隔开
        fp.write(title.strip())
        fp.write('\n')
        for i in range(len(context)):
            fp.write( context[i].strip() )
            fp.write('\n')
            #opt += (name.strip() + ',')
        
            
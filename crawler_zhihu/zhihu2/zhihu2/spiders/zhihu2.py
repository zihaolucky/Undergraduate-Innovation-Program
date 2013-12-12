# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.conf import settings
 
import codecs
 
#使用UTF-8格式保存文件
fp = codecs.open('record.txt', 'w', 'utf-8')
 
class ZhihuSpider(BaseSpider):
    #设置爬虫名称
    name = "zhihu2"
    #设置起始URL列表,it must be a list.
    start_urls = ["http://www.zhihu.com/topic/19553176/top-answers"]
    for i in range(2,20):
        page = "http://www.zhihu.com/topic/19553176/top-answers?page="+ str(i)
        start_urls.append(page)
    
 
    def parse(self, response):
        req = []
        hxs = HtmlXPathSelector(response)
        #通过XPath选出同一话题下精华帖的URL
        global page_urls
        page_urls =  hxs.select('//div[@id="zh-topic-top-page-list"]//h2//@href').extract()
        print 'page_urls =', page_urls
        for url in page_urls:
            #构建新的URL
            new_url = "http://www.zhihu.com" + url
            print "[parse]new_url = %s" % (new_url)
            #创建对应的页面的Request对象，设定回调函数为parse_cat，利用parse_cat处理返回的页面
            r = Request(new_url, callback=self.parse_question_page)
            req.append(r)
        return req
        
    def parse_question_page(self, response):
        req = []
        hxs = HtmlXPathSelector(response)
        #通过XPath选出同一话题下精华帖的URL
        answer_urls =  hxs.select('//span[@class="answer-date-link-wrap"]//@href').extract()
        print 'answer_urls =', answer_urls
        
        for url in answer_urls:
            #构建新的URL
            new_url = "http://www.zhihu.com" + url
            print "[parse]new_url = %s" % (new_url)
            #创建对应的页面的Request对象，设定回调函数为parse_cat，利用parse_cat处理返回的页面
            r = Request(new_url, callback=self.parse_answer_page)
            req.append(r)
        return req
 
    def parse_answer_page(self, response):
        hxs = HtmlXPathSelector(response)
        #利用XPath抽取出线路名称:line_name        
        first_answer_name = hxs.select('//div[@class="zm-item-answer-author-info"]//h3/a[2]/text()').extract()
        #
        comment_name = hxs.select('//div[@class="zm-comment-hd"]/a/text()').extract()
        #结果写入到记录的文件之中
        topic_name = hxs.select('//h2[@class="zm-item-title zm-editable-content"]/a/text()').extract()
        
        for i in range(len(first_answer_name)):
            fp.write( topic_name[0].strip() + ';' + first_answer_name[i].strip() )
            fp.write('\r\n')
        
        #二级评论
        for i in range(len(comment_name)):
            fp.write( first_answer_name[0].strip() + ';' + comment_name[i].strip() )
            fp.write('\r\n')
        
        print "\n"
        print "topic name:",topic_name[0].strip()
        print "\n"
        for i in range(len(comment_name)):
            print comment_name[i]
        for j in range(len(first_answer_name)):
            print first_answer_name[j]
        print '--------------------------------------------------------------'
        print "\n"
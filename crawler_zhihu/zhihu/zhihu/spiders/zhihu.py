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
    name = "zhihu"
    #设置起始URL列表
    start_urls = ["http://www.zhihu.com/question/20151457"]
 
    def parse(self, response):
        req = []
        hxs = HtmlXPathSelector(response)
        #通过XPath选出公交车路线分类页面的URL
        answer_urls =  hxs.select('//span[@class="answer-date-link-wrap"]//@href').extract()
        print 'answer_urls =', answer_urls
        for url in answer_urls:
            #构建新的URL
            new_url = "http://www.zhihu.com" + url
            print "[parse]new_url = %s" % (new_url)
            #创建对应的页面的Request对象，设定回调函数为parse_answer_page，处理返回的页面
            r = Request(new_url, callback=self.parse_answer_page)
            req.append(r)
        return req
        
 
    def parse_answer_page(self, response):
        hxs = HtmlXPathSelector(response)
        #利用XPath抽取出线路名称:line_name
        title = hxs.select('/html/body/div[4]/div/div/div[2]/h2/a/text()').extract()
        first_answer_name = hxs.select('//div[@class="zm-item-answer-author-info"]//h3/a[2]/text()').extract()
        #利用XPath抽取路线中经过的站点名称:route
        comment_name = hxs.select('//div[@class="zm-comment-hd"]/a/text()').extract()
        #结果写入到记录的文件之中
        
        #每个站点之间用,隔开
        fp.write(title[0].strip() + ',' + first_answer_name[0].strip())
        fp.write('\r\n')
        for i in range(len(comment_name)):
            fp.write( first_answer_name[0].strip() + ',' + comment_name[i].strip() )
            fp.write('\r\n')
            #opt += (name.strip() + ',')
        print "\n"
        print first_answer_name[0]
        print "\n"
        for i in range(len(comment_name)):
            print comment_name[i]
        print '--------------------------------------------------------------'
        
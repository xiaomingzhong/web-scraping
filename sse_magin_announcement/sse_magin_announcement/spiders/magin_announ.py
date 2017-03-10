#-*- encoding:utf8 -*-

import scrapy
import logging
from ..items import SseMaginAnnouncementItem

class MaginSpider(scrapy.Spider):

    name = 'sse_magin_announcement'

    def start_requests(self):
        url = 'http://www.sse.com.cn/disclosure/magin/announcement/ssereport/s_index.htm'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                   'Referer': 'http://www.sse.com.cn/disclosure/magin/announcement/'
                   }
        yield scrapy.Request(url=url, headers=headers, meta={'headers': headers}, callback=self.real_requests)


    def real_requests(self, response):
        announcements = response.xpath('//dd')
        headers = response.meta.get('headers')
        for announcement in announcements:
            url = announcement.xpath('a/@href').extract_first()
            url = 'http://www.sse.com.cn' + url
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)
        logging.info('=================================1=============================')
        page_index = response.xpath('//div[@class="createPage"]/@page_index').extract_first()
        page_count = response.xpath('//div[@class="createPage"]/@page_count').extract_first()
        new_index = int(page_index) + 1
        if new_index <= int(page_count):
            url = 'http://www.sse.com.cn/disclosure/magin/announcement/s_index_{0}.htm'.format(new_index)
            logging.info('============================2=======================')
            logging.info(url)
            yield scrapy.FormRequest(url=url, headers=headers, callback=self.real_requests)

    def parse(self,response):
        article = response.css('div.article-infor')
        item = SseMaginAnnouncementItem()
        item['title'] = article.xpath('h2/text()').extract_first()
        item['announ_date'] = article.css('.article_opt').xpath('i/text()').extract_first()
        lines = article.xpath('div[@class="allZoom"]//text()').extract()
        content = ""
        for line in lines:
            content += line
        item['content'] = content
        return item


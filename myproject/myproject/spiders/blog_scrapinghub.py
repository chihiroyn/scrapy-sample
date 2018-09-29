# -*- coding: utf-8 -*-
import scrapy


class BlogScrapinghubSpider(scrapy.Spider):
    name = 'blog_scrapinghub'
    allowed_domains = ['blog.scrapinghub.com']
    start_urls = ['http://blog.scrapinghub.com/']

    def parse(self, response):
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').extract_first()}

#        for next_page in response.css('div.prev-post > a'):
#        for next_page in response.css('.next-posts-link'):
        for next_page in response.css('div.blog-pagination > a'):
            yield response.follow(next_page, self.parse)

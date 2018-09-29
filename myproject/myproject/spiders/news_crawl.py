from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myproject.items import Headline

class NewsCrawlSpider(CrawlSpider):
    name = 'news_crawl'
    allowed_domains = ['news.yahoo.co.jp']
    start_urls = ['http://news.yahoo.co.jp/']

    # List of rules for crawling links
    rules = (
        # Route link to page of topics, treat response with parse_topics() method
        Rule(LinkExtractor(allow=r'/pickup/\d+$'), callback="parse_topics"),
    )

    def parse_topics(self, response):
        """
        Scrape title and body-text
        """ 
        item = Headline()
        item['title'] = response.css('.newsTitle ::text').extract_first()
        item['body'] = response.css('.hbody').xpath('string()').extract_first()
        yield item
from scrapy import Spider, Request
from AfpyCrawler.items import AfpycrawlerItem as Items

class AfpyJobSpider(Spider):
    name = 'afpy_jobs'
    start_urls = ['http://www.afpy.org/posts/emplois']

    def parse(self, response):
        job_items = Items()
        # for job in response.xpath('//article'):
        job = response.xpath('//article[last()]')
        title_xpath = './h2/text()'
        url_xpath = './p/a/@href'

        job_items['title'] = job.xpath(title_xpath)[0].extract()
        job_items['url'] = job.xpath(url_xpath)[0].extract()
        yield job_items

        #next_page_url_xpath = '//aside[last()]/a[last()]/@href'
        #next_page_url = response.xpath(next_page_url_xpath)[0].extract()
        #yield Request(url='http://www.afpy.org'+next_page_url)
import scrapy
from Lagou.items import LagouItem

class Lagou_zhiwei(scrapy.Spider):
    name = 'sam'
    start_urls = [
        "https://www.lagou.com/"
    ]

    def parse(self, response):
        for item in response.xpath('//*[@id="sidebar"]/div/div[1]/div[1]/div/a'):
            jobClass = item.xpath('text()').extract()
            jobUrl = item.xpath("@href").extract_first()

            oneItem = LagouItem()
            oneItem['jobClass'] = jobClass
            oneItem['jobUrl'] = jobUrl
            yield oneItem

        for item in response.xpath('//*[@id="sidebar"]/div/div[1]/div[2]/dl/dd/a'):
            jobClass = item.xpath('text()').extract()
            jobUrl = item.xpath("@href").extract_first()

            oneItem = LagouItem()
            oneItem['jobClass'] = jobClass
            oneItem['jobUrl'] = jobUrl
            yield oneItem
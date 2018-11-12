# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from ..items import NoticesThatIWantToReadItem
from scrapy import Spider


class notices_that_i_want_to_read(Spider):
    name = 'notices_that_i_want_to_read'
    start_urls = ['https://g1.globo.com/economia/tecnologia/']

    def parse(self, response):
        table_with_notices = response.xpath("//a[contains(@class, 'feed-post-link')]")
        table_with_subtitles = response.xpath("//div[contains(@class , 'feed-post-body-resumo')]")

        title = table_with_notices.xpath('./text()').extract()
        subtitle = table_with_subtitles.xpath('./div[contains(@class , _label_event)]/text()').extract()

        for i in range(len(title)):
            loader = ItemLoader(item=NoticesThatIWantToReadItem(), response=response)
            loader.add_value('title', title[i])
            loader.add_value('subtitle', subtitle[i])
            yield loader.load_item()

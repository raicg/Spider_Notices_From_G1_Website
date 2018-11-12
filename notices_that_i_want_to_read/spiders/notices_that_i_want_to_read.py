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
        href = table_with_notices.xpath('./@href').extract()
        subtitle = table_with_subtitles.xpath('./div[contains(@class , _label_event)]/text()').extract()

        for i in range(len(href)):
            yield response.follow(href[i], callback=self.parse_notice_page,
                meta={'title': title[i], 'subtitle': subtitle[i]}
            )

    def parse_notice_page(self, response):
        notice = response.xpath("//p[contains(@class, 'content-text__container')]/text()").extract()

        loader = ItemLoader(item=NoticesThatIWantToReadItem(), response=response)
        loader.add_value('title', response.meta.get('title'))
        loader.add_value('subtitle', response.meta.get('subtitle'))
        loader.add_value('notice', notice)

        return loader.load_item()

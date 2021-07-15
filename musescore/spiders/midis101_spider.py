import scrapy

from ..items import Midis101Item


class Midis101SpiderSpider(scrapy.Spider):
    name = 'midis101_spider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'musescore.pipelines.Midis101Pipeline': 111,
            # 'musescore.pipelines.Midis101MDFileDownloadPipeline': 222,
        },
    }
    allowed_domains = ['midis101.com']
    base_domain = 'http://www.midis101.com'
    start_urls = ['http://www.midis101.com/search/1/Italian']

    def start_requests(self):
        for page_num in range(1, 892):
            url = f'http://www.midis101.com/search/{page_num}/Italian'
            yield scrapy.Request(url=url, callback=self.parse, meta={'search_keyword': 'Italian', 'url': url})

    def parse(self, response, **kwargs):
        page_selector = scrapy.Selector(response)
        rows = page_selector.xpath(
            '//div[@class="main_content"]/div[(@class="main_content_normal") or (@class="main_content_alt")]')

        for row in rows:
            url = row.xpath('.//a/@href').extract_first()
            name = row.xpath('.//a/text()').extract_first()
            full_url = self.base_domain + url

            yield scrapy.Request(url=full_url, callback=self.parse_page, meta={**response.meta, 'name': name})

    def parse_page(self, response):
        page_selector = scrapy.Selector(response)
        url = page_selector.xpath('//div[@class="txtSubmit"]/a/@href').extract_first()
        midi_file_url = self.base_domain + url

        item = Midis101Item()
        name = response.meta['name']
        if name.startswith('Italian') and name != 'Italian':
            name = name.replace('Italian', '').strip()

        item['name'] = name
        item['folder_name'] = name
        item['search_word'] = response.meta['search_keyword']
        item['md_file_url'] = midi_file_url

        return item

import scrapy

from ..items import SongGalaxyItem


class SongGalaxySpider(scrapy.Spider):
    name = 'songgalaxy_spider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'musescore.pipelines.SongGalaxyPipeline': 111,
            'musescore.pipelines.MDFileDownloadPipeline': 222,
        },
    }
    allowed_domains = ['songgalaxy.com']
    start_urls = ['https://songgalaxy.com/midi.php?cat=German',
                  'https://songgalaxy.com/midi.php?cat=Ital%2FFrench%2FSpan',
                  'https://songgalaxy.com/midi.php?cat=Dutch',
                  'https://songgalaxy.com/midi.php?cat=Classical']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'url': url})

    def parse(self, response, **kwargs):
        page_selector = scrapy.Selector(response)

        item_count_text = page_selector.xpath('//div[@id="main"]//h1/text()').extract_first()

        try:
            items_count = item_count_text.split('(')[-1].split(')')[0]
            items_count = int(items_count)
        except (ValueError, IndexError):
            return

        pages = [page * 20 for page in range(items_count // 20 + 1)]
        print(pages[-1])
        for page in pages:
            yield scrapy.Request(url=response.meta['url'] + f'&p={page}', callback=self.parse_page, meta=response.meta)

    def parse_page(self, response, **kwargs):
        page_selector = scrapy.Selector(response)
        table_rows = page_selector.xpath('.//table[@class="contentsong"]//tr')
        for table_row in table_rows:
            row_selector = table_row.xpath('.//td')
            item = SongGalaxyItem()
            item['artist_name'] = row_selector[0].xpath('.//text()').extract_first()
            item['song_name'] = row_selector[1].xpath('.//text()').extract_first()
            item['folder_name'] = f'{item["artist_name"]}-{item["song_name"]}'
            item['md_file_url'] = row_selector[2].xpath('./a[@class="demo-save"]/@href').extract_first()

            item['search_word'] = response.meta['url'].split('=')[-1]

            yield item

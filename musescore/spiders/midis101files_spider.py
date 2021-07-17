import pandas
import scrapy

from ..items import Midis101Item
from ..pipelines import MIDIS101_OUTPUT_FOLDER_PATH


class Midis101FilesSpiderSpider(scrapy.Spider):
    name = 'midis101files_spider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'musescore.pipelines.Midis101MDFileDownloadPipeline': 222,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'musescore.middlewares.ScraperApiProxyMiddleware': 222,
        }
    }

    allowed_domains = ['midis101.com']
    base_domain = 'http://www.midis101.com'

    file_path = 'outputs/midis101/Italian.csv'

    def start_requests(self):
        data = pandas.read_csv(self.file_path)
        yield scrapy.Request(url=self.base_domain, callback=self.parse, meta={'data': data})

    def parse(self, response, **kwargs):
        for index, row in response.meta['data'].iterrows():
            item = Midis101Item()
            item['name'] = row['name']
            item['folder_name'] = row['folder_name']
            item['search_word'] = row['search_word']
            item['md_file_url'] = row['md_file_url']

            file_name = row['md_file_url'].split('/')[-1]
            folder_path = MIDIS101_OUTPUT_FOLDER_PATH.joinpath(row['search_word']).joinpath(row['folder_name'])
            file_path = folder_path.joinpath(f'{file_name}.mid')
            if not file_path.is_file():
                print('is not', file_path)
                yield item
            else:
                print('is', file_path)
                continue

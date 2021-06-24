import json
from datetime import datetime
from typing import List

import pandas
import scrapy
from scrapy import Selector

from ..items import MusescoreItem


class MusescoreSpider(scrapy.Spider):
    name = "musescore_spider"
    start_url: str = 'https://musescore.com/sheetmusic?page=%s&text=%s'
    result_per_page = 20

    def start_requests(self):
        search_words = pandas.read_csv('musicians.csv')['name'].values

        for search_keyword in search_words:
            url = self.start_url % ('1', search_keyword.replace(' ', '+'))
            yield scrapy.Request(url=url, callback=self.parse, meta={'search_keyword': search_keyword, 'url': url})
            break

    def parse(self, response, **kwargs):

        selector = Selector(response)
        page_data = selector.xpath("//div[@class='js-store']/@data-content").extract_first()
        page_data = json.loads(page_data)

        first_page_results = page_data['store']['page']['data']['scores']
        self.parse_page_results(first_page_results, **kwargs)

        try:
            results_count = page_data['store']['page']['data']['pagination']['totalCount']
        except KeyError:
            results_count = 20
        pages_count = results_count // self.result_per_page + 1
        print(f'{pages_count}' * 1000)
        for page_num in range(2, pages_count):
            url = self.start_url % (page_num, response.meta['search_keyword'].replace(' ', '+'))
            yield scrapy.Request(url=url, callback=self.parse_pages, meta=response.meta)

    def parse_pages(self, response, **kwargs):
        selector = Selector(response)
        page_data = selector.xpath("//div[@class='js-store']/@data-content").extract_first()
        page_data = json.loads(page_data)
        page_results = page_data['store']['page']['data']['scores']

        return self.parse_page_results(page_results, **response.meta)

    def parse_page_results(self, results: List[dict], **kwargs):
        for result in results:
            yield self.parse_result(result, **kwargs)

    def parse_result(self, result: dict, **kwargs):
        item = MusescoreItem()
        item.url = result.get('url')
        item.title = result.get('title')
        item.search_keyword = kwargs.get('search_keyword')
        item.parts = result.get('parts')
        item.duration = result.get('duration')
        item.pages = result.get('pages_count')
        item.measures = result.get('measures')
        item.key_signature = result.get('keysig')
        item.ensemble = result.get('description')
        item.part_names = ','.join(result.get('parts_names'))
        item.favourites = result.get('favourites_count')
        item.views = result.get('hits')
        item.rating = result.get('rating', {}).get('rating')
        item.uploaded_on = datetime.fromtimestamp(result.get('date_created', 0))
        item.instruments = ','.join(result.get('instruments'))
        if result.get('instrumentations'):
            instrumentations = [each.get('name') for each in result.get('instrumentations')]
            item.instrumentations = ','.join(instrumentations)

        return item

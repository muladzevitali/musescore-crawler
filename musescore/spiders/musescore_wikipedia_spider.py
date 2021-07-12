import json
from datetime import datetime
from pathlib import Path
from typing import List

import pandas
import scrapy
from scrapy import Selector

from ..items import MusescoreItem


def format_search_word(search_word: str) -> str:
    """
    Function removes unwanted characters from query parameter
    """
    search_word = search_word.replace('&', '%26')
    search_word = search_word.replace(' ', '+')

    return search_word


def prettify_title(title: str) -> str:
    html_tags_to_remove = ['[b]', '[/b]']

    for tag in html_tags_to_remove:
        title = title.replace(tag, '')

    return title


class MusescoreWikipediaSpider(scrapy.Spider):
    name = "musescore_wikipedia_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'musescore.pipelines.MusescoreWikipediaPipeline': 500,
        },
    }
    start_url: str = 'https://musescore.com/sheetmusic?page=%s&text=%s'
    wikipedia_outputs_path = Path('outputs/wikipedia')
    result_per_page = 20

    def start_requests(self):

        search_words = list()
        for folder in self.wikipedia_outputs_path.iterdir():
            for file_path in folder.iterdir():
                artist_names = pandas.read_csv(file_path)['artist_name'].values.tolist()
                _search_words = [(artist_name, folder.name, file_path.stem) for artist_name in artist_names]
                search_words.extend(_search_words)

        for (artist_name, category_name, list_name) in search_words:
            url = self.start_url % ('1', format_search_word(artist_name))
            yield scrapy.Request(url=url, callback=self.parse, meta={'search_keyword': artist_name,
                                                                     'url': url,
                                                                     'category': category_name,
                                                                     'list_name': list_name})

    def parse(self, response, **kwargs):

        selector = Selector(response)
        page_data = selector.xpath("//div[@class='js-store']/@data-content").extract_first()
        page_data = json.loads(page_data)

        try:
            results_count = page_data['store']['page']['data']['pagination']['totalCount']
        except KeyError:
            results_count = 20
        pages_count = results_count // self.result_per_page + 1
        for page_num in range(1, pages_count + 1):
            url = self.start_url % (page_num, format_search_word(response.meta['search_keyword']))

            yield scrapy.Request(url=url, callback=self.parse_pages, meta=response.meta)

    def parse_pages(self, response):
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

        item['url'] = result.get('url')
        item['title'] = prettify_title(result.get('title'))
        item['search_keyword'] = kwargs.get('search_keyword')
        item['parts'] = result.get('parts')
        item['duration'] = result.get('duration')
        item['pages'] = result.get('pages_count')
        item['measures'] = result.get('measures')
        item['key_signature'] = result.get('keysig')
        item['ensemble'] = result.get('description')
        item['part_names'] = ','.join(result.get('parts_names'))
        item['favourites'] = result.get('favourites_count')
        item['views'] = result.get('hits')
        item['rating'] = result.get('rating', {}).get('rating')
        item['uploaded_on'] = datetime.fromtimestamp(result.get('date_created', 0))
        item['instruments'] = ','.join(result.get('instruments'))
        item['category'] = kwargs.get('category')
        item['list_name'] = kwargs.get('list_name')

        if result.get('instrumentations'):
            instrumentations = [each.get('name') for each in result.get('instrumentations')]
            item['instrumentations'] = ','.join(instrumentations)

        return item

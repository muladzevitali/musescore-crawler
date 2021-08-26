import json
import re

import pandas
import scrapy

from ..items.genius import GeniusItem


class GeniusSpider(scrapy.Spider):
    name = 'genius'
    allowed_domains = ['genius.com']
    base_url = 'https://genius.com'
    start_url = 'https://genius.com/api/search/song?&q=%s'
    custom_settings = {
        'ITEM_PIPELINES': {
            'musescore.pipelines.genius.GeniusPipeline': 111,
        },
    }

    def start_requests(self):
        data = pandas.read_csv('genius.csv')
        for index, row in data.iterrows():
            query_word = f"{row['artist_name']} {row['song_name']}"
            url = self.start_url % query_word

            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'artist_name': row['artist_name'],
                                       'song_name': row['song_name'],
                                       'id': str(row['id'])})

    def parse(self, response, **kwargs):
        meta = json.loads(response.text)
        songs = meta['response']['sections'][0]['hits']
        next_page = meta['response']['next_page']

        for song in songs:
            artist_name = song['result']['primary_artist']['name']
            song_name = song['result']['title']
            if not artist_name.lower().strip() == response.meta['artist_name'].lower().strip():
                continue

            if not song_name.lower().strip() == response.meta['song_name'].lower().strip():
                continue

            return scrapy.Request(url=song['result']['url'], callback=self.parse_lyrics, meta=response.meta)

        if not next_page:
            return

        query_word = f"{response.meta['artist_name']} {response.meta['song_name']}"
        url = self.start_url % query_word + f'&page={next_page}'

        return scrapy.Request(url=url, callback=self.parse, meta=response.meta)

    def parse_lyrics(self, response):
        if response.text.find('id="lyrics-root"') > -1:
            lyrics = ''
            for element in response.xpath('//div[@id="lyrics-root"]/div[contains(@class, "Lyrics__Container")]'):
                lyrics_parts = element.xpath('./text()').extract()
                lyrics += '\n'.join([each.strip() for each in lyrics_parts])
        else:
            lyrics_parts = response.xpath('//div[@class="lyrics"]/descendant-or-self::text()').extract()
            lyrics = '\n'.join(lyrics_parts)

        lyrics = re.sub(r'\n+', '\n', lyrics).strip()

        item = GeniusItem()
        item['id'] = response.meta['id']
        item['artist_name'] = response.meta['artist_name']
        item['song_name'] = response.meta['song_name']
        item['lyrics'] = lyrics

        return item

import scrapy
import wikipedia

from ..items import WikipediaItem


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia_spider"
    start_url: str = 'https://en.wikipedia.org'

    def start_requests(self):

        page = wikipedia.WikipediaPage(title='Lists of musicians')

        page_selector = scrapy.Selector(text=page.html())
        elements = page_selector.xpath("//div[@class='mw-parser-output']//node()").extract()

        groups = {}

        current_header = -1
        for element_text in elements:
            if element_text == '\n':
                continue

            element = scrapy.Selector(text=element_text)
            if element.xpath('body/node()').xpath('name()').extract_first() == 'h2':
                current_header = element.xpath('.//text()').extract_first()

                continue
            list_of_li = element.xpath('.//li/a/@href').extract()
            list_of_li = [url for url in list_of_li if '/' in url]
            if not list_of_li:
                continue

            groups.setdefault(current_header, set())
            groups[current_header] = groups[current_header].union(list_of_li)

        del groups['See also']

        for group_name, group_instances in groups.items():
            for instance_url in group_instances:
                url = self.start_url + instance_url
                yield scrapy.Request(url, callback=self.parse,
                                     meta={'group_name': group_name})

    def parse(self, response, **kwargs):
        page = scrapy.Selector(response)
        artists = page.xpath("//div[@id='mw-content-text']//li/a/@title").extract()
        group_instance = page.xpath("//h1[@id='firstHeading']/text()").extract_first()

        for artist in artists:
            yield self.parse_artist(artist, group_instance=group_instance, **response.meta)

    @staticmethod
    def parse_artist(artist_name: str, **kwargs):
        artist = WikipediaItem()
        artist['artist_name'] = artist_name
        artist['group'] = kwargs.get('group_name')
        artist['group_instance'] = kwargs.get('group_instance')

        return artist

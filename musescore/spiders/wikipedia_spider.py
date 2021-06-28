import scrapy

import wikipedia


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
            for group_instance in group_instances:
                url = self.start_url + group_instance
                yield scrapy.Request(url, callback=self.parse,
                                     meta={'group_name': group_name, 'group_instance': group_instance})
                break
            break

    def parse(self, request, **kwargs):
        page = scrapy.Selector(request)
        artists = page.xpath("//div[@id='mw-content-text']//li/a/@title").extract()
        print(artists)

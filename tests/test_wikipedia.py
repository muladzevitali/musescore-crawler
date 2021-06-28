import scrapy
import wikipedia

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
    list_of_li = element.xpath('.//li/a/@title').extract()
    list_of_li = [url for url in list_of_li if '/' in url]
    if not list_of_li:
        continue

    groups.setdefault(current_header, set())
    groups[current_header] = groups[current_header].union(list_of_li)

del groups['See also']

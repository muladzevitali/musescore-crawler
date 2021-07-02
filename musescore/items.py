# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from typing import Optional

import scrapy


class MusescoreItem(scrapy.Item):
    url: str = scrapy.Field(default=None)
    title: str = scrapy.Field(default=None)
    search_keyword: str = scrapy.Field(default=None)
    parts: Optional[int] = scrapy.Field(default=None)
    duration: str = scrapy.Field(default=None)
    pages: Optional[int] = scrapy.Field(default=None)
    measures: str = scrapy.Field(default=None)
    key_signature: str = scrapy.Field(default=None)
    ensemble: str = scrapy.Field(default=None)
    part_names: str = scrapy.Field(default=None)
    favourites: Optional[int] = scrapy.Field(default=None)
    views: Optional[int] = scrapy.Field(default=None)
    rating: Optional[float] = scrapy.Field(default=None)
    uploaded_on: str = scrapy.Field(default=None)
    instruments: str = scrapy.Field(default=None)
    instrumentations: str = scrapy.Field(default=None)
    category: str = scrapy.Field(default=None)


class WikipediaItem(scrapy.Item):
    group: str = scrapy.Field(default=None)
    group_instance: str = scrapy.Field(default=None)
    artist_name: str = scrapy.Field(default=None)

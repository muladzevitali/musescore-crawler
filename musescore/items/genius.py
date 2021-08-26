import scrapy


class GeniusItem(scrapy.Item):
    id: str = scrapy.Field(default=None)
    artist_name: str = scrapy.Field(default=None)
    song_name: str = scrapy.Field(default=None)
    lyrics: str = scrapy.Field(default=None)

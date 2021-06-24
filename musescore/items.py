# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field
from typing import Optional

import scrapy


@dataclass
class MusescoreItem:
    url: str = field(default=None)
    title: str = field(default=None)
    search_keyword: str = field(default=None)
    parts: Optional[int] = field(default=None)
    duration: str = field(default=None)
    pages: Optional[int] = field(default=None)
    measures: str = field(default=None)
    key_signature: str = field(default=None)
    ensemble: str = field(default=None)
    part_names: str = field(default=None)
    favourites: Optional[int] = field(default=None)
    views: Optional[int] = field(default=None)
    rating: Optional[float] = field(default=None)
    uploaded_on: str = field(default=None)
    instruments: str = field(default=None)
    instrumentations: str = field(default=None)

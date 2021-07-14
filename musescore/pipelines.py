# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import atexit
from pathlib import Path

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from scrapy.pipelines.files import FilesPipeline

from src.scripts.utils import (drop_duplicates_in_sub_folders, merge_files_in_folder)

MUSESCORE_OUTPUT_FOLDER_PATH = Path('outputs/musescore')
MUSESCORE_WIKIPEDIA_OUTPUT_FOLDER_PATH = Path('outputs/musescore_wikipedia')
WIKIPEDIA_OUTPUT_FOLDER_PATH = Path('outputs/wikipedia')
SONGGALAXY_OUTPUT_FOLDER_PATH = Path('outputs/songgalaxy')


class MusescorePipeline:
    def __init__(self):
        self.output_folder_path = MUSESCORE_OUTPUT_FOLDER_PATH
        self.output_folder_path.mkdir(exist_ok=True, parents=True)

        atexit.register(merge_files_in_folder, self.output_folder_path, self.output_folder_path)

    def open_spider(self, spider):
        self.keyword_to_exporter = {}

    def close_spider(self, spider):
        for exporter, csv_file in self.keyword_to_exporter.values():
            exporter.finish_exporting()
            csv_file.close()

    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        keyword = adapter['search_keyword']

        if not adapter['title']:
            return
        if keyword not in self.keyword_to_exporter:
            output_file_path = self.output_folder_path.joinpath(f'{keyword}.csv')
            csv_file = open(str(output_file_path), 'wb')
            exporter = CsvItemExporter(csv_file)
            exporter.start_exporting()
            self.keyword_to_exporter[keyword] = (exporter, csv_file)

        return self.keyword_to_exporter[keyword][0]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item


class MusescoreWikipediaPipeline:
    def __init__(self):
        self.output_folder_path = MUSESCORE_WIKIPEDIA_OUTPUT_FOLDER_PATH
        self.output_folder_path.mkdir(exist_ok=True, parents=True)
        atexit.register(drop_duplicates_in_sub_folders, (MUSESCORE_WIKIPEDIA_OUTPUT_FOLDER_PATH, 'url'))

    def open_spider(self, spider):
        self.keyword_to_exporter = {}

    def close_spider(self, spider):
        for exporter, csv_file in self.keyword_to_exporter.values():
            exporter.finish_exporting()
            csv_file.close()

    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        keyword = adapter['search_keyword']
        category = adapter['category']
        list_name = adapter['list_name']
        if not adapter['title']:
            return
        if keyword not in self.keyword_to_exporter:
            output_folder = self.output_folder_path.joinpath(category).joinpath(list_name)
            output_folder.mkdir(parents=True, exist_ok=True)

            output_file_path = output_folder.joinpath(f'{keyword}.csv')
            csv_file = open(str(output_file_path), 'wb')
            exporter = CsvItemExporter(csv_file)
            exporter.start_exporting()
            self.keyword_to_exporter[keyword] = (exporter, csv_file)

        return self.keyword_to_exporter[keyword][0]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item


class WikipediaPipeline:
    def __init__(self):
        self.base_folder_path = Path('outputs/wikipedia')
        self.base_folder_path.mkdir(exist_ok=True, parents=True)

    def open_spider(self, spider):
        self.keyword_to_exporter = {}

    def close_spider(self, spider):
        for exporter, csv_file in self.keyword_to_exporter.values():
            exporter.finish_exporting()
            csv_file.close()

    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        group = adapter['group']
        keyword = adapter['group_instance']

        output_folder_path = self.base_folder_path.joinpath(group)
        output_folder_path.mkdir(parents=True, exist_ok=True)

        if keyword not in self.keyword_to_exporter:
            output_file_path = output_folder_path.joinpath(f'{keyword}.csv')
            csv_file = open(str(output_file_path), 'wb')
            exporter = CsvItemExporter(csv_file)
            exporter.start_exporting()
            self.keyword_to_exporter[keyword] = (exporter, csv_file)

        return self.keyword_to_exporter[keyword][0]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)

        return item


class SongGalaxyPipeline:
    def __init__(self):
        self.output_folder_path = SONGGALAXY_OUTPUT_FOLDER_PATH
        self.output_folder_path.mkdir(exist_ok=True, parents=True)

    def open_spider(self, spider):
        self.keyword_to_exporter = {}

    def close_spider(self, spider):
        for exporter, csv_file in self.keyword_to_exporter.values():
            exporter.finish_exporting()
            csv_file.close()

    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        keyword = adapter['search_word']

        if not adapter['song_name']:
            return
        if keyword not in self.keyword_to_exporter:
            output_file_path = self.output_folder_path.joinpath(f'{keyword}.csv')
            csv_file = open(str(output_file_path), 'wb')
            exporter = CsvItemExporter(csv_file)
            exporter.start_exporting()
            self.keyword_to_exporter[keyword] = (exporter, csv_file)

        return self.keyword_to_exporter[keyword][0]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item


class MDFileDownloadPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        md_file_url = item['md_file_url']
        for url in [md_file_url]:
            yield scrapy.Request(url=url)

    def file_path(self, request, response=None, info=None, *, item=None):
        output_folder_path = SONGGALAXY_OUTPUT_FOLDER_PATH.joinpath(item['search_word'])
        output_folder_path = output_folder_path.joinpath(item['folder_name'])

        output_folder_path.mkdir(exist_ok=True, parents=True)

        file_name = request.url.split('/')[-1]
        file_path = output_folder_path.joinpath(file_name)
        return str(file_path)

    def item_completed(self, results, item, info):
        return item

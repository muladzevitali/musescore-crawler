# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import atexit
from pathlib import Path

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter

from src.scripts.utils import drop_duplicates_in_sub_folders

MUSESCORE_OUTPUT_FOLDER_PATH = Path('outputs/musescore')
MUSESCORE_WIKIPEDIA_OUTPUT_FOLDER_PATH = Path('outputs/musescore_wikipedia')
WIKIPEDIA_OUTPUT_FOLDER_PATH = Path('outputs/wikipedia')


class MusescorePipeline:
    def __init__(self):
        self.output_folder_path = MUSESCORE_OUTPUT_FOLDER_PATH
        self.output_folder_path.mkdir(exist_ok=True, parents=True)

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

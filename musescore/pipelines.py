# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from pathlib import Path


class MusescorePipeline:
    def __init__(self):
        self.output_folder_path = Path('outputs')
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
        if keyword not in self.keyword_to_exporter:
            output_file_path = self.output_folder_path.joinpath(f'{keyword}.csv')
            csv_file = open(str(output_file_path), 'wb')
            exporter = CsvItemExporter(csv_file)
            exporter.start_exporting()
            self.keyword_to_exporter[keyword] = (exporter, csv_file)

        return self.keyword_to_exporter[keyword][0]

    def process_item(self, item, spider):
        print(item)
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item

from pathlib import Path

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter

GENIUS_OUTPUT_FOLDER_PATH = Path('outputs/genius')


class GeniusPipeline:
    def __init__(self):
        self.output_folder_path = GENIUS_OUTPUT_FOLDER_PATH
        self.output_folder_path.mkdir(exist_ok=True, parents=True)

    def open_spider(self, spider):
        self.keyword_to_exporter = {}

    def close_spider(self, spider):
        for exporter, csv_file in self.keyword_to_exporter.values():
            exporter.finish_exporting()
            csv_file.close()

    def _exporter_for_item(self, item):
        adapter = ItemAdapter(item)
        keyword = adapter['id']

        if not adapter['id']:
            return

        song_folder = self.output_folder_path.joinpath(adapter['id'])
        song_folder.mkdir(exist_ok=True, parents=True)
        song_lyrics_file = song_folder.joinpath('lyrics.txt')

        with open(str(song_lyrics_file), 'w') as output_stream:
            output_stream.write(adapter['lyrics'])

        if keyword not in self.keyword_to_exporter:
            output_file_path = self.output_folder_path.joinpath('overall.csv')
            csv_file = open(str(output_file_path), 'wb')
            exporter = CsvItemExporter(csv_file)
            exporter.start_exporting()
            self.keyword_to_exporter[keyword] = (exporter, csv_file)

        return self.keyword_to_exporter[keyword][0]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item

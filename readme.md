# Python parser for <i>musescore.com</i>

### Usage

* Install the dependencies:

```bash
pip install -r requirements.txt
```

* Change search keywords in the file musicians.csv under the column: <b>name</b>

* Run crawler:

```bash
scrapy crawl wikipedia_spider
scrapy crawl musescore_wikipedia_spider
scrapy crawl musescore_spider
scrapy crawl songgalaxy_spider
```

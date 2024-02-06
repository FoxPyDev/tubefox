from web_scraper import WebScraper
from app_scraper import AppScraper
from data_collector import DataCollector


class TubeFox:
    def __init__(self, url):
        self.url = url
        self.collected_data = DataCollector(WebScraper(self.url).data_dict)
        self.app_data_dict = AppScraper(self.collected_data.collect_metadata()['id'])

    @property
    def id(self):
        return self.collected_data.collect_metadata().get('id', '')

    @property
    def title(self):
        return self.collected_data.collect_metadata().get('title', '')

    @property
    def description(self):
        return self.collected_data.collect_metadata().get('description', '')

    @property
    def keywords(self):
        keywords = self.collected_data.collect_metadata().get('keywords', [])
        return ', '.join(keywords)


if __name__ == "__main__":
    yt = TubeFox('https://www.youtube.com/watch?v=CV7MuLeBKgE&ab_channel=AdrianZP')
    print(yt.id)
    print(yt.title)
    print(yt.description)
    print(yt.keywords)

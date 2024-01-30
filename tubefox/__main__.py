from web_scraper import WebScraper
from app_scraper import AppScraper
from metadata import Metadata


class TubeFox:
    def __init__(self, url):
        self.url = url
        self.web_data_dict = WebScraper(self.url).get_data()
        self.videoid = Metadata(self.web_data_dict).id
        self.app_data_dict = AppScraper(self.videoid).get_page_source()


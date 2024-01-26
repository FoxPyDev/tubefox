import re
import json
import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, video_url):
        self.video_url = video_url
        self.data_dict = self._get_data()

    def _get_page_source(self):
        try:
            response = requests.get(self.video_url)
            if response.status_code == 200:
                return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException:
            pass
        return None

    def _get_data(self):
        page_source = self._get_page_source()
        if page_source:
            script_tag = page_source.find('script', string=re.compile(r'ytInitialPlayerResponse'))
            json_match = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?})\s*;', script_tag.text)
            json_text = json_match.group(1)
            json_data = json.loads(json_text)
            return dict(json_data)


if __name__ == "__main__":
    pass

import re
import json
import requests
from bs4 import BeautifulSoup


class WebScraper:
    """
    WebScraper class for scraping data from a YouTube video webpage.

    Args:
        video_url (str): The URL of the YouTube video.

    Attributes:
        video_url (str): The URL of the YouTube video.
        data_dict (dict): A dictionary containing the scraped data.

    Note:
        This class uses BeautifulSoup and regular expressions to parse the HTML content of the webpage.
    """

    def __init__(self, video_url: str) -> None:
        self.video_url: str = video_url
        self.data_dict: dict = self.get_data

    def _get_page_source(self) -> BeautifulSoup:
        """
        Method to retrieve the HTML source code of the webpage.

        Returns:
            BeautifulSoup: A BeautifulSoup object containing the parsed HTML of the webpage,
                           or None if the request fails.
        """
        try:
            response = requests.get(self.video_url)
            if response.status_code == 200:
                return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException:
            pass
        return None

    @property
    def get_data(self) -> dict:
        """
        Method to extract relevant data from the webpage.

        Returns:
            dict: A dictionary containing the extracted data,
                  or None if the webpage content cannot be parsed.
        """
        page_source = self._get_page_source()
        if page_source:
            script_tag = page_source.find('script', string=re.compile(r'ytInitialPlayerResponse'))
            json_match = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?})\s*;', script_tag.text)
            json_text = json_match.group(1)
            json_data = json.loads(json_text)
            return dict(json_data)

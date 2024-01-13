import re
import json
import requests
from bs4 import BeautifulSoup

""" 
TubeFox is a lightweight and easy-to-use module for retrieving information about YouTube videos, 
such as title, description, tags, and for downloading videos and video thumbnails. 
The module is built on top of the requests and beautifulsoup4 libraries. 
"""


class TubeFox:
    def __init__(self, video_url):
        """
        Initializes a TubeFox instance with the provided YouTube video URL.
        Parameters:
            video_url (str): The URL of the YouTube video.
        The method starts by storing the provided video URL as an instance variable.
        It then attempts to make an HTTP GET request to the video URL using the 'requests' library.
        If the response status code is 200 (OK), it proceeds to parse the HTML content of the page
        using BeautifulSoup with the "html.parser" parser.
        If the response status code is not 200 or an exception occurs during the request, the 'page_html'
        attribute is set to None.
        Subsequently, the method initializes the 'video_details' attribute by calling the 'get_all_data_in_dict'
        method, extracting the 'videoDetails' information from the 'ytInitialPlayerResponse' JSON on the YouTube page.
        Attributes:
            video_url (str): The YouTube video URL.
            page_html (BeautifulSoup): Parsed HTML content of the YouTube video page.
            None if the request or parsing fails.
            video_details (dict): Parsed video details extracted from the 'ytInitialPlayerResponse' JSON.
                                 An empty dictionary if details are not available or parsing fails.
        """
        self.video_url = video_url
        try:
            response = requests.get(self.video_url)
            if response.status_code == 200:
                self.page_html = BeautifulSoup(response.content, "html.parser")
            else:
                self.page_html = None
        except requests.RequestException:
            self.page_html = None
        self.video_details = self.get_all_data_in_dict().get('videoDetails', {})

    def get_all_data_in_dict(self):
        """
        Extracts and returns various data from a YouTube page's HTML content in the form of a dictionary.

        This function specifically looks for a <script> tag containing the 'ytInitialPlayerResponse' string
        in the provided HTML (presumably representing a YouTube video page). It then uses regular expressions
        to locate and extract the JSON data associated with 'ytInitialPlayerResponse'. The extracted JSON text
        is then loaded into a Python dictionary using the `json.loads` function.

        Returns:
            dict: A dictionary containing the parsed data from the 'ytInitialPlayerResponse' JSON on the YouTube page.

        """
        script_tag = self.page_html.find('script', string=re.compile(r'ytInitialPlayerResponse'))
        json_match = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?})\s*;', script_tag.text)
        json_text = json_match.group(1)
        json_data = json.loads(json_text)
        return dict(json_data)

    def get_video_download_links(self):
        pass

    def get_thumbnail_download_links(self):
        pass

    def get_audio_download_links(self):
        pass

    def get_subtitles_download_links(self):
        pass

    @property
    def videoid(self):
        """
        Property representing the video ID extracted from the video details.
        Returns an empty string if the video ID is not available.
        """
        return self.video_details.get('videoId', '')

    @property
    def title(self):
        """
        Property representing the title of the video extracted from the video details.
        Returns an empty string if the title is not available.
        """
        return self.video_details.get('title', '')

    @property
    def description(self):
        """
        Property representing the short description of the video extracted from the video details.
        Returns an empty string if the description is not available.
        """
        return self.video_details.get('shortDescription', '')

    @property
    def keywords(self):
        """
        Property representing the keywords of the video extracted from the video details.
        Returns a comma-separated string of keywords. Returns an empty string if keywords are not available.
        """
        keywords = self.video_details.get('keywords', [])
        return ', '.join(keywords)


if __name__ == "__main__":
    yt = TubeFox('https://www.youtube.com/watch?v=EHi0RDZ31VA')
    print(yt.videoid)
    print(yt.title)
    print(yt.description)
    print(yt.keywords)

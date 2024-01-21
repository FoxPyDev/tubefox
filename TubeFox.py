import os
import re
import json
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from Helper import clean_filename

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
        self.page_html = self._get_page_html()
        self.video_details = self.get_all_data_in_dict().get('videoDetails', {})

    def _get_page_html(self):
        """
        Retrieves and returns the parsed HTML content of the YouTube video page.

        This method is called during the initialization to make an HTTP GET request to the video URL
        and parse the HTML content using BeautifulSoup.

        Returns:
            BeautifulSoup: Parsed HTML content of the YouTube video page.
                           None if the request or parsing fails.
        """
        try:
            response = requests.get(self.video_url)
            if response.status_code == 200:
                return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException:
            pass
        return None

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

    @property
    def generate_filename(self):
        return clean_filename(self.title)

    @property
    def get_video_download_links(self):
        """
            Retrieves the download links for video streams with various qualities.

            This property sends a POST request to the YouTube API endpoint to obtain video streaming data.
            It includes information such as video quality, format, and download links. The response is then
            processed to extract and return a dictionary where keys represent the video quality (height) and
            values are the corresponding download links.

            Returns:
                dict: A dictionary where keys represent the video quality (height),
                and values are the associated download links.

            Note:
                The method relies on the 'requests' library to communicate with the YouTube API.
                The API key, user-agent, and payload information are used to authenticate and request the required data.
                The returned dictionary may include various video qualities, and the 'N/A' placeholder is used
                for cases where the quality information is not available.

            Example:
                If the video has streaming data for 720p and 1080p qualities, the returned dictionary may look like:
                {
                    '720p': 'https://example.com/video_720p.mp4',
                    '1080p': 'https://example.com/video_1080p.mp4',
                }
            """
        url = 'https://www.youtube.com/youtubei/v1/player?key=AIzaSyA8eiZmM1FaDVjRy-df2KTyQ_vz_yYM39w'

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; GB) gzip'
        }

        payload = {
            "videoId": f'{self.videoid}',
            "context": {
                "client": {
                    "clientName": "ANDROID",
                    "clientVersion": "17.10.35",
                    "androidSdkVersion": 30
                }
            }
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        data = response.json()
        video_links = data.get('streamingData', {}).get('formats', [])
        video_links_dict = {link.get('height', 'N/A'): link.get('url', '') for link in video_links}
        return video_links_dict

    @property
    def get_thumbnail_download_links(self):
        """
        Property that fetches a dictionary of thumbnail download links with their corresponding quality.

        Returns:
            dict: A dictionary where keys represent thumbnail quality, and values are the associated download links.
        """
        thumbnail_links = self.get_all_data_in_dict().get('videoDetails', {}).get('thumbnail', {}).get('thumbnails', [])
        return {thumbnail.get('height', 'N/A'): thumbnail.get('url', '') for thumbnail in thumbnail_links}

    @property
    def get_audio_download_links(self):
        """
        Property that obtains a dictionary of audio download links and their corresponding bitrate.

        Returns:
            dict: A dictionary where keys represent audio bitrate, and values are the associated download links.
        """
        audios = self.get_all_data_in_dict().get('streamingData', {}).get('adaptiveFormats', [])
        return {link.get('bitrate', 'N/A'): link.get('url', '') for link in audios if
                "audio/" in link.get('mimeType', '')}

    @property
    def get_subtitles_download_links(self):
        """
        Property that obtains a dictionary of subtitles download links and their corresponding language.

        Returns:
            dict: A dictionary where keys represent subtitle language, and values are the associated download links.
        """
        subtitles = self.get_all_data_in_dict().get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get(
            'captionTracks', [])
        return {el.get('name', {}).get('simpleText', 'N/A'): el.get('baseUrl', '') for el in subtitles}

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

    def _download_file(self, path, filename, file_type, best_quality_link, extension, chunk_size=1024):
        """
        Downloads a file with the best available quality and displays information about the process.

        Parameters:
            path (str): Path where the file will be saved.
            filename (str): Name of the file to be saved.
            file_type (str): Type of the file ('video', 'thumbnail', 'audio').
            best_quality_link (str): Link to the file with the best quality.
            extension (str): File extension ('mp4', 'jpg', 'mp3').
            chunk_size (int): Size of each chunk for download. Defaults to 1024 bytes.

        Returns:
            None
        """
        # Check if the link is empty or None
        if not best_quality_link:
            print(f"No {file_type} download link available.")
            return

        if not filename:
            filename = self.generate_filename

        if not path:
            path = os.getcwd()

        response = requests.get(best_quality_link, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        print(f"Start download {file_type}")
        with open(f'{path}{filename}.{extension}', 'wb') as file, tqdm(
                desc=f"{filename}.{extension}", total=total_size, unit='B', unit_scale=True
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))
        print(f"{file_type} downloaded")

    def download_video(self, path=None, filename=None, chunk_size=1024):
        """
        Downloads the video with the best available quality.

        Parameters:
            path (str): Path where the file will be saved.
            filename (str): Name of the file to be saved.
            chunk_size (int): Size of each chunk for download. Defaults to 1024 bytes.

        Returns:
            None
        """
        best_quality_link = self.get_video_download_links[max(self.get_video_download_links.keys())]
        self._download_file(path, filename, 'Video', best_quality_link, 'mp4', chunk_size)

    def download_thumbnail(self, path=None, filename=None, chunk_size=1024):
        """
        Downloads the thumbnail image with the best available quality.

        Parameters:
            path (str): Path where the file will be saved.
            filename (str): Name of the file to be saved.
            chunk_size (int): Size of each chunk for download. Defaults to 1024 bytes.

        Returns:
            None
        """
        best_quality_link = self.get_thumbnail_download_links[max(self.get_thumbnail_download_links.keys())]
        self._download_file(path, filename, 'Thumbnail', best_quality_link, 'jpg', chunk_size)

    def download_audio(self, path=None, filename=None, chunk_size=1024):
        """
        Downloads the audio with the best available quality.

        Parameters:
            path (str): Path where the file will be saved.
            filename (str): Name of the file to be saved.
            chunk_size (int): Size of each chunk for download. Defaults to 1024 bytes.

        Returns:
            None
        """
        best_quality_link = self.get_audio_download_links[max(self.get_audio_download_links.keys())]
        self._download_file(path, filename, 'Audio', best_quality_link, 'mp3', chunk_size)

    def download_subtitles(self, path=None):
        """
        Downloads subtitle files associated with the YouTube video in various languages.

        The method retrieves a dictionary of subtitle download links and their corresponding language
        using the 'ytInitialPlayerResponse' JSON on the YouTube page. It then downloads each subtitle file and
        saves it with the format "{language} - {cleaned_video_title}.xml" in the current directory.
        """
        if not path:
            path = os.getcwd()

        subtitles_dict = self.get_subtitles_download_links
        for subtitle in subtitles_dict:
            response = requests.get(subtitles_dict[subtitle]).content
            with open(f"{path}{subtitle} - {self.generate_filename}.xml", "wb") as xml:
                xml.write(response)
                print(f"{subtitle} subtitle saved")


if __name__ == "__main__":
    yt = TubeFox('https://www.youtube.com/watch?v=YOUR_VIDEO_ID')
    print(yt.videoid)
    print(yt.title)
    print(yt.description)
    print(yt.keywords)
    print(yt.get_video_download_links)
    print(yt.get_thumbnail_download_links)
    print(yt.get_subtitles_download_links)
    print(yt.get_audio_download_links)
    yt.download_video()
    yt.download_thumbnail()
    yt.download_audio()
    yt.download_subtitles()

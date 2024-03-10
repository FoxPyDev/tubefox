import json
import requests
from typing import Dict, Union
from tubefox.yt_app_version_updater import get_yt_app_latest_version


class AppScraper:
    """
    AppScraper class for scraping data related to a YouTube video using an external API.

    Args:
        video_id (str): The ID of the YouTube video.

    Attributes:
        video_id (str): The ID of the YouTube video.
        data_dict (dict): A dictionary containing the scraped data.

    Raises:
        requests.RequestException: If an error occurs while making the API request.

    Note:
        This class requires a 'config.ini' file to be present in the same directory,
        containing necessary configuration parameters such as 'api_url', 'api_key', and 'headers'.
    """

    latest_version = get_yt_app_latest_version()
    version_to_use = '19.08.36' if latest_version is None else latest_version

    def __init__(self, video_id: str) -> None:
        self.video_id: str = video_id
        self.data_dict = self.get_data

    @property
    def get_data(self) -> Dict[str, Union[str, int, Dict[str, Union[str, int]]]]:
        """
        Method to fetch data related to the video from an external API.

        Returns:
            dict: A dictionary containing the scraped data, or None if the request fails.
        """
        api_url = 'https://www.youtube.com/youtubei/v1/player?key='
        api_key = 'AIzaSyA8eiZmM1FaDVjRy-df2KTyQ_vz_yYM39w'
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'com.google.android.youtube/{AppScraper.version_to_use} (Linux; U; Android 12; GB) gzip'
        }

        try:
            payload = {
                "videoId": f'{self.video_id}',
                "context": {
                    "client": {
                        "clientName": "ANDROID",
                        "clientVersion": f"{AppScraper.version_to_use}",
                        "androidSdkVersion": 30
                    }
                }
            }

            response = requests.post(api_url+api_key, data=json.dumps(payload), headers=headers)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return {}

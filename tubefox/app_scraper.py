import json
import requests
import configparser
import ast


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

    def __init__(self, video_id: str) -> None:
        self.video_id: str = video_id
        self.data_dict: dict = self.get_data

    @property
    def get_data(self) -> dict:
        """
        Method to fetch data related to the video from an external API.

        Returns:
            dict: A dictionary containing the scraped data, or None if the request fails.
        """
        config = configparser.ConfigParser()
        config.read('config.ini')
        api_url = config.get('Settings', 'api_url')
        api_key = config.get('Settings', 'api_key')
        headers_str = config.get('Settings', 'headers')
        headers = ast.literal_eval(headers_str)

        try:
            payload = {
                "videoId": f'{self.video_id}',
                "context": {
                    "client": {
                        "clientName": "ANDROID",
                        "clientVersion": "17.10.35",
                        "androidSdkVersion": 30
                    }
                }
            }

            response = requests.post(api_url+api_key, data=json.dumps(payload), headers=headers)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return None

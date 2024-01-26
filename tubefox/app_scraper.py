from metadata import Metadata
import json
import requests
import configparser
import ast


class AppScraper(Metadata):
    def __init__(self, video_url):
        super().__init__(video_url)
        self.video_id = self.id

    def _get_page_source(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        api_url = config.get('Settings', 'api_url')
        api_key = config.get('Settings', 'api_key')
        headers_str = config.get('Settings', 'headers')
        headers = ast.literal_eval(headers_str)

        try:
            payload = {
                "videoId": f'{self.id}',
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
                return {response.json()}
        except requests.RequestException:
            pass
        return None


if __name__ == "__main__":
    pass
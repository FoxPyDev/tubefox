from web_scraper import WebScraper
from app_scraper import AppScraper


class DataCollector:
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def collect_metadata(self):
        video_info = {
            'id': self.data_dict.get('videoDetails', {}).get('videoId', ''),
            'title': self.data_dict.get('videoDetails', {}).get('title', ''),
            'description': self.data_dict.get('videoDetails', {}).get('shortDescription', ''),
            'keywords': self.data_dict.get('videoDetails', {}).get('keywords', ''),
        }
        return video_info

    def collect_subtitles_links(self):
        subtitles = self.data_dict.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get(
            'captionTracks', [])
        return {el.get('name', {}).get('simpleText', 'N/A'): el.get('baseUrl', '') for el in subtitles}

    def collect_video_links(self):
        videos = self.data_dict.get('streamingData', {}).get('formats', [])
        return {link.get('height', 'N/A'): link.get('url', '') for link in videos}

    def collect_muted_video_links(self):
        muted_videos = self.data_dict.get('streamingData', {}).get('adaptiveFormats', [])
        return {link.get('height', 'N/A'): link.get('url', '') for link in muted_videos if
                "video/mp4" in link.get('mimeType', '')}

    def collect_audio_links(self):
        audios = self.data_dict.get('streamingData', {}).get('adaptiveFormats', [])
        return {link.get('bitrate', 'N/A'): link.get('url', '') for link in audios if
                "audio/mp4" in link.get('mimeType', '')}

    def collect_thumbnail_links(self):
        thumbnail_links = self.data_dict.get('videoDetails', {}).get('thumbnail', {}).get('thumbnails', [])
        return {thumbnail.get('height', 'N/A'): thumbnail.get('url', '') for thumbnail in thumbnail_links}


if __name__ == "__main__":
    web = WebScraper("https://www.youtube.com/watch?v=VX-mp48z-Rg")
    app = AppScraper("VX-mp48z-Rg")
    data1 = DataCollector(web.data_dict)
    data2 = DataCollector(app.data_dict)
    print(data1.collect_subtitles_links())
    print(data2.collect_subtitles_links())
    # print(data1.collect_audio_links())
    # print(data2.collect_audio_links())
    # print(data1.collect_thumbnail_links())
    # print(data2.collect_thumbnail_links())
    # print(data1.collect_muted_video_links())
    # print(data2.collect_muted_video_links())

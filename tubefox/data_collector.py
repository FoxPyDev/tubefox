class DataCollector:
    """
    DataCollector class for extracting various metadata and links from a YouTube video data dictionary.

    Args:
        data_dict (dict): A dictionary containing data related to a YouTube video.

    Attributes:
        data_dict (dict): A dictionary containing data related to a YouTube video.

    Methods:
        collect_metadata: Extract metadata such as video ID, title, description, and keywords.
        collect_subtitles_links: Extract links to subtitles associated with the video.
        collect_video_links: Extract links to video streams of different qualities.
        collect_muted_video_links: Extract links to muted video streams of different qualities.
        collect_audio_links: Extract links to audio streams of different qualities.
        collect_thumbnail_links: Extract links to thumbnails of different sizes.

    Note:
        This class assumes that the input dictionary follows the structure of a YouTube video data response.
    """

    def __init__(self, data_dict: dict) -> None:
        """
        Initializes the DataCollector with a data dictionary.

        Args:
            data_dict (dict): A dictionary containing data related to a YouTube video.
        """
        self.data_dict: dict = data_dict

    def collect_metadata(self) -> dict:
        """
        Extract metadata such as video ID, title, description, and keywords.

        Returns:
            dict: A dictionary containing video metadata.
        """
        video_info = {
            'id': self.data_dict.get('videoDetails', {}).get('videoId', ''),
            'title': self.data_dict.get('videoDetails', {}).get('title', ''),
            'description': self.data_dict.get('videoDetails', {}).get('shortDescription', ''),
            'keywords': self.data_dict.get('videoDetails', {}).get('keywords', ''),
        }
        return video_info

    def collect_subtitles_links(self) -> dict:
        """
        Extract links to subtitles associated with the video.

        Returns:
            dict: A dictionary mapping subtitle names to their corresponding URLs.
        """
        subtitles = self.data_dict.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get(
            'captionTracks', [])
        return {el.get('name', {}).get('simpleText', 'N/A'): el.get('baseUrl', '') for el in subtitles}

    def collect_muted_video_links(self) -> dict:
        """
        Collect muted video links from the streaming data.

        Returns:
            dict: A dictionary mapping video heights to dictionaries with video information.
                  Example:
                  {
                      720: {
                          'url': 'http://example.com/video1',
                          'mimeType': 'video/mp4; codecs="av01.0"',
                          'format': 'mp4'
                      },
                      1080: {
                          'url': 'http://example.com/video2',
                          'mimeType': 'video/webm; codecs="vp9"',
                          'format': 'webm'
                      }
                  }
        """
        videos = self.data_dict.get('streamingData', {}).get('adaptiveFormats', [])
        result = {}
        for video in videos:
            if 'video/mp4; codecs="av01.0' in video['mimeType']:
                format_type = "mp4"
            elif 'video/webm; codecs="vp9' in video['mimeType']:
                format_type = "webm"
            else:
                continue

            result[video['height']] = {
                'url': video['url'],
                'mimeType': video['mimeType'],
                'format': format_type
            }
        return result

    def collect_video_links(self) -> dict:
        """
        Extract links to video streams of different qualities.

        Returns:
            dict: A dictionary mapping video heights to dictionaries with video information.
        """
        videos = self.data_dict.get('streamingData', {}).get('formats', [])
        result = {}
        for video in videos:
            result[video['height']] = {
                'url': video['url'],
                'mimeType': video['mimeType'],
                'format': 'mp4',
                'full_video': 'ok',
            }
        return result

    def collect_audio_links(self) -> dict:
        """
        Extract links to audio streams of different qualities.

        Returns:
            dict: A dictionary mapping bitrates to dictionaries with audio information.
        """
        audios = self.data_dict.get('streamingData', {}).get('adaptiveFormats', [])
        result = {}
        for audio in audios:
            if 'mp4a' in audio['mimeType']:
                format_type = "mp4a"
            elif 'opus' in audio['mimeType']:
                format_type = "opus"
            else:
                continue

            result[audio['bitrate']] = {
                'url': audio['url'],
                'mimeType': audio['mimeType'],
                'format': format_type
            }
        return result

    def collect_thumbnail_links(self) -> dict:
        """
        Extract links to thumbnails of different sizes.

        Returns:
            dict: A dictionary mapping thumbnail sizes to their corresponding URLs with format 'jpg'.
        """
        thumbnail_links = self.data_dict.get('videoDetails', {}).get('thumbnail', {}).get('thumbnails', [])
        return {
            thumbnail.get('height', 'N/A'): {
                'url': thumbnail.get('url', ''),
                'format': 'jpg'
            } for thumbnail in thumbnail_links
        }
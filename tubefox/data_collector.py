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

    def collect_video_links(self) -> dict:
        """
        Extract links to video streams of different qualities.

        Returns:
            dict: A dictionary mapping video qualities to their corresponding URLs.
        """
        videos = self.data_dict.get('streamingData', {}).get('formats', [])
        return {link.get('height', 'N/A'): link.get('url', '') for link in videos}

    def collect_muted_video_links(self) -> dict:
        """
        Extract links to muted video streams of different qualities.

        Returns:
            dict: A dictionary mapping video qualities to their corresponding URLs.
        """
        muted_videos = self.data_dict.get('streamingData', {}).get('adaptiveFormats', [])
        return {link.get('height', 'N/A'): link.get('url', '') for link in muted_videos if
                "video/mp4" in link.get('mimeType', '')}

    def collect_audio_links(self) -> dict:
        """
        Extract links to audio streams of different qualities.

        Returns:
            dict: A dictionary mapping audio qualities to their corresponding URLs.
        """
        audios = self.data_dict.get('streamingData', {}).get('adaptiveFormats', [])
        return {link.get('bitrate', 'N/A'): link.get('url', '') for link in audios if
                "audio/mp4" in link.get('mimeType', '')}

    def collect_thumbnail_links(self) -> dict:
        """
        Extract links to thumbnails of different sizes.

        Returns:
            dict: A dictionary mapping thumbnail sizes to their corresponding URLs.
        """
        thumbnail_links = self.data_dict.get('videoDetails', {}).get('thumbnail', {}).get('thumbnails', [])
        return {thumbnail.get('height', 'N/A'): thumbnail.get('url', '') for thumbnail in thumbnail_links}

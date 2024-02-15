from typing import Optional

from tubefox.web_scraper import WebScraper
from tubefox.app_scraper import AppScraper
from tubefox.data_collector import DataCollector
from tubefox.downloader import Downloader
from tubefox.subtitles import Subtitles
from tubefox.subtitles import save_subtitle
from tubefox.helpers import clean_filename


class TubeFox:
    """
    TubeFox is a wrapper class that provides convenient methods for scraping data, downloading media,
    and managing subtitles from YouTube videos.

    Args:
        url (str): The URL of the YouTube video.
    """

    def __init__(self, url: str) -> None:
        self.url: str = url
        self.web_collected_data: DataCollector = DataCollector(WebScraper(self.url).data_dict)
        self.app_collected_data: DataCollector = DataCollector(
            AppScraper(self.web_collected_data.collect_metadata()['id']).data_dict)

    @property
    def id(self) -> str:
        """Return the video ID."""
        return self.web_collected_data.collect_metadata().get('id', '')

    @property
    def title(self) -> str:
        """Return the video title."""
        return self.web_collected_data.collect_metadata().get('title', '')

    @property
    def description(self) -> str:
        """Return the video description."""
        return self.web_collected_data.collect_metadata().get('description', '')

    @property
    def keywords(self) -> str:
        """Return the video keywords as a comma-separated string."""
        keywords = self.web_collected_data.collect_metadata().get('keywords', [])
        return ', '.join(keywords)

    def download_video(self, filename: Optional[str] = None, path: Optional[str] = None,
                       quality: Optional[int] = None) -> None:
        """
        Download the video.

        Args:
            filename (str, optional): The name of the downloaded video file. If not provided,
            the video title will be used.
            path (str, optional): The path where the downloaded file will be saved. Defaults to current directory.
            quality (int, optional): The desired quality of the video. Defaults to the highest available quality.
        """
        best_quality_link = self.app_collected_data.collect_video_links()[max(
            self.app_collected_data.collect_video_links().keys())]
        if quality is None:
            download_link = best_quality_link
        else:
            download_link = self.app_collected_data.collect_video_links().get(int(quality))
        if path is None:
            path = "./"
        if filename is None:
            filename = clean_filename(self.title)

        Downloader(filename=filename,
                   download_link=download_link,
                   path=path,
                   file_type='video',
                   extension='mp4').download_file()

    def download_muted_video(self, filename: Optional[str] = None, path: Optional[str] = None,
                             quality: Optional[int] = None) -> None:
        """
        Download the video without audio.

        Args:
            filename (str, optional): The name of the downloaded video file. If not provided,
            the video title will be used.
            path (str, optional): The path where the downloaded file will be saved. Defaults to current directory.
            quality (int, optional): The desired quality of the video. Defaults to the highest available quality.
        """
        best_quality_link = self.app_collected_data.collect_muted_video_links()[max(
            self.app_collected_data.collect_muted_video_links().keys())]
        if quality is None:
            download_link = best_quality_link
        else:
            download_link = self.app_collected_data.collect_muted_video_links().get(int(quality))
        if path is None:
            path = "./"
        if filename is None:
            filename = clean_filename(self.title)

        Downloader(filename=filename,
                   download_link=download_link,
                   path=path,
                   file_type='video',
                   extension='mp4').download_file()

    def download_audio(self, filename: Optional[str] = None, path: Optional[str] = None,
                       quality: Optional[int] = None) -> None:
        """
        Download the audio track of the video.

        Args:
            filename (str, optional): The name of the downloaded audio file. If not provided,
            the video title will be used.
            path (str, optional): The path where the downloaded file will be saved. Defaults to current directory.
            quality (int, optional): The desired quality of the audio. Defaults to the highest available quality.
        """
        best_quality_link = self.app_collected_data.collect_audio_links()[max(
            self.app_collected_data.collect_audio_links().keys())]
        if quality is None:
            download_link = best_quality_link
        else:
            download_link = self.app_collected_data.collect_audio_links().get(int(quality))
        if path is None:
            path = "./"
        if filename is None:
            filename = clean_filename(self.title)

        Downloader(filename=filename,
                   download_link=download_link,
                   path=path,
                   file_type='audio',
                   extension='mp3').download_file()

    def download_thumbnail(self, filename: Optional[str] = None, path: Optional[str] = None,
                           quality: Optional[int] = None) -> None:
        """
        Download the video thumbnail.

        Args:
            filename (str, optional): The name of the downloaded thumbnail file. If not provided,
            the video title will be used.
            path (str, optional): The path where the downloaded file will be saved. Defaults to current directory.
            quality (int, optional): The desired quality of the thumbnail. Defaults to the highest available quality.
        """
        best_quality_link = self.web_collected_data.collect_thumbnail_links()[max(
            self.web_collected_data.collect_thumbnail_links().keys())]
        if quality is None:
            download_link = best_quality_link
        else:
            download_link = self.web_collected_data.collect_thumbnail_links().get(int(quality))

        if path is None:
            path = "./"
        if filename is None:
            filename = clean_filename(self.title)

        Downloader(
            filename=filename,
            download_link=download_link,
            path=path,
            file_type='thumbnail',
            extension='jpg').download_file()

    def download_subtitles(self, mode: Optional[str] = None, filename: Optional[str] = None,
                           path: Optional[str] = None) -> None:
        """
        Download subtitles of the video.

        Args:
            mode (str, optional): The format of subtitles to download ('srt' or 'txt'). Defaults to 'txt'.
            filename (str, optional): The name of the downloaded subtitles file. If not provided,
            the video title will be used.
            path (str, optional): The path where the downloaded file will be saved. Defaults to current directory.
        """
        if path is None:
            path = "./"
        if filename is None:
            filename = clean_filename(self.title)

        for subtitle in self.web_collected_data.collect_subtitles_links():
            if mode == 'srt':
                subtitle_text = Subtitles(self.web_collected_data.collect_subtitles_links()[subtitle]).subtitles_to_srt
                save_subtitle(subtitle=subtitle_text, path=path,
                              filename=f'{filename} - {subtitle}',
                              filetype='srt')
            else:
                subtitle_text = Subtitles(self.web_collected_data.collect_subtitles_links()[subtitle]).subtitles_to_text
                save_subtitle(subtitle=subtitle_text, path=path,
                              filename=f'{filename} - {subtitle}',
                              filetype='txt')

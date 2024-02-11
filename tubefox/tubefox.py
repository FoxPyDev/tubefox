from web_scraper import WebScraper
from app_scraper import AppScraper
from data_collector import DataCollector
from downloader import Downloader
from subtitles import Subtitles
from subtitles import save_subtitle
from helpers import clean_filename


class TubeFox:
    def __init__(self, url):
        self.url = url
        self.web_collected_data = DataCollector(WebScraper(self.url).data_dict)
        self.app_collected_data = DataCollector(AppScraper(self.web_collected_data.collect_metadata()['id']).data_dict)

    @property
    def id(self):
        return self.web_collected_data.collect_metadata().get('id', '')

    @property
    def title(self):
        return self.web_collected_data.collect_metadata().get('title', '')

    @property
    def description(self):
        return self.web_collected_data.collect_metadata().get('description', '')

    @property
    def keywords(self):
        keywords = self.web_collected_data.collect_metadata().get('keywords', [])
        return ', '.join(keywords)

    def download_video(self, filename=None, path=None, quality=None):
        best_quality_link = yt.app_collected_data.collect_video_links()[max(
            yt.app_collected_data.collect_video_links().keys())]
        if quality is None:
            download_link = best_quality_link
        else:
            download_link = yt.app_collected_data.collect_video_links().get(int(quality))
        if path is None:
            path = "./"
        if filename is None:
            filename = clean_filename(self.title)

        Downloader(filename=filename,
                   download_link=download_link,
                   path=path,
                   file_type='video',
                   extension='mp4').download_file()

    def download_muted_video(self, filename=None, path=None, quality=None):
        best_quality_link = yt.app_collected_data.collect_muted_video_links()[max(
                yt.app_collected_data.collect_muted_video_links().keys())]
        if quality is None:
            download_link = best_quality_link
        else:
            download_link = yt.app_collected_data.collect_muted_video_links().get(int(quality))
        if path is None:
            path = "./"
        if filename is None:
            filename = clean_filename(self.title)

        Downloader(filename=filename,
                   download_link=download_link,
                   path=path,
                   file_type='video',
                   extension='mp4').download_file()

    def download_audio(self, filename=None, path=None, quality=None):
        best_quality_link = yt.app_collected_data.collect_audio_links()[max(
                yt.app_collected_data.collect_audio_links().keys())]
        if quality is None:
            download_link = best_quality_link
        else:
            download_link = yt.app_collected_data.collect_audio_links().get(int(quality))
        if path is None:
            path = "./"
        if filename is None:
            filename = clean_filename(self.title)

        Downloader(filename=filename,
                   download_link=download_link,
                   path=path,
                   file_type='audio',
                   extension='mp3').download_file()

    def download_thumbnail(self, filename=None, path=None, quality=None):
        best_quality_link = yt.web_collected_data.collect_thumbnail_links()[max(
                yt.web_collected_data.collect_thumbnail_links().keys())]
        if quality is None:
            download_link = best_quality_link
        else:
            download_link = yt.web_collected_data.collect_thumbnail_links().get(int(quality))

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

    def download_subtitles(self, mode=None, filename=None, path=None):
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


if __name__ == "__main__":
    yt = TubeFox('https://www.youtube.com/watch?v=VIDEO_ID')
    print(yt.id)
    print(yt.title)
    print(yt.description)
    print(yt.keywords)
    yt.download_video()
    yt.download_video(path='../', filename='tubefox_test_video', quality=360)
    yt.download_muted_video()
    yt.download_muted_video(path='../', filename='tubefox_test_muted_video', quality=1080)
    yt.download_audio()
    yt.download_audio(path='../', filename='tubefox_test_audio')
    yt.download_thumbnail()
    yt.download_thumbnail(path='../')
    yt.download_subtitles(mode='srt')
    yt.download_subtitles()

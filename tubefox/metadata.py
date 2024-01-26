from tubefox.web_scraper import WebScraper


class Metadata(WebScraper):
    def __init__(self, video_url):
        super().__init__(video_url)
        self.all_data = self.data_dict.get('videoDetails', {})

    @property
    def id(self):
        """
        Property representing the video ID extracted from the video details.
        Returns an empty string if the video ID is not available.
        """
        return self.all_data.get('videoId', '')

    @property
    def title(self):
        """
        Property representing the title of the video extracted from the video details.
        Returns an empty string if the title is not available.
        """
        return self.all_data.get('title', '')

    @property
    def description(self):
        """
        Property representing the short description of the video extracted from the video details.
        Returns an empty string if the description is not available.
        """
        return self.all_data.get('shortDescription', '')

    @property
    def keywords(self):
        """
        Property representing the keywords of the video extracted from the video details.
        Returns a comma-separated string of keywords. Returns an empty string if keywords are not available.
        """
        keywords = self.all_data.get('keywords', [])
        return ', '.join(keywords)


if __name__ == "__main__":
    pass

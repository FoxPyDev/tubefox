import requests
import logging
from tubefox.yt_app_version_updater import get_yt_app_latest_version


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Downloader:


    """
    Downloader class for downloading files from URLs.

    Args:
        path (str): The path where the downloaded file will be saved.
        filename (str): The name of the downloaded file.
        file_type (str): The type of the downloaded file (e.g., 'video', 'audio', 'thumbnail').
        download_link (str): The URL from which the file will be downloaded.
        extension (str): The file extension of the downloaded file.
        chunk_size (int, optional): The size of each chunk in bytes for streaming. Defaults to 1024.

    Attributes:
        path (str): The path where the downloaded file will be saved.
        filename (str): The name of the downloaded file.
        file_type (str): The type of the downloaded file.
        download_link (str): The URL from which the file will be downloaded.
        extension (str): The file extension of the downloaded file.
        chunk_size (int): The size of each chunk in bytes for streaming.

    Methods:
        download_file: Download the file from the provided URL and save it to the specified path.

    Note:
        This class utilizes the requests library for making HTTP requests and tqdm for displaying progress bars.
    """

    latest_version = get_yt_app_latest_version()
    version_to_use = '19.08.36' if latest_version is None else latest_version

    def __init__(self, path: str, filename: str, file_type: str, download_link: str, extension: str,
                 chunk_size: int = 1024) -> None:
        self.path: str = path
        self.filename: str = filename
        self.file_type: str = file_type
        self.download_link: str = download_link
        self.extension: str = extension
        self.chunk_size: int = chunk_size

    def download_file(self) -> None:
        """
        Download the file from the provided URL and save it to the specified path.

        Returns:
            None
        """
        # Check if the link is empty or None
        if not self.download_link:
            logger.error(f"No {self.file_type} download link available.")
            return

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'com.google.android.youtube/{Downloader.version_to_use} (Linux; U; Android 12; GB) gzip'
        }

        response = requests.get(self.download_link, stream=True, headers=headers)
        if response.status_code == 200:
            logger.info(f"Start download {self.file_type}")
            with open(f'{self.path}{self.filename}.{self.extension}', 'wb') as file:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        file.write(chunk)
            logger.info(f"{self.file_type} downloaded")
        else:
            logger.error("Error connecting")
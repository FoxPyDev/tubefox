import html
from tubefox.helpers import TimeConvertor
from bs4 import BeautifulSoup
import requests


def save_subtitle(filename: str, path: str, filetype: str, subtitle: str) -> None:
    """
    Save subtitles to a file.

    Args:
        filename (str): The name of the subtitle file.
        path (str): The path where the subtitle file will be saved.
        filetype (str): The type of the subtitle file (e.g., 'srt', 'txt').
        subtitle (str): The subtitle content to be saved to the file.

    Returns:
        None
    """
    with open(f'{path}{filename}.{filetype}', 'wb') as subtitle_file:
        subtitle_file.write(subtitle.encode())


class Subtitles:
    """
    Subtitles class for processing subtitle data.

    Args:
        subtitle_link (str): The URL of the subtitle file.

    Attributes:
        subtitle_link (str): The URL of the subtitle file.
        xml_subtitle (BeautifulSoup): A BeautifulSoup object containing the parsed XML of the subtitle file.
    """

    def __init__(self, subtitle_link: str) -> None:
        self.subtitle_link: str = subtitle_link
        self.xml_subtitle: BeautifulSoup = BeautifulSoup(requests.get(self.subtitle_link).text, "xml")

    @property
    def subtitles_to_text(self) -> str:
        """
        Convert subtitles to plain text format.

        Returns:
            str: The plain text representation of the subtitles.
        """
        subtitle: str = self.xml_subtitle.get_text(separator='\n')
        return html.unescape(subtitle)

    @property
    def subtitles_to_srt(self) -> str:
        """
        Convert subtitles to SubRip (SRT) format.

        Returns:
            str: The SubRip (SRT) formatted subtitles.
        """
        text_blocks = self.xml_subtitle.findAll("text")
        formatted_subtitles: str = ''
        for block in text_blocks:
            convertor = TimeConvertor(float(block['start']), float(block['dur']))
            formatted_subtitles += (f'{text_blocks.index(block)+1}\n{convertor.convert_start_time} --> '
                                    f'{convertor.convert_end_time}\n{html.unescape(block.text)}\n\n')
        return formatted_subtitles

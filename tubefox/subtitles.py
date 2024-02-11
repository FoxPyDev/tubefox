import html
from helpers import TimeConvertor
from bs4 import BeautifulSoup
import requests


def save_subtitle(filename, path, filetype, subtitle):
    with open(f'{path}{filename}.{filetype}', 'wb') as subtitle_file:
        subtitle_file.write(subtitle.encode())


class Subtitles:
    def __init__(self, subtitle_link):
        self.subtitle_link = subtitle_link
        self.xml_subtitle = BeautifulSoup(requests.get(self.subtitle_link).text, "xml")

    @property
    def subtitles_to_text(self):
        subtitle = self.xml_subtitle.get_text(separator='\n')
        return html.unescape(subtitle)

    @property
    def subtitles_to_srt(self):
        text_blocks = self.xml_subtitle.findAll("text")
        formatted_subtitles = ''
        for block in text_blocks:
            convertor = TimeConvertor(float(block['start']), float(block['dur']))
            formatted_subtitles += (f'{text_blocks.index(block)+1}\n{convertor.convert_start_time} --> '
                                    f'{convertor.convert_end_time}\n{html.unescape(block.text)}\n')
        return formatted_subtitles

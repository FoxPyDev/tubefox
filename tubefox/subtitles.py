import html
from helpers import TimeConvertor

from bs4 import BeautifulSoup
import requests


class Subtitles:
    def __init__(self, subtitle_link):
        self.subtitle_link = subtitle_link
        self.xml_subtitle = BeautifulSoup(requests.get(self.subtitle_link).text, "xml")

    @property
    def subtitles_to_text(self):
        subtitle = self.xml_subtitle.get_text(separator='\n')
        return html.unescape(subtitle)

    @property
    def subtitles_to_sub(self):
        text_blocks = self.xml_subtitle.findAll("text")
        formatted_subtitles = ''
        for block in text_blocks:
            convertor = TimeConvertor(float(block['start']), float(block['dur']))
            formatted_subtitles += (f'{text_blocks.index(block)+1}\n{convertor.convert_start_time} --> '
                                    f'{convertor.convert_end_time}\n{html.unescape(block.text)}\n')
        return formatted_subtitles


if __name__ == "__main__":
    sbt = Subtitles("https://www.youtube.com/api/timedtext?v=HnjVSCnPYCU&ei=uK26ZaXtHZWB6dsPyf2bmA4&caps=asr&opi=112496729&xoaf=5&hl=uk&ip=0.0.0.0&ipbits=0&expire=1706758184&sparams=ip,ipbits,expire,v,ei,caps,opi,xoaf&signature=21E9A8A218B683A631516235BBAFFD1BA37254A5.79CBE56072BB4A9D1703A7EF113EE73CA60D03FA&key=yt8&kind=asr&lang=uk")
    # print(sbt.subtitles_to_text)
    # print(sbt.xml_subtitle)
    print(sbt.subtitles_to_sub)

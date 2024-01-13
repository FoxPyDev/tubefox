# TubeFox

TubeFox is a lightweight and easy-to-use Python module designed for retrieving information about YouTube videos. 

It allows users to fetch details such as video title, description, tags, and provides functionality for downloading videos and video thumbnails. 

This module is built on top of the requests and beautifulsoup4 libraries.

## Usage

```python
import TubeFox

# Example usage
video_url = "https://www.youtube.com/watch?v=your_video_id"
tube_fox_instance = TubeFox(video_url)

# Retrieve video details
print("Video ID:", tube_fox_instance.videoid)
print("Title:", tube_fox_instance.title)
print("Description:", tube_fox_instance.description)
print("Keywords:", tube_fox_instance.keywords)

# Additional functionalities (to be implemented)
tube_fox_instance.download_video
tube_fox_instance.download_thumbnail
tube_fox_instance.download_audio
tube_fox_instance.download_subtitles
```
## Contact
Author: [FoxPyDev](https://github.com/FoxPyDev)

Telegram: [FoxPyDev](https://t.me/FoxPyDev)

E-mail: foxpythondev@gmail.com

Feel free to reach out for any questions, suggestions, or feedback!


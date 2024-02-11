# TubeFox
TubeFox is a Python library that provides convenient methods for scraping data, downloading media, and managing subtitles from YouTube videos.

## Installation
You can install TubeFox using pip:
```python
pip install tubefox
```

## Usage

```python
from tubefox import TubeFox

# Initialize TubeFox with the URL of the YouTube video
yt = TubeFox('https://www.youtube.com/watch?v=VIDEO_ID')

# Get video metadata
print("Video ID:", yt.id)
print("Title:", yt.title)
print("Description:", yt.description)
print("Keywords:", yt.keywords)

# Download video
yt.download_video()

# Download video with custom options
yt.download_video(path='../', filename='tubefox_test_video', quality=360)

# Download muted video
yt.download_muted_video()

# Download muted video with custom options
yt.download_muted_video(path='../', filename='tubefox_test_muted_video', quality=1080)

# Download audio
yt.download_audio()

# Download audio with custom options
yt.download_audio(path='../', filename='tubefox_test_audio')

# Download thumbnail
yt.download_thumbnail()

# Download thumbnail with custom options
yt.download_thumbnail(path='../')

# Download subtitles
yt.download_subtitles(mode='srt')

# Download subtitles with default options
yt.download_subtitles()
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! Feel free to submit pull requests or open issues for any bugs or feature requests.

## Acknowledgements
TubeFox uses the following open-source libraries:
```python
BeautifulSoup
requests
tqdm
```
## Disclaimer
This project is not affiliated with or endorsed by YouTube. Use responsibly and respect the terms of service of the platforms you interact with.
## Contact
Author: [FoxPyDev](https://github.com/FoxPyDev)

Telegram: [FoxPyDev](https://t.me/FoxPyDev)

E-mail: foxpythondev@gmail.com

Feel free to reach out for any questions, suggestions, or feedback!


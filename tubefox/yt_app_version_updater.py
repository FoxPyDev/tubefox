import logging
import requests
from bs4 import BeautifulSoup

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_yt_app_latest_version():
    """
    Fetches the latest version of the YouTube app from a specified URL.

    Returns:
    - The latest version of the YouTube app if successful.
    - None if there's an error during the process.
    """
    url = 'https://androidapksfree.com/youtube/com-google-android-youtube/old/'

    try:
        # Making a GET request to fetch the webpage
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        # Logging error message if fetching the webpage fails
        logger.error(f"Failed to fetch the latest version: {e}")
        return None

    try:
        # Parsing the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')
        version_element = soup.find('span', class_='limit-line')
        if version_element:
            # Stripping whitespace and extracting the first 8 characters of the version text
            version_text = version_element.get_text().strip()[:8]
            return version_text
        else:
            # Logging a warning if the version element is not found
            logger.warning("Version element not found.")
            return None
    except Exception as e:
        # Logging error message if parsing the HTML fails
        logger.error(f"Error occurred during parsing: {e}")
        return None


if __name__ == "__main__":
    # Fetching the latest version of the YouTube app
    latest_version = get_yt_app_latest_version()
    if latest_version:
        # Logging the latest version if successful
        logger.info(f"The latest version of YouTube app is: {latest_version}")
    else:
        # Logging a warning if fetching the latest version fails
        logger.warning("Failed to fetch the latest version.")
